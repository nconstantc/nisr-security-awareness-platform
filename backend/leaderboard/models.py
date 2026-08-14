from django.db import models

from notifications.models import SingletonSettings


class LeaderboardSettings(SingletonSettings):
    """Единственная запись (singleton) - лидерборды по умолчанию выключены, т.к. публичный
    рейтинг по успеваемости в ИБ - HR-чувствительная тема, может демотивировать отстающих
    (см. .claude/internal/pro-roadmap.md #5)."""

    enabled = models.BooleanField("Show leaderboards to employees", default=False)

    class Meta:
        verbose_name = "Leaderboard settings"
        verbose_name_plural = "Leaderboard settings"

    def __str__(self):
        return "Leaderboard settings"
