from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

LOGIN_LOCKOUT_THRESHOLD = 5
LOGIN_LOCKOUT_DURATION = timedelta(minutes=15)


class UserManager(BaseUserManager):
    """Django's own UserManager hardcodes a positional `username` in create_superuser(), which
    breaks manage.py createsuperuser for this email-based model (username isn't a required
    field, so the command never collects it)."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class Department(models.Model):
    name = models.CharField("Name", max_length=200, unique=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    """A company employee. Logs in by email, not by username.

    The role is stored via Django's standard is_staff/is_superuser, without a separate field:
    an employee (both False) can't access the console, a training manager (is_staff=True) can run
    courses and waves, and a full administrator (plus is_superuser=True) sees everything, including LDAP,
    integrations, notifications, and management of other users' roles."""

    ROLE_EMPLOYEE = "employee"
    ROLE_MANAGER = "manager"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [ROLE_EMPLOYEE, ROLE_MANAGER, ROLE_ADMIN]

    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField("Email", unique=True)
    full_name = models.CharField("Full name", max_length=255)
    department = models.ForeignKey(
        Department, verbose_name="Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="employees"
    )
    position = models.CharField("Position", max_length=200, blank=True)
    must_change_password = models.BooleanField(
        "Password change required",
        default=True,
        help_text="Enabled for new accounts - the user must change their password on first login.",
    )
    failed_login_attempts = models.PositiveIntegerField("Consecutive failed login attempts", default=0)
    locked_until = models.DateTimeField("Locked until", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["full_name"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    @property
    def role(self):
        if self.is_superuser:
            return self.ROLE_ADMIN
        if self.is_staff:
            return self.ROLE_MANAGER
        return self.ROLE_EMPLOYEE

    def set_role(self, role):
        if role not in self.ROLE_CHOICES:
            raise ValueError(f"Unknown role: {role}")
        self.is_staff = role in (self.ROLE_MANAGER, self.ROLE_ADMIN)
        self.is_superuser = role == self.ROLE_ADMIN

    def is_locked_out(self):
        return bool(self.locked_until and self.locked_until > timezone.now())

    def register_failed_login(self):
        """Separate from the IP throttle on LoginView - protects a specific account from a password-guessing
        attack distributed across many IPs, where an IP-based limit wouldn't help. If the previous
        lockout has already expired, the counter is reset before the new incident - otherwise it would grow
        indefinitely, and a single random typo a day after the first lockout would lock the account
        again."""
        if self.locked_until and self.locked_until <= timezone.now():
            self.failed_login_attempts = 0
            self.locked_until = None
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= LOGIN_LOCKOUT_THRESHOLD:
            self.locked_until = timezone.now() + LOGIN_LOCKOUT_DURATION
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def clear_lockout(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=["failed_login_attempts", "locked_until"])


class LdapSettings(models.Model):
    """A single (singleton) record - AD/LDAP settings, editable from the admin console."""

    enabled = models.BooleanField("Enabled", default=False)
    server_uri = models.CharField(
        "Server URI", max_length=255, blank=True, help_text="For example: ldaps://dc1.company.local"
    )
    start_tls = models.BooleanField("StartTLS", default=False)
    bind_dn = models.CharField("Bind DN", max_length=255, blank=True)
    bind_password = models.CharField("Bind password", max_length=255, blank=True)
    user_search_base = models.CharField("User search base", max_length=255, blank=True)
    user_search_filter = models.CharField(
        "Search filter", max_length=255, blank=True, default="(mail=%(user)s)"
    )
    attr_full_name = models.CharField("Full name attribute", max_length=100, blank=True, default="displayName")
    attr_email = models.CharField("Email attribute", max_length=100, blank=True, default="mail")
    attr_department = models.CharField("Department attribute", max_length=100, blank=True, default="department")
    updated_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = "LDAP/AD settings"
        verbose_name_plural = "LDAP/AD settings"

    def __str__(self):
        return "LDAP/AD settings"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SecuritySettings(models.Model):
    """A single (singleton) record - login-protection toggles, editable from the console."""

    login_lockout_enabled = models.BooleanField(
        "Lock account after repeated failed passwords",
        default=True,
        help_text="When disabled, only the IP-based rate limit on the login endpoint itself remains.",
    )

    class Meta:
        verbose_name = "Login security settings"
        verbose_name_plural = "Login security settings"

    def __str__(self):
        return "Login security settings"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class LoginAttemptLog(models.Model):
    """A log of every login attempt (successful or not) - for auditing who tried to log in and from where."""

    email = models.CharField("Email entered", max_length=255)
    ip_address = models.GenericIPAddressField("IP address", null=True, blank=True)
    success = models.BooleanField("Successful")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Login log entry"
        verbose_name_plural = "Login log"
        ordering = ["-created_at"]

    def __str__(self):
        status = "success" if self.success else "failed"
        return f"{self.email} - {status} - {self.created_at:%Y-%m-%d %H:%M}"
