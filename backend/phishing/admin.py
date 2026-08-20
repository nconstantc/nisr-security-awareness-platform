from django.contrib import admin
from .models import PhishingTemplate, PhishingCampaign, PhishingResult


@admin.register(PhishingTemplate)
class PhishingTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'sender_name', 'is_active', 'created_at')
    search_fields = ('name', 'subject', 'sender_name')
    list_filter = ('is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('name', 'subject', 'body')}),
        ('Sender Information', {'fields': ('sender_name', 'sender_email')}),
        ('Landing Page', {'fields': ('landing_page_url',)}),
        ('Status', {'fields': ('is_active',)}),
    )


@admin.register(PhishingCampaign)
class PhishingCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'status', 'start_date', 'end_date', 'created_at')
    search_fields = ('name',)
    list_filter = ('status', 'departments', 'created_at')
    filter_horizontal = ('departments',)
    fieldsets = (
        (None, {'fields': ('name', 'template', 'course')}),
        ('Target Audience', {'fields': ('departments',)}),
        ('Schedule', {'fields': ('start_date', 'end_date')}),
        ('Status', {'fields': ('status',)}),
    )


@admin.register(PhishingResult)
class PhishingResultAdmin(admin.ModelAdmin):
    list_display = ('employee', 'campaign', 'status', 'opened_at', 'clicked_at', 'reported_at')
    search_fields = ('employee__email', 'campaign__name')
    list_filter = ('status', 'campaign')
    readonly_fields = ('opened_at', 'clicked_at', 'submitted_at', 'reported_at')