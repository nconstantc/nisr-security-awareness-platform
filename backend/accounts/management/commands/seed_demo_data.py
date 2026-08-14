import os
import random
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import Department, User
from quizzes.models import QuizAttempt
from waves.models import TrainingWave, WaveAssignment

DEMO_PASSWORD = "Demo12345!"

DEPARTMENTS = [
    "IT Department",
    "Accounting",
    "Sales Department",
    "HR Department",
    "Legal Department",
    "Security Service",
]

EMPLOYEES = [
    ("Amanda Nolan", "amanda.nolan"),
    ("Dmitry Volkov", "dmitry.volkov"),
    ("Alice Jameson", "alice.jameson"),
    ("Sergey Petrov", "sergey.petrov"),
    ("Grace Hamilton", "grace.hamilton"),
    ("Alexander Kim", "alexander.kim"),
    ("Maria Sokolova", "maria.sokolova"),
    ("Ethan Byrne", "ethan.byrne"),
    ("Natalie Cooper", "natalie.cooper"),
    ("Timur Yessenov", "timur.yessenov"),
    ("Victoria Smith", "victoria.smith"),
    ("Ashley Turner", "ashley.turner"),
    ("Igor Morozov", "igor.morozov"),
    ("Jenna Abbott", "jenna.abbott"),
    ("Paul Newman", "paul.newman"),
    ("Diana Sutton", "diana.sutton"),
    ("Roman Lebedev", "roman.lebedev"),
    ("Kevin Ospanov", "kevin.ospanov"),
    ("Elena Popova", "elena.popova"),
    ("Bradley Isaev", "bradley.isaev"),
    ("Olivia Walsh", "olivia.walsh"),
    ("Dana Campbell", "dana.campbell"),
    ("Maxim Soloviev", "maxim.soloviev"),
    ("Gabrielle Sharpe", "gabrielle.sharpe"),
]


class Command(BaseCommand):
    help = (
        "Наполняет базу демонстрационными данными для скриншотов и презентации - отделы, "
        "сотрудники и результаты обучения с разными исходами (сдал/не сдал/в процессе/не "
        f"начал). Не для продакшена - у всех демо-сотрудников один и тот же пароль ({DEMO_PASSWORD}). "
        "Отделы и сотрудники создаются идемпотентно (get_or_create), попытки тестов при "
        "повторном запуске добавляются заново поверх существующих назначений."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        if os.environ.get("ALLOW_DEMO_SEED", "").strip().lower() not in ("1", "true", "yes", "on"):
            raise CommandError(
                "Эта команда создает фиктивных сотрудников и записывает им результаты в РЕАЛЬНЫЕ "
                "активные волны - на настоящей базе компании это испортит статистику по живым "
                "сотрудникам. Если это действительно демо/тестовый инстанс, запустите с "
                "ALLOW_DEMO_SEED=true в окружении."
            )

        departments = [Department.objects.get_or_create(name=name)[0] for name in DEPARTMENTS]

        employees = []
        for i, (full_name, username) in enumerate(EMPLOYEES):
            email = f"{username}@awareness.local"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email,
                    "full_name": full_name,
                    "department": departments[i % len(departments)],
                    "position": "Employee",
                    "is_active": True,
                    "must_change_password": False,
                },
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save(update_fields=["password"])
            employees.append(user)

        waves = list(TrainingWave.objects.filter(status=TrainingWave.ACTIVE).select_related("course"))
        if not waves:
            self.stdout.write(self.style.WARNING("Нет активных волн - сначала запустите обучение хотя бы по одному курсу."))
            return

        created_assignments = 0
        created_attempts = 0
        for wave in waves:
            question_ids = list(wave.course.questions.filter(is_active=True).values_list("id", flat=True))
            participants = random.sample(employees, k=random.randint(min(8, len(employees)), len(employees)))

            for employee in participants:
                assignment, was_created = WaveAssignment.objects.get_or_create(wave=wave, employee=employee)
                if was_created:
                    created_assignments += 1
                    WaveAssignment.objects.filter(pk=assignment.pk).update(
                        assigned_at=timezone.now() - timedelta(days=random.randint(1, 25))
                    )

                if not question_ids:
                    continue
                outcome = random.choices(
                    ["passed_first", "passed_retry", "failed", "not_started"],
                    weights=[45, 15, 15, 25],
                )[0]
                if outcome == "not_started":
                    continue

                def make_attempt(passed, days_ago):
                    score = random.uniform(wave.pass_threshold, 100) if passed else random.uniform(40, wave.pass_threshold - 1)
                    started = timezone.now() - timedelta(days=days_ago, hours=random.randint(0, 5))
                    attempt = QuizAttempt.objects.create(
                        wave_assignment=assignment,
                        question_set=question_ids,
                        pass_threshold_snapshot=wave.pass_threshold,
                        score_percent=round(score, 2),
                        passed=passed,
                    )
                    QuizAttempt.objects.filter(pk=attempt.pk).update(
                        started_at=started, submitted_at=started + timedelta(minutes=random.randint(5, 20))
                    )

                if outcome == "passed_first":
                    make_attempt(True, random.randint(0, 20))
                    created_attempts += 1
                elif outcome == "passed_retry":
                    make_attempt(False, random.randint(10, 20))
                    make_attempt(True, random.randint(0, 9))
                    created_attempts += 2
                elif outcome == "failed":
                    for _ in range(wave.max_attempts or random.randint(1, 2)):
                        make_attempt(False, random.randint(0, 15))
                        created_attempts += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: {len(employees)} демо-сотрудников, {created_assignments} новых назначений, "
                f"{created_attempts} новых попыток тестов. Пароль демо-сотрудников: {DEMO_PASSWORD}"
            )
        )
