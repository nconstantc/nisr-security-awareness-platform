from django import forms
from django.contrib import admin, messages
from django.shortcuts import render
from django.utils.html import format_html

from accounts.models import Department

from .models import TrainingWave, WaveAssignment
from . import services

STATUS_COLORS = {
    "not_started": ("#9ca3af", "Not started"),
    "in_progress": ("#f59e0b", "In progress"),
    "passed": ("#16a34a", "Passed"),
    "failed": ("#dc2626", "Not passed (attempts exhausted)"),
}


def status_badge(status, overdue=False):
    color, label = STATUS_COLORS[status]
    if overdue and status != "passed":
        color, label = "#dc2626", f"{label} · overdue"
    return format_html('<span style="color:#fff;background:{};padding:2px 8px;border-radius:10px;font-size:12px">{}</span>', color, label)


class WaveAssignmentInline(admin.TabularInline):
    model = WaveAssignment
    extra = 0
    fields = ("employee", "department_snapshot", "assigned_at", "status_display", "best_score_display")
    readonly_fields = ("department_snapshot", "assigned_at", "status_display", "best_score_display")
    autocomplete_fields = ["employee"]

    @admin.display(description="Status")
    def status_display(self, obj):
        if not obj.pk:
            return "-"
        overdue = obj.wave.is_overdue
        return status_badge(obj.status, overdue)

    @admin.display(description="Best score")
    def best_score_display(self, obj):
        best = obj.best_attempt if obj.pk else None
        return f"{best.score_percent}%" if best else "-"


class DepartmentAssignForm(forms.Form):
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(), widget=forms.CheckboxSelectMultiple, required=True, label="Departments"
    )


@admin.register(TrainingWave)
class TrainingWaveAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "start_date", "deadline", "status", "pass_threshold", "progress", "overdue_flag")
    list_filter = ("status", "course")
    search_fields = ("name",)
    inlines = [WaveAssignmentInline]
    actions = ["assign_all_active_employees", "assign_by_department"]

    @admin.display(description="Progress")
    def progress(self, obj):
        total = obj.assignments.count()
        if not total:
            return "0/0"
        passed = sum(1 for a in obj.assignments.all() if a.status == "passed")
        return f"{passed}/{total} passed"

    @admin.display(description="Overdue")
    def overdue_flag(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color:#dc2626;font-weight:600">yes</span>')
        return "no"

    @admin.action(description="Assign to all active employees")
    def assign_all_active_employees(self, request, queryset):
        created = sum(services.assign_all_active_employees(wave) for wave in queryset)
        self.message_user(request, f"Assigned {created} employees.", level=messages.SUCCESS)

    @admin.action(description="Assign by department…")
    def assign_by_department(self, request, queryset):
        if "apply" in request.POST:
            form = DepartmentAssignForm(request.POST)
            if form.is_valid():
                departments = form.cleaned_data["departments"]
                created = sum(services.assign_departments(wave, departments) for wave in queryset)
                self.message_user(request, f"Assigned {created} employees from the selected departments.", level=messages.SUCCESS)
                return None
        else:
            form = DepartmentAssignForm()

        return render(
            request,
            "admin/waves/trainingwave/assign_by_department.html",
            context={
                "form": form,
                "waves": queryset,
                "action_name": "assign_by_department",
                "opts": self.model._meta,
            },
        )


@admin.register(WaveAssignment)
class WaveAssignmentAdmin(admin.ModelAdmin):
    """Плоский список назначений по всем волнам - основной вид для подсветки несдавших."""

    list_display = ("employee", "wave", "department_snapshot", "status_display", "best_score_display", "assigned_at")
    list_filter = ("wave", "department_snapshot", "wave__status")
    search_fields = ("employee__full_name", "employee__email")
    autocomplete_fields = ["employee", "wave"]

    @admin.display(description="Status")
    def status_display(self, obj):
        return status_badge(obj.status, obj.wave.is_overdue)

    @admin.display(description="Best score")
    def best_score_display(self, obj):
        best = obj.best_attempt
        return f"{best.score_percent}%" if best else "-"
