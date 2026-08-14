import secrets

from django.conf import settings
from django.db import models

from notifications.models import SingletonSettings

from .validators import validate_icon_extension, validate_icon_size


class Badge(models.Model):
    """Тип награды, который админ определяет один раз. Условие получения по приоритету:
    wave задана - только эта конкретная волна (например, годовой/квартальный цикл обязательного
    курса - "Пароли 2026" и "Пароли 2027" это два разных объекта Badge, каждый со своей волной,
    иконкой и годом в названии); wave пуста, но задан course - любая волна этого курса
    (не разделяется по циклам); оба пусты - любой пройденный курс вообще."""

    name = models.CharField("Name", max_length=255)
    description = models.TextField("Description", blank=True)
    icon = models.ImageField(
        "Icon",
        upload_to="badges/icons/",
        validators=[validate_icon_extension, validate_icon_size],
    )
    course = models.ForeignKey(
        "courses.Course",
        verbose_name="Course",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="badges",
        help_text="Leave empty to award for completing any course. Ignored if a wave is specified.",
    )
    wave = models.ForeignKey(
        "waves.TrainingWave",
        verbose_name="Wave (cycle)",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="badges",
        help_text="Use for annual/quarterly badges - the badge will only be awarded for completing this specific wave, not any wave of the same course.",
    )
    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="A disabled badge is no longer awarded; badges already awarded are not revoked",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


def _generate_badge_token():
    return secrets.token_urlsafe(24)


class EmployeeBadge(models.Model):
    """Факт выдачи награды сотруднику. badge_name_snapshot замораживает название на момент
    выдачи - см. WaveAssignment.department_snapshot/IntegrationLog.token_name_snapshot за тем же
    прецедентом: если админ переименует награду после того как сотрудник уже поделился ссылкой,
    публичная страница должна продолжать показывать то, что реально было получено. token хранится
    в открытом виде (не хэшируется, в отличие от IntegrationToken) - он изначально предназначен
    для публикации, а не является credential."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Employee", on_delete=models.CASCADE, related_name="badges"
    )
    badge = models.ForeignKey(Badge, verbose_name="Badge", on_delete=models.PROTECT, related_name="awards")
    badge_name_snapshot = models.CharField("Name at time of award", max_length=255, editable=False)
    wave_assignment = models.ForeignKey(
        "waves.WaveAssignment", verbose_name="Wave assignment", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    token = models.CharField(max_length=40, unique=True, editable=False, default=_generate_badge_token)
    awarded_at = models.DateTimeField("Awarded", auto_now_add=True)

    class Meta:
        verbose_name = "Awarded badge"
        verbose_name_plural = "Awarded badges"
        unique_together = [("employee", "badge")]
        ordering = ["-awarded_at"]

    def __str__(self):
        return f"{self.employee.full_name} - {self.badge_name_snapshot}"

    def save(self, *args, **kwargs):
        if not self.badge_name_snapshot and self.badge_id:
            self.badge_name_snapshot = self.badge.name
        super().save(*args, **kwargs)


class BadgeSettings(SingletonSettings):
    """Единственная запись (singleton) - решает, показывать ли настоящее имя сотрудника на
    публичной странице подтверждения награды."""

    show_real_name = models.BooleanField("Show real name on the public page", default=True)

    class Meta:
        verbose_name = "Badge settings"
        verbose_name_plural = "Badge settings"

    def __str__(self):
        return "Badge settings"
