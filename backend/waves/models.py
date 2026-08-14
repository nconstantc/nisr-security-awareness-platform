from django.conf import settings
from django.db import models

from accounts.models import Department
from courses.models import Course


class TrainingWave(models.Model):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (ACTIVE, "Active"),
        (CLOSED, "Closed"),
    ]

    name = models.CharField("Wave name", max_length=255)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.PROTECT, related_name="waves")
    start_date = models.DateField("Start date")
    deadline = models.DateField("Deadline")
    pass_threshold = models.PositiveSmallIntegerField("Pass threshold, %", default=95)
    max_attempts = models.PositiveSmallIntegerField(
        "Max attempts", null=True, blank=True, help_text="Empty = no limit"
    )
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Created by", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Training wave"
        verbose_name_plural = "Training waves"
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

    @property
    def is_overdue(self):
        from django.utils import timezone

        return self.deadline < timezone.localdate() and self.status != self.CLOSED


class WaveAssignment(models.Model):
    wave = models.ForeignKey(TrainingWave, verbose_name="Wave", on_delete=models.CASCADE, related_name="assignments")
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Employee", on_delete=models.CASCADE, related_name="wave_assignments"
    )
    department_snapshot = models.ForeignKey(
        Department, verbose_name="Department at time of assignment", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    assigned_at = models.DateTimeField("Assigned", auto_now_add=True)
    reminder_sent_at = models.DateTimeField(
        "Reminder sent",
        null=True,
        blank=True,
        help_text="The deadline reminder is sent once - it is not sent again.",
    )

    class Meta:
        verbose_name = "Wave assignment"
        verbose_name_plural = "Wave assignments"
        unique_together = [("wave", "employee")]

    def __str__(self):
        return f"{self.wave.name} - {self.employee.full_name}"

    def save(self, *args, **kwargs):
        if not self.department_snapshot_id and self.employee_id:
            self.department_snapshot = self.employee.department
        super().save(*args, **kwargs)

    @property
    def best_attempt(self):
        return self.attempts.filter(submitted_at__isnull=False).order_by("-passed", "-score_percent").first()

    @property
    def progress(self):
        """(отвечено, всего) вопросов по последней попытке - для прогресс-бара на портале."""
        attempt = self.attempts.order_by("-started_at").first()
        if not attempt:
            return (0, 0)
        total = len(attempt.question_set)
        if attempt.is_submitted:
            return (total, total)
        return (attempt.answers.count(), total)

    @property
    def status(self):
        """not_started | in_progress | passed | failed"""
        attempts = list(self.attempts.all())
        if not attempts:
            return "not_started"
        if any(a.passed for a in attempts):
            return "passed"
        if self.wave.max_attempts and len(attempts) >= self.wave.max_attempts:
            return "failed"
        return "in_progress"
