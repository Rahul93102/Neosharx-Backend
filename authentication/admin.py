from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Import SharXathon admin configuration
from .sharxathon_admin import SharXathonAdmin

# Import TechNews admin configuration
from .technews_admin import TechNewsAdmin

# Import RoboticsNews admin configuration
from .robotics_admin import RoboticsNewsAdmin

@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_phone_verified', 'is_staff', 'created_at')
    list_filter = ('is_phone_verified', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Phone Information', {'fields': ('phone_number', 'is_phone_verified')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Phone Information', {'fields': ('phone_number',)}),
    )


@admin.register(models.StartupStory)
class StartupStoryAdmin(admin.ModelAdmin):
    list_display = ('heading', 'company_name', 'industry', 'stage', 'is_featured', 'is_published', 'views_count', 'created_at')
    list_filter = ('is_featured', 'is_published', 'industry', 'stage', 'created_at')
    search_fields = ('heading', 'company_name', 'founder_name', 'summary', 'content')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at', 'slug')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('heading', 'subheading', 'slug', 'company_name', 'founder_name', 'founded_year')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'key_takeaways', 'challenges_faced', 'solutions_implemented')
        }),
        ('Media', {
            'fields': ('featured_image', 'video_url', 'additional_images'),
            'classes': ('collapse',)
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
        ('Categorization', {
            'fields': ('industry', 'stage', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_featured', 'is_published', 'author', 'views_count', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.NeoStory)
class NeoStoryAdmin(admin.ModelAdmin):
    list_display = ('header', 'category', 'author_name', 'read_time', 'is_featured', 'is_published', 'views_count', 'created_at')
    list_filter = ('is_featured', 'is_published', 'category', 'created_at')
    search_fields = ('header', 'author_name', 'introduction', 'tags')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at', 'slug')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('header', 'slug', 'author_name', 'read_time')
        }),
        ('Main Content', {
            'fields': ('main_image', 'introduction')
        }),
        ('Featured Screen', {
            'fields': ('featured_screen',),
            'description': 'Add a single featured screen (image or video) as JSON object. Example: {"url": "https://example.com/image.jpg", "type": "image", "is_featured": true} or {"url": "https://youtube.com/watch?v=xyz", "type": "video", "is_featured": true}'
        }),
        ('Story Sections', {
            'fields': ('sections',),
            'description': 'Add sections as JSON array. Example: [{"subheading": "Title", "paragraph": "Content", "media_type": "image", "media_url": "https://...", "media_caption": "Caption"}]'
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_featured', 'is_published', 'author', 'views_count', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.TalkEpisode)
class TalkEpisodeAdmin(admin.ModelAdmin):
    list_display = ('episode_number', 'title', 'duration_minutes', 'is_published', 'published_at', 'created_at')
    list_filter = ('is_published', 'published_at', 'created_at')
    search_fields = ('title', 'header', 'description')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'youtube_embed_url')
    ordering = ('-episode_number',)
    
    fieldsets = (
        ('Episode Information', {
            'fields': ('episode_number', 'title', 'slug', 'header')
        }),
        ('Media', {
            'fields': ('youtube_url', 'youtube_embed_url', 'thumbnail_url', 'duration_minutes')
        }),
        ('Content', {
            'fields': ('description', 'key_takeaways'),
            'description': 'Key takeaways should be a JSON array: ["Takeaway 1", "Takeaway 2", "Takeaway 3"]'
        }),
        ('Featured Screen', {
            'fields': ('featured_screen',),
            'description': 'Add ONE featured screen as JSON object: {"url": "https://example.com/image.jpg", "type": "image", "is_featured": true} OR {"url": "https://youtube.com/watch?v=...", "type": "video", "is_featured": false}. Type must be either "image" or "video". Set is_featured to true to show in top slider.'
        }),
        ('Speaker Panels', {
            'fields': ('speaker_panels',),
            'description': 'Add speakers as JSON array. Example: [{"name": "John Doe", "title": "CEO", "bio": "Bio text", "avatar_url": "https://...", "social_links": {"linkedin": "url", "twitter": "url"}}]'
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(models.NeoProject)
class NeoProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'difficulty_level', 'is_featured', 'is_published', 'views_count', 'stars_count', 'created_at')
    list_filter = ('category', 'status', 'difficulty_level', 'is_featured', 'is_published', 'is_open_source', 'created_at')
    search_fields = ('title', 'description', 'developer_name', 'technologies', 'tags')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at', 'slug')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'detailed_description')
        }),
        ('Media & Demo', {
            'fields': ('featured_image', 'demo_url', 'video_url', 'screenshots'),
            'description': 'Screenshots should be a JSON array of URLs: ["url1", "url2", ...]'
        }),
        ('Featured Screen', {
            'fields': ('featured_screen',),
            'description': 'Add a single featured screen (image or video) as JSON object. Example: {"url": "https://example.com/image.jpg", "type": "image", "is_featured": true} or {"url": "https://youtube.com/watch?v=xyz", "type": "video", "is_featured": true}'
        }),
        ('Technical Details', {
            'fields': ('category', 'technologies', 'github_url', 'status', 'difficulty_level'),
            'description': 'Technologies should be comma-separated: "React, Node.js, MongoDB"'
        }),
        ('Project Information', {
            'fields': ('features', 'installation_instructions', 'usage_instructions'),
            'description': 'Features should be a JSON array: ["Feature 1", "Feature 2", ...]'
        }),
        ('Team & Attribution', {
            'fields': ('developer_name', 'developer_email', 'collaborators', 'author'),
            'description': 'Collaborators should be comma-separated: "John Doe, Jane Smith"'
        }),
        ('Metadata', {
            'fields': ('tags', 'license', 'version', 'project_start_date', 'project_completion_date'),
            'description': 'Tags should be comma-separated: "web, react, javascript"'
        }),
        ('Publishing & Metrics', {
            'fields': ('is_featured', 'is_published', 'is_open_source', 'views_count', 'stars_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')


# Register Event model if not already present
@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'category', 'event_date', 'location', 'is_featured', 'is_published', 'views_count', 'created_at')
    list_filter = ('event_type', 'category', 'is_featured', 'is_published', 'event_date')
    search_fields = ('name', 'description', 'location', 'organizer_name')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at')
    ordering = ('-event_date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'details', 'event_type', 'category')
        }),
        ('Timing & Location', {
            'fields': ('event_date', 'start_time', 'end_time', 'event_timezone', 'location', 'is_virtual', 'venue_details')
        }),
        ('Media & Content', {
            'fields': ('featured_image', 'thumbnail_image', 'gallery_images', 'benefits', 'key_highlights', 'agenda')
        }),
        ('Registration & Pricing', {
            'fields': ('registration_url', 'registration_deadline', 'is_registration_open', 'max_participants', 'current_participants', 'is_free', 'ticket_price', 'early_bird_price', 'early_bird_deadline')
        }),
        ('Organizer & Social', {
            'fields': ('organizer_name', 'organizer_email', 'organizer_phone', 'organizer_website', 'event_website', 'social_links', 'sponsors')
        }),
        ('Display & Metadata', {
            'fields': ('is_featured', 'is_published', 'display_order', 'views_count', 'created_by', 'created_at', 'updated_at', 'published_at')
        }),
    )

    prepopulated_fields = { 'slug': ('name',) }

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_type', 'category', 'is_featured', 'is_published', 'autoplay', 'display_order', 'internal_views', 'created_at')
    list_filter = ('video_type', 'category', 'is_featured', 'is_published', 'autoplay', 'created_at')
    search_fields = ('title', 'description', 'video_id', 'tags')
    readonly_fields = ('video_id', 'embed_url', 'auto_thumbnail', 'internal_views', 'created_at', 'updated_at')
    ordering = ('display_order', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'slug', 'video_type', 'category', 'tags')
        }),
        ('YouTube Details', {
            'fields': ('youtube_url', 'video_id', 'embed_url'),
            'description': '''
            Paste the full YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID or https://youtube.com/shorts/SHORT_ID)
            The video ID and embed URL will be automatically extracted.
            '''
        }),
        ('Thumbnail', {
            'fields': ('thumbnail_url', 'auto_thumbnail'),
            'description': 'Custom thumbnail is optional. YouTube thumbnail is auto-fetched.',
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_published', 'display_order', 'autoplay'),
            'description': '''
            - is_featured: Show prominently on homepage
            - is_published: Make visible to public
            - display_order: Lower numbers appear first
            - autoplay: Enable autoplay (muted) on homepage
            '''
        }),
        ('Video Metadata (Optional)', {
            'fields': ('duration', 'view_count', 'like_count', 'published_date'),
            'classes': ('collapse',),
            'description': 'These fields are optional and can be fetched from YouTube API'
        }),
        ('Analytics & Relations', {
            'fields': ('internal_views', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'interest', 'email', 'provider', 'created_at')
    list_filter = ('user_type', 'interest', 'provider', 'created_at')
    search_fields = ('email', 'user_type', 'interest')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'email', 'provider')
        }),
        ('Preferences', {
            'fields': ('user_type', 'interest')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
