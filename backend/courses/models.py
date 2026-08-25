from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from .validators import validate_icon_extension, validate_icon_size


class Course(models.Model):
    title = models.CharField("Title", max_length=255)
    description = models.TextField("Description", blank=True)
    icon = models.ImageField(
        "Icon",
        upload_to="courses/icons/",
        null=True,
        blank=True,
        validators=[validate_icon_extension, validate_icon_size],
    )
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, related_name="chapters")
    order = models.PositiveIntegerField("Order", default=0)
    title = models.CharField("Title", max_length=255)
    content = CKEditor5Field("Content", config_name="default", blank=True, default="")
    pdf_file = models.FileField(
        "PDF Document",
        upload_to="chapters/pdfs/",
        blank=True,
        null=True,
        help_text="Upload a PDF document related to this chapter"
    )

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        ordering = ["course", "order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    SINGLE = "single"
    MULTIPLE = "multiple"
    QUESTION_TYPES = [
        (SINGLE, "Single correct answer"),
        (MULTIPLE, "Multiple correct answers"),
    ]

    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, related_name="questions")
    chapter = models.ForeignKey(
        Chapter, verbose_name="Chapter", on_delete=models.SET_NULL, null=True, blank=True, related_name="questions"
    )
    text = models.TextField("Question text")
    question_type = models.CharField("Type", max_length=10, choices=QUESTION_TYPES, default=SINGLE)
    explanation = models.TextField("Explanation", blank=True, help_text="Shown after answering")
    is_active = models.BooleanField("Active", default=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text[:80]


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name="Question", on_delete=models.CASCADE, related_name="choices")
    text = models.CharField("Choice text", max_length=500)
    is_correct = models.BooleanField("Correct", default=False)
    order = models.PositiveIntegerField("Order", default=0)

    class Meta:
        verbose_name = "Answer choice"
        verbose_name_plural = "Answer choices"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text