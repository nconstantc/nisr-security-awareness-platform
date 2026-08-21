from django.apps import AppConfig


class QuizzesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quizzes'

    from django.apps import AppConfig
    def ready(self):
        # Import signals to register them
        import quizzes.signals  # noqa: F401
