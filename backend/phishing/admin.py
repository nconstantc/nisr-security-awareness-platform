from django.contrib import admin
from .models import PhishingTemplate, PhishingCampaign, PhishingResult, PhishingReport


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


@admin.register(PhishingReport)
class PhishingReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'subject', 'sender_email', 'status', 'reported_at')
    list_filter = ('status', 'reported_at')
    search_fields = ('employee__email', 'subject', 'sender_email')
    readonly_fields = ('employee', 'sender_email', 'subject', 'body_preview', 'reason', 'reported_at')
    actions = ['mark_as_phishing', 'mark_as_false_positive']
    
    def mark_as_phishing(self, request, queryset):
        queryset.update(status='confirmed_phishing', is_phishing=True)
    mark_as_phishing.short_description = "✅ Confirm as phishing"
    
    def mark_as_false_positive(self, request, queryset):
        queryset.update(status='false_positive', is_phishing=False)
    mark_as_false_positive.short_description = "❌ Mark as false positive"