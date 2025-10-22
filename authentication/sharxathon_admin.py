"""
Django Admin configuration for SharXathon model
Add this to your main admin.py file
"""

from django.contrib import admin
from .models import SharXathon

@admin.register(SharXathon)
class SharXathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_datetime', 'status', 'current_participants', 'max_participants', 'is_featured', 'is_published', 'views_count')
    list_filter = ('status', 'difficulty_level', 'team_size', 'is_featured', 'is_published', 'is_virtual', 'start_datetime')
    search_fields = ('name', 'topic', 'location', 'organizer_name', 'description')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at', 'slug', 'time_until_start', 'time_until_end', 'participation_percentage')
    ordering = ('-start_datetime',)
    date_hierarchy = 'start_datetime'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'content', 'topic'),
            'description': 'Essential hackathon details'
        }),
        ('Location & Timing', {
            'fields': ('location', 'is_virtual', 'start_datetime', 'end_datetime', 'registration_deadline'),
            'description': 'When and where the hackathon happens'
        }),
        ('Visual Content', {
            'fields': ('banner_image', 'logo_image', 'gallery_images'),
            'classes': ('collapse',),
            'description': 'Images and visual assets. Gallery images should be JSON array: ["url1", "url2", ...]'
        }),
        ('Featured Screen', {
            'fields': ('featured_screen',),
            'description': '''
            Featured Screen Configuration (JSON format):
            {"url": "https://image-or-video-url.com", "type": "image", "is_featured": true}
            - url: Direct link to image or video
            - type: "image" or "video" 
            - is_featured: true to show in featured slider, false to hide
            '''
        }),
        ('Hackathon Settings', {
            'fields': ('difficulty_level', 'team_size', 'max_participants', 'current_participants', 'requirements'),
            'description': 'Technical requirements and participation limits'
        }),
        ('Prizes & Benefits', {
            'fields': ('prizes', 'benefits'),
            'description': '''
            Prizes JSON format: [{"position": "1st Place", "prize": "$5000", "description": "Winner details"}]
            Benefits JSON format: ["Free meals", "Networking", "Certificate"]
            '''
        }),
        ('Rules & Judging', {
            'fields': ('rules', 'judging_criteria'),
            'classes': ('collapse',),
            'description': '''
            Rules JSON format: ["Rule 1", "Rule 2", "Rule 3"]
            Judging JSON format: [{"criteria": "Innovation", "weight": "30%", "description": "Details"}]
            '''
        }),
        ('Organizer Details', {
            'fields': ('organizer_name', 'organizer_email', 'organizer_phone', 'website_url'),
            'classes': ('collapse',),
        }),
        ('Registration & Social', {
            'fields': ('registration_url', 'discord_url', 'social_links'),
            'classes': ('collapse',),
            'description': 'Social links JSON format: {"twitter": "url", "linkedin": "url", "instagram": "url"}'
        }),
        ('Sponsors', {
            'fields': ('sponsors',),
            'classes': ('collapse',),
            'description': 'Sponsors JSON format: [{"name": "Company", "logo": "url", "tier": "Gold", "website": "url"}]'
        }),
        ('Status & Publishing', {
            'fields': ('status', 'is_featured', 'is_published', 'views_count', 'published_at', 'created_by'),
        }),
        ('Analytics & Timing', {
            'fields': ('time_until_start', 'time_until_end', 'participation_percentage'),
            'classes': ('collapse',),
            'description': 'Read-only calculated fields'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by')
    
    def participation_status(self, obj):
        percentage = obj.participation_percentage
        return f"{obj.current_participants}/{obj.max_participants} ({percentage:.1f}%)"
    participation_status.short_description = "Participation"
    
    def time_status(self, obj):
        if obj.time_until_start:
            return f"Starts in {obj.time_until_start}"
        elif obj.time_until_end:
            return f"Ends in {obj.time_until_end}"
        else:
            return "Event completed"
    time_status.short_description = "Time Status"