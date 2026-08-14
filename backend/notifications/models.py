from django.db import models

from config.crypto import decrypt, encrypt


def encrypted_property(field_name):
    """password = encrypted_property('password_encrypted') - шифрует/расшифровывает прозрачно,
    сам секрет никогда не хранится и не сериализуется в открытом виде."""

    def getter(self):
        return decrypt(getattr(self, field_name))

    def setter(self, value):
        setattr(self, field_name, encrypt(value))

    return property(getter, setter)


def is_set_property(field_name):
    return property(lambda self: bool(getattr(self, field_name)))


class SingletonSettings(models.Model):
    """Единственная запись (pk=1), как accounts.LdapSettings - настройки одного канала уведомлений."""

    class Meta:
        abstract = True

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class EmailSettings(SingletonSettings):
    enabled = models.BooleanField("Enabled", default=False)
    smtp_host = models.CharField("SMTP server", max_length=255, blank=True)
    smtp_port = models.PositiveIntegerField("Port", default=587)
    use_tls = models.BooleanField("STARTTLS", default=True)
    username = models.CharField("Login", max_length=255, blank=True)
    password_encrypted = models.CharField("Password (encrypted)", max_length=500, blank=True, editable=False)
    from_email = models.EmailField("Sender email", blank=True)
    from_name = models.CharField("Sender name", max_length=255, blank=True, default="Awareness")
    updated_at = models.DateTimeField("Updated", auto_now=True)

    password = encrypted_property("password_encrypted")
    password_set = is_set_property("password_encrypted")

    class Meta:
        verbose_name = "Email settings (SMTP)"
        verbose_name_plural = "Email settings (SMTP)"

    def __str__(self):
        return "Email settings (SMTP)"


class TelegramSettings(SingletonSettings):
    """Бот-токен + один целевой chat_id (группа/канал для админов) - без персональных ЛС сотрудникам."""

    enabled = models.BooleanField("Enabled", default=False)
    bot_token_encrypted = models.CharField("Bot token (encrypted)", max_length=500, blank=True, editable=False)
    chat_id = models.CharField(
        "Chat ID", max_length=100, blank=True, help_text="ID of the group/channel the bot sends notifications to"
    )
    updated_at = models.DateTimeField("Updated", auto_now=True)

    bot_token = encrypted_property("bot_token_encrypted")
    bot_token_set = is_set_property("bot_token_encrypted")

    class Meta:
        verbose_name = "Telegram settings"
        verbose_name_plural = "Telegram settings"

    def __str__(self):
        return "Telegram settings"


class SlackSettings(SingletonSettings):
    enabled = models.BooleanField("Enabled", default=False)
    webhook_url_encrypted = models.CharField(
        "Webhook URL (encrypted)", max_length=1000, blank=True, editable=False
    )
    updated_at = models.DateTimeField("Updated", auto_now=True)

    webhook_url = encrypted_property("webhook_url_encrypted")
    webhook_url_set = is_set_property("webhook_url_encrypted")

    class Meta:
        verbose_name = "Slack settings"
        verbose_name_plural = "Slack settings"

    def __str__(self):
        return "Slack settings"


class TeamsSettings(SingletonSettings):
    enabled = models.BooleanField("Enabled", default=False)
    webhook_url_encrypted = models.CharField(
        "Webhook URL (encrypted)", max_length=1000, blank=True, editable=False
    )
    updated_at = models.DateTimeField("Updated", auto_now=True)

    webhook_url = encrypted_property("webhook_url_encrypted")
    webhook_url_set = is_set_property("webhook_url_encrypted")

    class Meta:
        verbose_name = "Microsoft Teams settings"
        verbose_name_plural = "Microsoft Teams settings"

    def __str__(self):
        return "Microsoft Teams settings"


class NotificationLog(models.Model):
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("telegram", "Telegram"),
        ("slack", "Slack"),
        ("teams", "Microsoft Teams"),
    ]

    channel = models.CharField("Channel", max_length=20, choices=CHANNEL_CHOICES)
    event = models.CharField("Event", max_length=50)
    target = models.CharField("Recipient", max_length=255, blank=True)
    success = models.BooleanField("Successful")
    message = models.CharField("Result", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification log entry"
        verbose_name_plural = "Notification log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.channel}:{self.event} -> {self.target} ({'ok' if self.success else 'error'})"
