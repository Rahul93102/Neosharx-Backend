from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
import string

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.username or self.phone_number

class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))
    
    def __str__(self):
        return f"OTP for {self.phone_number} - {self.otp}"


class StartupStory(models.Model):
    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('ecommerce', 'E-Commerce'),
        ('ai_ml', 'AI/ML'),
        ('saas', 'SaaS'),
        ('other', 'Other'),
    ]
    
    STAGE_CHOICES = [
        ('idea', 'Idea'),
        ('pre_seed', 'Pre-Seed'),
        ('seed', 'Seed'),
        ('series_a', 'Series A'),
        ('series_b', 'Series B'),
        ('growth', 'Growth'),
        ('exit', 'Exit'),
    ]
    
    # Basic Information
    heading = models.CharField(max_length=255, help_text="Main title of the story")
    subheading = models.CharField(max_length=255, blank=True, help_text="Optional subtitle")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly version of title")
    
    # Story Content
    summary = models.TextField(help_text="Brief summary/excerpt (2-3 sentences)")
    content = models.TextField(help_text="Main story content (supports HTML)")
    
    # Additional Sections
    key_takeaways = models.TextField(help_text="Key lessons learned (one per line)")
    challenges_faced = models.TextField(blank=True, help_text="Challenges the startup faced")
    solutions_implemented = models.TextField(blank=True, help_text="How they solved the challenges")
    
    # Media
    featured_image = models.URLField(blank=True, help_text="URL for main story image")
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    additional_images = models.TextField(blank=True, help_text="Additional image URLs (one per line)")
    
    # Featured Screen
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='Featured screen configuration: {"url": "image/video URL", "type": "image/video", "is_featured": true/false}'
    )
    
    # Categorization
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='technology')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='seed')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    
    # Metadata
    founder_name = models.CharField(max_length=255, blank=True, help_text="Name of the founder(s)")
    company_name = models.CharField(max_length=255, help_text="Name of the startup")
    founded_year = models.IntegerField(blank=True, null=True)
    
    # Publishing
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as featured")
    is_published = models.BooleanField(default=False, help_text="Make visible to public")
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Author
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Startup Story"
        verbose_name_plural = "Startup Stories"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.heading
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.heading)
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)


class NeoStory(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('innovation', 'Innovation'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('leadership', 'Leadership'),
        ('culture', 'Culture'),
        ('social_impact', 'Social Impact'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    header = models.CharField(max_length=255, help_text="Main title of the Neo story")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly version of title")
    
    # Main Content
    main_image = models.URLField(help_text="URL for main story image")
    introduction = models.TextField(help_text="Brief introduction/excerpt (2-3 sentences)")
    
    # Story Sections (JSON format for flexibility)
    sections = models.JSONField(
        default=list,
        help_text="""
        JSON array of sections. Each section should have:
        {
            "subheading": "Section Title",
            "paragraph": "Section content text",
            "media_type": "image" or "video" or "none",
            "media_url": "URL to image or video",
            "media_caption": "Optional caption"
        }
        """
    )
    
    # Categorization
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='technology')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    
    # Metadata
    author_name = models.CharField(max_length=255, blank=True, help_text="Name of the author")
    read_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # Featured Screen (Single image or video)
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="""
        Featured screen object with format:
        {
            "url": "https://example.com/image.jpg or youtube.com/watch?v=...",
            "type": "image" or "video",
            "is_featured": true or false
        }
        """
    )
    
    # Publishing
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as featured")
    is_published = models.BooleanField(default=False, help_text="Make visible to public")
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Author
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Neo Story"
        verbose_name_plural = "Neo Stories"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.header
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.header)
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)


class SharXathon(models.Model):
    """
    Model for SharXathon (Hackathon) events with comprehensive details
    """
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    TEAM_SIZE_CHOICES = [
        ('individual', 'Individual'),
        ('2-3', '2-3 Members'),
        ('4-5', '4-5 Members'),
        ('6-8', '6-8 Members'),
        ('any', 'Any Size'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('registration_open', 'Registration Open'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255, help_text="Name of the hackathon")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(help_text="Brief description of the hackathon")
    content = models.TextField(help_text="Detailed content and information")
    
    # Location and Timing
    location = models.CharField(max_length=255, help_text="Physical or virtual location")
    is_virtual = models.BooleanField(default=False, help_text="Is this a virtual event?")
    start_datetime = models.DateTimeField(help_text="When the hackathon starts")
    end_datetime = models.DateTimeField(help_text="When the hackathon ends")
    registration_deadline = models.DateTimeField(help_text="Last date for registration")
    
    # Visual Content
    banner_image = models.URLField(blank=True, help_text="Main banner image URL")
    logo_image = models.URLField(blank=True, help_text="Event logo URL")
    gallery_images = models.JSONField(
        default=list,
        blank=True,
        help_text='JSON array of image URLs: ["url1", "url2", ...]'
    )
    
    # Featured Screen
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='Featured screen configuration: {"url": "image/video URL", "type": "image/video", "is_featured": true/false}'
    )
    
    # Hackathon Details
    topic = models.CharField(max_length=255, help_text="Main theme/topic of hackathon")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    team_size = models.CharField(max_length=20, choices=TEAM_SIZE_CHOICES, default='4-5')
    max_participants = models.IntegerField(default=100, help_text="Maximum number of participants")
    current_participants = models.IntegerField(default=0, help_text="Current registered participants")
    
    # Prizes and Benefits
    prizes = models.JSONField(
        default=list,
        help_text="""JSON array of prizes:
        [
            {
                "position": "1st Place",
                "prize": "$5000 + Mentorship",
                "description": "Winner gets cash prize and 3-month mentorship"
            }
        ]
        """
    )
    benefits = models.JSONField(
        default=list,
        help_text="""JSON array of benefits:
        [
            "Free meals and snacks",
            "Networking opportunities", 
            "Workshops and sessions",
            "Certificate of participation"
        ]
        """
    )
    
    # Rules and Requirements
    rules = models.JSONField(
        default=list,
        help_text="""JSON array of rules:
        [
            "Teams can have 2-5 members",
            "All code must be written during the event",
            "Use any programming language or framework",
            "Submit project by deadline"
        ]
        """
    )
    requirements = models.TextField(blank=True, help_text="Technical requirements and prerequisites")
    
    # Organizer Information
    organizer_name = models.CharField(max_length=255, default="NeoSharX Team")
    organizer_email = models.EmailField(blank=True, help_text="Contact email for queries")
    organizer_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    website_url = models.URLField(blank=True, help_text="Official event website")
    
    # Social and Registration
    registration_url = models.URLField(blank=True, help_text="External registration link")
    discord_url = models.URLField(blank=True, help_text="Discord server for participants")
    social_links = models.JSONField(
        default=dict,
        blank=True,
        help_text="""JSON object of social links:
        {
            "twitter": "https://twitter.com/event",
            "linkedin": "https://linkedin.com/event", 
            "instagram": "https://instagram.com/event"
        }
        """
    )
    
    # Judging Criteria
    judging_criteria = models.JSONField(
        default=list,
        help_text="""JSON array of judging criteria:
        [
            {
                "criteria": "Innovation",
                "weight": "30%",
                "description": "How innovative and creative is the solution?"
            }
        ]
        """
    )
    
    # Sponsors and Partners
    sponsors = models.JSONField(
        default=list,
        blank=True,
        help_text="""JSON array of sponsors:
        [
            {
                "name": "TechCorp",
                "logo": "https://example.com/logo.png",
                "tier": "Gold",
                "website": "https://techcorp.com"
            }
        ]
        """
    )
    
    # Event Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as featured")
    is_published = models.BooleanField(default=False, help_text="Make visible to public")
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Author/Creator
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "SharXathon"
        verbose_name_plural = "SharXathons"
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        # Auto-update status based on dates
        from django.utils import timezone as tz
        now = tz.now()
        
        if now < self.registration_deadline:
            if self.status == 'upcoming':
                self.status = 'registration_open'
        elif self.registration_deadline <= now < self.start_datetime:
            self.status = 'upcoming'
        elif self.start_datetime <= now < self.end_datetime:
            self.status = 'ongoing'
        elif now >= self.end_datetime:
            if self.status != 'cancelled':
                self.status = 'completed'
        
        super().save(*args, **kwargs)
    
    @property
    def time_until_start(self):
        """Get time remaining until hackathon starts"""
        from django.utils import timezone as tz
        if tz.now() < self.start_datetime:
            return self.start_datetime - tz.now()
        return None
    
    @property
    def time_until_end(self):
        """Get time remaining until hackathon ends"""
        from django.utils import timezone as tz
        if tz.now() < self.end_datetime:
            return self.end_datetime - tz.now()
        return None
    
    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        from django.utils import timezone as tz
        return tz.now() < self.registration_deadline and self.status in ['upcoming', 'registration_open']
    
    @property
    def is_active(self):
        """Check if hackathon is currently active/ongoing"""
        from django.utils import timezone as tz
        now = tz.now()
        return self.start_datetime <= now <= self.end_datetime
    
    @property
    def participation_percentage(self):
        """Get current participation as percentage of max"""
        if self.max_participants > 0:
            return min(100, (self.current_participants / self.max_participants) * 100)
        return 0


class TechNews(models.Model):
    """
    Model for What's Up Tech - Technology news articles
    """
    
    CATEGORY_CHOICES = [
        ('ai_ml', 'AI & Machine Learning'),
        ('blockchain', 'Blockchain & Crypto'),
        ('cloud', 'Cloud Computing'),
        ('cybersecurity', 'Cybersecurity'),
        ('mobile', 'Mobile Development'),
        ('web', 'Web Development'),
        ('iot', 'Internet of Things'),
        ('devops', 'DevOps'),
        ('data_science', 'Data Science'),
        ('quantum', 'Quantum Computing'),
        ('ar_vr', 'AR/VR'),
        ('5g', '5G & Networking'),
        ('startup', 'Startup News'),
        ('product_launch', 'Product Launch'),
        ('funding', 'Funding & Investment'),
        ('tech_policy', 'Tech Policy'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('breaking', 'Breaking News'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=300, help_text="Article headline")
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    subtitle = models.CharField(max_length=500, blank=True, help_text="Brief subtitle or tagline")
    excerpt = models.TextField(max_length=500, help_text="Short summary/excerpt (max 500 chars)")
    content = models.TextField(help_text="Full article content (supports HTML)")
    
    # Categorization
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Primary category"
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text='Tags as JSON array: ["tag1", "tag2", "tag3"]'
    )
    
    # Media
    featured_image = models.URLField(blank=True, help_text="Main article image URL")
    thumbnail_image = models.URLField(blank=True, help_text="Thumbnail image URL (for cards)")
    video_url = models.URLField(blank=True, help_text="Video URL (YouTube, Vimeo, etc.)")
    gallery_images = models.JSONField(
        default=list,
        blank=True,
        help_text='Additional images as JSON array: ["url1", "url2"]'
    )
    
    # Source & Attribution
    source_name = models.CharField(max_length=200, blank=True, help_text="Original source name")
    source_url = models.URLField(blank=True, help_text="Link to original article")
    author_name = models.CharField(max_length=200, blank=True, help_text="Article author")
    author_bio = models.TextField(blank=True, help_text="Author biography")
    author_avatar = models.URLField(blank=True, help_text="Author avatar image URL")
    
    # Metadata
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Article priority/importance"
    )
    read_time_minutes = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # Engagement
    views_count = models.IntegerField(default=0, help_text="Number of views")
    likes_count = models.IntegerField(default=0, help_text="Number of likes")
    shares_count = models.IntegerField(default=0, help_text="Number of shares")
    
    # Featured Screen
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='Featured screen configuration: {"url": "image/video URL", "type": "image/video", "is_featured": true/false}'
    )
    
    # Related Content
    related_links = models.JSONField(
        default=list,
        blank=True,
        help_text='Related links: [{"title": "Link", "url": "https://..."}]'
    )
    key_points = models.JSONField(
        default=list,
        blank=True,
        help_text='Key takeaways: ["Point 1", "Point 2", "Point 3"]'
    )
    
    # Publishing
    is_published = models.BooleanField(default=False, help_text="Publish this article?")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage?")
    is_breaking = models.BooleanField(default=False, help_text="Mark as breaking news?")
    is_trending = models.BooleanField(default=False, help_text="Mark as trending?")
    published_at = models.DateTimeField(null=True, blank=True, help_text="Publication date")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords (comma-separated)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tech News Article"
        verbose_name_plural = "Tech News Articles"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['is_published', '-published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_breaking']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while TechNews.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Set published_at timestamp
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/tech/{self.slug}/"
    
    @property
    def is_recent(self):
        """Check if article was published in last 24 hours"""
        if self.published_at:
            from django.utils import timezone as tz
            from datetime import timedelta
            return tz.now() - self.published_at < timedelta(hours=24)
        return False
    
    @property
    def engagement_score(self):
        """Calculate engagement score based on views, likes, shares"""
        return (self.views_count * 1) + (self.likes_count * 5) + (self.shares_count * 10)


class TalkEpisode(models.Model):
    """
    Model for NeoSharX Talks Episodes
    """
    
    # Basic Information
    episode_number = models.IntegerField(unique=True, help_text="Episode number (e.g., 1, 2, 3)")
    title = models.CharField(max_length=300, help_text="Episode title")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    header = models.CharField(max_length=500, help_text="Episode header/tagline")
    
    # Media
    youtube_url = models.URLField(help_text="YouTube video URL or embed URL")
    thumbnail_url = models.URLField(blank=True, null=True, help_text="Custom thumbnail URL")
    
    # Content
    description = models.TextField(help_text="Full episode description")
    key_takeaways = models.JSONField(
        default=list,
        help_text="List of key takeaways (e.g., ['Point 1', 'Point 2', 'Point 3'])"
    )
    
    # Featured Screen (single image or video)
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='Featured screen object: {"url": "https://...", "type": "image" or "video", "is_featured": true/false}'
    )
    
    # Speaker Information
    speaker_panels = models.JSONField(
        default=list,
        help_text="List of speaker objects with name, title, bio, avatar_url, social_links"
    )
    
    # Episode Metadata
    duration_minutes = models.IntegerField(default=60, help_text="Episode duration in minutes")
    published_at = models.DateTimeField(help_text="When the episode was published")
    
    # Status
    is_published = models.BooleanField(default=True, help_text="Is this episode published?")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-episode_number']
        verbose_name = 'Talk Episode'
        verbose_name_plural = 'Talk Episodes'
    
    def __str__(self):
        return f"Episode {self.episode_number}: {self.title}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(f"episode-{self.episode_number}-{self.title}")
            self.slug = base_slug
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/talks/{self.slug}/"
    
    @property
    def youtube_embed_url(self):
        """Convert YouTube URL to embed format"""
        if 'youtube.com/watch?v=' in self.youtube_url:
            video_id = self.youtube_url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in self.youtube_url:
            video_id = self.youtube_url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.youtube_url


class RoboticsNews(models.Model):
    CATEGORY_CHOICES = [
        ('ai_robotics', 'AI & Robotics'),
        ('industrial', 'Industrial Robotics'),
        ('medical', 'Medical Robotics'),
        ('autonomous', 'Autonomous Vehicles'),
        ('space', 'Space Robotics'),
        ('consumer', 'Consumer Robotics'),
        ('research', 'Research & Development'),
        ('entertainment', 'Entertainment Robotics'),
        ('military', 'Military & Defense'),
        ('agriculture', 'Agricultural Robotics'),
        ('manufacturing', 'Manufacturing'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    # Core Content
    title = models.CharField(max_length=255, help_text="Main headline")
    subtitle = models.CharField(max_length=255, blank=True, help_text="Optional subtitle")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly version")
    
    # Content
    summary = models.TextField(help_text="Brief article summary (2-3 sentences)")
    content = models.TextField(help_text="Full article content (supports HTML)")
    excerpt = models.TextField(blank=True, help_text="Short excerpt for previews")
    
    # Media
    featured_image = models.URLField(help_text="Main article image URL")
    additional_images = models.TextField(blank=True, help_text="Additional image URLs (one per line)")
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo video URL")
    
    # Categorization
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ai_robotics')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Source Information
    source_name = models.CharField(max_length=255, blank=True, help_text="Original source")
    source_url = models.URLField(blank=True, help_text="Link to original article")
    author_name = models.CharField(max_length=255, blank=True, help_text="Article author")
    
    # Technical Details
    robot_type = models.CharField(max_length=255, blank=True, help_text="Type of robot discussed")
    company_mentioned = models.CharField(max_length=255, blank=True, help_text="Companies mentioned")
    technology_focus = models.CharField(max_length=255, blank=True, help_text="Key technologies")
    
    # Featured Screen (Single image or video)
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="""
        Featured screen object with format:
        {
            "url": "https://example.com/image.jpg or youtube.com/watch?v=...",
            "type": "image" or "video",
            "is_featured": true or false
        }
        """
    )
    
    # Publishing
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    is_published = models.BooleanField(default=True, help_text="Visible to public")
    is_breaking = models.BooleanField(default=False, help_text="Breaking news priority")
    
    # Engagement Metrics (start at 0)
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Meta
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ], default='intermediate')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Robotics News Article"
        verbose_name_plural = "Robotics News Articles"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/robotics/{self.slug}/"
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def youtube_embed_url(self):
        """Convert YouTube URL to embed format"""
        if not self.video_url:
            return ""
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url


class Comment(models.Model):
    """Universal comment model for all content types"""
    
    CONTENT_TYPE_CHOICES = [
        ('startup_story', 'Startup Story'),
        ('neo_story', 'Neo Story'),
        ('neo_project', 'Neo Project'),
        ('tech_news', 'Tech News'),
        ('robotics_news', 'Robotics News'),
        ('talk_episode', 'Talk Episode'),
        ('sharxathon', 'SharXathon'),
    ]
    
    # Universal fields
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_slug = models.CharField(max_length=255, help_text="Slug of the content being commented on")
    
    # Comment content
    text = models.TextField(help_text="Comment text content")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Moderation and status
    is_approved = models.BooleanField(default=True, help_text="Whether comment is approved for display")
    is_flagged = models.BooleanField(default=False, help_text="Whether comment has been flagged for review")
    flagged_reason = models.CharField(max_length=255, blank=True, help_text="Reason for flagging")
    
    # Engagement
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'content_slug']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_type}: {self.content_slug}"
    
    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None
    
    @property
    def reply_count(self):
        """Get count of replies to this comment"""
        return self.replies.filter(is_approved=True).count()
    
    def get_content_title(self):
        """Get the title of the content this comment belongs to"""
        try:
            if self.content_type == 'startup_story':
                return StartupStory.objects.get(slug=self.content_slug).title
            elif self.content_type == 'neo_story':
                return NeoStory.objects.get(slug=self.content_slug).title
            elif self.content_type == 'neo_project':
                return NeoProject.objects.get(slug=self.content_slug).title
            elif self.content_type == 'tech_news':
                return TechNews.objects.get(slug=self.content_slug).headline
            elif self.content_type == 'robotics_news':
                return RoboticsNews.objects.get(slug=self.content_slug).title
            elif self.content_type == 'talk_episode':
                return TalkEpisode.objects.get(slug=self.content_slug).title
            elif self.content_type == 'sharxathon':
                return SharXathon.objects.get(slug=self.content_slug).title
        except:
            return "Unknown Content"
        return "Unknown Content"


class CommentLike(models.Model):
    """Track user likes/dislikes on comments"""
    
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'comment']  # One reaction per user per comment
    
    def __str__(self):
        return f"{self.user.username} {self.reaction}d comment {self.comment.id}"


class NeoProject(models.Model):
    """
    Model for Neo Projects - showcase of innovative projects and developments
    """
    
    CATEGORY_CHOICES = [
        ('web_development', 'Web Development'),
        ('mobile_app', 'Mobile App'),
        ('ai_ml', 'AI/ML'),
        ('blockchain', 'Blockchain'),
        ('iot', 'IoT'),
        ('robotics', 'Robotics'),
        ('data_science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('cloud_computing', 'Cloud Computing'),
        ('devops', 'DevOps'),
        ('game_development', 'Game Development'),
        ('ar_vr', 'AR/VR'),
        ('fintech', 'FinTech'),
        ('healthtech', 'HealthTech'),
        ('edtech', 'EdTech'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_development', 'In Development'),
        ('beta', 'Beta'),
        ('completed', 'Completed'),
        ('maintained', 'Maintained'),
        ('archived', 'Archived'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=255, help_text="Project title")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly version of title")
    description = models.TextField(help_text="Brief project description")
    detailed_description = models.TextField(blank=True, help_text="Detailed project description")
    
    # Media
    featured_image = models.URLField(blank=True, help_text="Main project image URL")
    demo_url = models.URLField(blank=True, help_text="Live demo URL")
    video_url = models.URLField(blank=True, help_text="Demo video URL")
    screenshots = models.JSONField(
        default=list,
        help_text="Array of screenshot URLs"
    )
    
    # Technical Details
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='web_development')
    technologies = models.CharField(max_length=500, help_text="Comma-separated list of technologies used")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_development')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    
    # Project Details
    features = models.JSONField(
        default=list,
        help_text="Array of key features"
    )
    installation_instructions = models.TextField(blank=True, help_text="How to install/setup the project")
    usage_instructions = models.TextField(blank=True, help_text="How to use the project")
    
    # Team & Attribution
    developer_name = models.CharField(max_length=255, blank=True, help_text="Main developer/team name")
    developer_email = models.EmailField(blank=True, help_text="Contact email")
    collaborators = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of collaborators")
    
    # Metadata
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for filtering")
    license = models.CharField(max_length=100, blank=True, help_text="Project license (e.g., MIT, GPL)")
    version = models.CharField(max_length=20, blank=True, help_text="Current version")
    
    # Featured Screen (Single image or video)
    featured_screen = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="""
        Featured screen object with format:
        {
            "url": "https://example.com/image.jpg or youtube.com/watch?v=...",
            "type": "image" or "video",
            "is_featured": true or false
        }
        """
    )
    
    # Publishing & Metrics
    is_featured = models.BooleanField(default=False, help_text="Show as featured project")
    is_published = models.BooleanField(default=False, help_text="Make visible to public")
    is_open_source = models.BooleanField(default=True, help_text="Is this an open source project?")
    views_count = models.IntegerField(default=0)
    stars_count = models.IntegerField(default=0, help_text="GitHub stars or similar rating")
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    project_start_date = models.DateField(blank=True, null=True, help_text="When the project was started")
    project_completion_date = models.DateField(blank=True, null=True, help_text="When the project was completed")
    
    # Relations
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Neo Project"
        verbose_name_plural = "Neo Projects"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def technology_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def collaborator_list(self):
        """Return collaborators as a list"""
        return [collab.strip() for collab in self.collaborators.split(',') if collab.strip()]


class Event(models.Model):
    """
    Model for Events displayed on the home page
    Supports past, recent, and upcoming events with slider functionality
    """
    
    EVENT_TYPE_CHOICES = [
        ('past', 'Past Event'),
        ('recent', 'Recent Event'),
        ('upcoming', 'Upcoming Event'),
    ]
    
    EVENT_CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('hackathon', 'Hackathon'),
        ('meetup', 'Meetup'),
        ('webinar', 'Webinar'),
        ('networking', 'Networking'),
        ('summit', 'Summit'),
        ('expo', 'Expo'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255, help_text="Event name/title")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(help_text="Brief description of the event")
    details = models.TextField(help_text="Detailed information about the event")
    
    # Event Classification
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='upcoming')
    category = models.CharField(max_length=50, choices=EVENT_CATEGORY_CHOICES, default='conference')
    
    # Location and Timing
    location = models.CharField(max_length=255, help_text="Event location or 'Virtual'")
    is_virtual = models.BooleanField(default=False)
    venue_details = models.TextField(blank=True, help_text="Detailed venue information")
    
    event_date = models.DateField(help_text="Event date")
    start_time = models.TimeField(null=True, blank=True, help_text="Event start time")
    end_time = models.TimeField(null=True, blank=True, help_text="Event end time")
    event_timezone = models.CharField(max_length=50, default='UTC', blank=True, help_text="Timezone (e.g., 'America/New_York', 'Asia/Kolkata')")
    
    # Visual Content
    featured_image = models.URLField(help_text="Main event image URL")
    thumbnail_image = models.URLField(blank=True, help_text="Thumbnail for cards/sliders")
    gallery_images = models.JSONField(
        default=list,
        blank=True,
        help_text='JSON array of image URLs for event gallery'
    )
    
    # Benefits and Features
    benefits = models.JSONField(
        default=list,
        help_text="""JSON array of event benefits:
        [
            "Networking opportunities",
            "Free meals and refreshments",
            "Certificate of attendance",
            "Workshop materials included"
        ]
        """
    )
    
    key_highlights = models.JSONField(
        default=list,
        blank=True,
        help_text="""JSON array of key highlights:
        [
            "Keynote by industry leaders",
            "Panel discussions",
            "Interactive workshops",
            "Product demos"
        ]
        """
    )
    
    # Speakers/Guests
    speakers = models.JSONField(
        default=list,
        blank=True,
        help_text="""JSON array of speakers:
        [
            {
                "name": "John Doe",
                "title": "CEO, TechCorp",
                "bio": "Expert in AI and ML",
                "photo": "https://example.com/photo.jpg"
            }
        ]
        """
    )
    
    # Registration and Participation
    registration_url = models.URLField(blank=True, help_text="External registration link")
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_registration_open = models.BooleanField(default=True)
    max_participants = models.IntegerField(default=0, help_text="0 means unlimited")
    current_participants = models.IntegerField(default=0)
    
    # Pricing
    is_free = models.BooleanField(default=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Ticket price in USD")
    early_bird_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    early_bird_deadline = models.DateTimeField(blank=True, null=True)
    
    # Organizer Information
    organizer_name = models.CharField(max_length=255, default="NeoSharX Team")
    organizer_email = models.EmailField(blank=True)
    organizer_phone = models.CharField(max_length=20, blank=True)
    organizer_website = models.URLField(blank=True)
    
    # Social Links
    event_website = models.URLField(blank=True, help_text="Official event website")
    social_links = models.JSONField(
        default=dict,
        blank=True,
        help_text="""JSON object of social links:
        {
            "twitter": "https://twitter.com/event",
            "linkedin": "https://linkedin.com/event",
            "facebook": "https://facebook.com/event",
            "instagram": "https://instagram.com/event"
        }
        """
    )
    
    # Sponsors and Partners
    sponsors = models.JSONField(
        default=list,
        blank=True,
        help_text="""JSON array of sponsors:
        [
            {
                "name": "TechCorp",
                "logo": "https://example.com/logo.png",
                "tier": "Gold",
                "website": "https://techcorp.com"
            }
        ]
        """
    )
    
    # Agenda/Schedule
    agenda = models.JSONField(
        default=list,
        blank=True,
        help_text="""JSON array of agenda items:
        [
            {
                "time": "09:00 AM",
                "title": "Registration & Breakfast",
                "description": "Check-in and networking",
                "speaker": ""
            }
        ]
        """
    )
    
    # Display Settings
    is_featured = models.BooleanField(default=False, help_text="Show as featured event")
    is_published = models.BooleanField(default=False, help_text="Make visible to public")
    display_order = models.IntegerField(default=0, help_text="Order in slider (lower number = first)")
    
    # Metadata
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Relations
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['display_order', '-event_date']
        indexes = [
            models.Index(fields=['event_type', 'is_published']),
            models.Index(fields=['event_date', 'is_featured']),
            models.Index(fields=['display_order']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.event_date}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def is_past_event(self):
        """Check if event date has passed"""
        from datetime import date
        return self.event_date < date.today()
    
    @property
    def is_today(self):
        """Check if event is today"""
        from datetime import date
        return self.event_date == date.today()
    
    @property
    def days_until_event(self):
        """Get number of days until event"""
        from datetime import date
        if self.event_date >= date.today():
            return (self.event_date - date.today()).days
        return None
    
    @property
    def formatted_date(self):
        """Get formatted date string"""
        return self.event_date.strftime("%B %d, %Y")
    
    @property
    def formatted_time(self):
        """Get formatted time range string"""
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class YouTubeVideo(models.Model):
    """
    Model for YouTube videos and shorts displayed on the home page
    Supports autoplay in uniform rectangular cards
    """
    
    VIDEO_TYPE_CHOICES = [
        ('video', 'YouTube Video'),
        ('short', 'YouTube Short'),
    ]
    
    CATEGORY_CHOICES = [
        ('tech_talks', 'Tech Talks'),
        ('tutorials', 'Tutorials'),
        ('startup_stories', 'Startup Stories'),
        ('hackathons', 'Hackathons'),
        ('events', 'Events'),
        ('interviews', 'Interviews'),
        ('demos', 'Product Demos'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=255, help_text="Video title")
    description = models.TextField(blank=True, help_text="Video description")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # YouTube Details
    youtube_url = models.URLField(help_text="Full YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID or https://youtube.com/shorts/SHORT_ID)")
    video_id = models.CharField(max_length=50, help_text="YouTube video ID (extracted from URL)")
    embed_url = models.URLField(blank=True, help_text="Auto-generated embed URL")
    
    # Classification
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPE_CHOICES, default='video')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='tech_talks')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    
    # Thumbnail
    thumbnail_url = models.URLField(blank=True, help_text="Custom thumbnail URL (if not using YouTube default)")
    auto_thumbnail = models.URLField(blank=True, help_text="Auto-fetched YouTube thumbnail")
    
    # Display Settings
    is_featured = models.BooleanField(default=False, help_text="Show prominently on homepage")
    is_published = models.BooleanField(default=False, help_text="Make visible to public")
    display_order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    autoplay = models.BooleanField(default=True, help_text="Enable autoplay on homepage")
    
    # Video Details (Optional - can be fetched from YouTube API)
    duration = models.CharField(max_length=20, blank=True, help_text="Video duration (e.g., '5:30')")
    view_count = models.IntegerField(default=0, help_text="YouTube view count")
    like_count = models.IntegerField(default=0, help_text="YouTube like count")
    
    # Metadata
    published_date = models.DateField(blank=True, null=True, help_text="Original YouTube publish date")
    internal_views = models.IntegerField(default=0, help_text="Views on our platform")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "YouTube Video"
        verbose_name_plural = "YouTube Videos"
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['video_type', 'is_published']),
            models.Index(fields=['category', 'is_featured']),
            models.Index(fields=['display_order']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.video_type})"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        
        # ALWAYS extract video ID from YouTube URL (overwrite any manual entry)
        if self.youtube_url:
            extracted_id = self.extract_video_id(self.youtube_url)
            if extracted_id:
                self.video_id = extracted_id
        
        # ALWAYS regenerate embed URL when video_id changes
        if self.video_id:
            if self.video_type == 'short':
                # YouTube Shorts embed
                self.embed_url = f"https://www.youtube.com/embed/{self.video_id}?autoplay=1&mute=1&loop=1&playlist={self.video_id}&controls=0&modestbranding=1"
            else:
                # Regular YouTube video embed
                self.embed_url = f"https://www.youtube.com/embed/{self.video_id}?autoplay=1&mute=1&loop=1&playlist={self.video_id}&controls=1&modestbranding=1"
        
        # Auto-generate YouTube thumbnail if not provided
        if self.video_id and not self.auto_thumbnail:
            self.auto_thumbnail = f"https://img.youtube.com/vi/{self.video_id}/maxresdefault.jpg"
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def extract_video_id(url):
        """Extract video ID from various YouTube URL formats"""
        import re
        
        # Pattern for regular videos: youtube.com/watch?v=VIDEO_ID
        pattern1 = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        # Pattern for shorts: youtube.com/shorts/VIDEO_ID
        pattern2 = r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})'
        # Pattern for embed URLs
        pattern3 = r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})'
        
        for pattern in [pattern1, pattern2, pattern3]:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return ""
    
    @property
    def thumbnail(self):
        """Get the best available thumbnail"""
        return self.thumbnail_url or self.auto_thumbnail or f"https://img.youtube.com/vi/{self.video_id}/hqdefault.jpg"
    
    @property
    def watch_url(self):
        """Get the standard YouTube watch URL"""
        if self.video_type == 'short':
            return f"https://www.youtube.com/shorts/{self.video_id}"
        return f"https://www.youtube.com/watch?v={self.video_id}"


class UserPreference(models.Model):
    """
    Model to store user preferences from signup
    """
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('working_professional', 'Working Professional'),
        ('tech_enthusiast', 'Tech Enthusiast'),
    ]
    
    INTEREST_CHOICES = [
        ('talks', 'Talks'),
        ('startups', 'Startups'),
        ('neo_stories', 'Neo Stories'),
        ('projects', 'Projects'),
        ('sharxathons', 'SharXathons'),
        ('robosharx', 'RoboSharX'),
        ('tech_news', 'Tech News'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='preferences')
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    email = models.EmailField(blank=True, null=True)
    provider = models.CharField(max_length=20, blank=True, null=True, help_text="google or linkedin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user_type} - {self.interest} ({self.created_at.strftime('%Y-%m-%d')})"
