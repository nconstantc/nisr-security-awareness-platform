import hashlib
import secrets

from django.conf import settings
from django.db import models


def generate_token():
    return f"awr_{secrets.token_urlsafe(32)}"


def hash_token(raw_token):
    return hashlib.sha256(raw_token.encode()).hexdigest()


class IntegrationToken(models.Model):
    """Токен для сервис-сервис вызовов внешних систем (не для людей - см. IntegrationTokenAuthentication).
    Сам токен не хранится - только его хэш, как пароль."""

    name = models.CharField("Integration name", max_length=255)
    prefix = models.CharField("Token prefix", max_length=16, editable=False)
    token_hash = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField("Active", default=True)
    allowed_courses = models.ManyToManyField(
        "courses.Course",
        verbose_name="Allowed courses",
        related_name="integration_tokens",
        help_text="The token can only assign training for these courses - this limits the damage if the token is leaked.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Created by", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField("Last used", null=True, blank=True)

    class Meta:
        verbose_name = "Integration token"
        verbose_name_plural = "Integration tokens"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.prefix}...)"

    @classmethod
    def issue(cls, name, courses, created_by=None):
        """Создает токен и возвращает (instance, plaintext_token) - открытый текст виден только один раз."""
        raw_token = generate_token()
        instance = cls.objects.create(
            name=name,
            prefix=raw_token[:12],
            token_hash=hash_token(raw_token),
            created_by=created_by,
        )
        instance.allowed_courses.set(courses)
        return instance, raw_token


class IntegrationLog(models.Model):
    """Журнал каждого вызова публичного API интеграций - нужен для аудита (требования АРФР)."""

    token = models.ForeignKey(
        IntegrationToken, verbose_name="Token", on_delete=models.SET_NULL, null=True, related_name="logs"
    )
    token_name_snapshot = models.CharField("Token name at time of call", max_length=255)
    employee_email = models.CharField("Employee email", max_length=255)
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Employee", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    course = models.ForeignKey(
        "courses.Course", verbose_name="Course", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    reason = models.CharField("Reason (from integration)", max_length=255, blank=True)
    success = models.BooleanField("Successful")
    message = models.CharField("Result", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Integration log entry"
        verbose_name_plural = "Integration log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.token_name_snapshot} -> {self.employee_email} ({'ok' if self.success else 'error'})"
