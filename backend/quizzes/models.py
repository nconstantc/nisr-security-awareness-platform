from django.db import models
from django.utils import timezone

from courses.models import Choice, Question
from waves.models import WaveAssignment

FORFEIT_REASON_CHOICES = [("focus_loss", "Lost focus on the quiz page")]


class QuizAttempt(models.Model):
    """
    Одна попытка прохождения теста. После submitted_at попытка иммутабельна -
    это аудиторский след для регулятора (кто, когда, что отвечал, какой был порог).
    """

    wave_assignment = models.ForeignKey(
        WaveAssignment, verbose_name="Wave assignment", on_delete=models.CASCADE, related_name="attempts"
    )
    question_set = models.JSONField(
        "Question snapshot",
        help_text="List of question IDs shown in this attempt, in the order shown",
    )
    pass_threshold_snapshot = models.PositiveSmallIntegerField("Pass threshold at time of attempt")
    started_at = models.DateTimeField("Started", auto_now_add=True)
    submitted_at = models.DateTimeField("Submitted", null=True, blank=True)
    score_percent = models.FloatField("Score, %", null=True, blank=True)
    passed = models.BooleanField("Passed", default=False)
    forfeited_reason = models.CharField(
        "Reason for forced failure",
        max_length=20,
        choices=FORFEIT_REASON_CHOICES,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "Quiz attempt"
        verbose_name_plural = "Quiz attempts"
        ordering = ["-started_at"]

    def __str__(self):
        who = self.wave_assignment.employee.full_name
        return f"{who} - {self.wave_assignment.wave.name} ({self.started_at:%Y-%m-%d})"

    @property
    def is_submitted(self):
        return self.submitted_at is not None

    def finalize(self, forfeited_reason=""):
        """Подсчитать балл, зафиксировать результат. Идемпотентно - повторный вызов ничего не делает."""
        if self.is_submitted:
            return
        answers = list(self.answers.select_related("question"))
        total = len(self.question_set)
        correct = sum(1 for a in answers if a.is_correct)
        self.score_percent = round((correct / total) * 100, 2) if total else 0.0
        # Честный балл сохраняется даже при форфейте - это аудиторский след ("87%, но покинул
        # страницу") ценнее плоского 0%, а passed все равно форсится в False, так что итог для
        # статуса волны не меняется.
        self.passed = False if forfeited_reason else self.score_percent >= self.pass_threshold_snapshot
        self.forfeited_reason = forfeited_reason
        self.submitted_at = timezone.now()
        self.save(update_fields=["score_percent", "passed", "submitted_at", "forfeited_reason"])


class QuizSecuritySettings(models.Model):
    """Единственная запись (singleton) - переключатель контроля фокуса на тесте, редактируется
    из консоли (/console/security)."""

    focus_control_enabled = models.BooleanField(
        "Focus control during quiz",
        default=True,
        help_text="When disabled, switching to another window/tab during the quiz is not tracked and does not cause an automatic fail.",
    )

    class Meta:
        verbose_name = "Focus control settings"
        verbose_name_plural = "Focus control settings"

    def __str__(self):
        return "Focus control settings"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, verbose_name="Attempt", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, verbose_name="Question", on_delete=models.PROTECT, related_name="+")
    selected_choices = models.JSONField("Selected choices (IDs)", default=list)
    is_correct = models.BooleanField("Correct", default=False)

    class Meta:
        verbose_name = "Question answer"
        verbose_name_plural = "Question answers"
        unique_together = [("attempt", "question")]

    def __str__(self):
        return f"{self.attempt_id} - {self.question_id}"

    def evaluate(self):
        correct_ids = set(Choice.objects.filter(question_id=self.question_id, is_correct=True).values_list("id", flat=True))
        self.is_correct = set(self.selected_choices) == correct_ids
        return self.is_correct
