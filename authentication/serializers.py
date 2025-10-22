from rest_framework import serializers
from django.contrib.auth import authenticate
from . import models
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'phone_number', 'password', 'confirm_password')
    
    def validate_phone_number(self, value):
        # Basic phone number validation
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = models.CustomUser.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include username and password.")

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    
    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be 6 digits.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'is_phone_verified', 'created_at')
        read_only_fields = ('id', 'created_at', 'is_phone_verified')

class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_phone_number(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
    
    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be 6 digits.")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

class ForgotUsernameSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

class RecoverUsernameSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    
    def validate_phone_number(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
    
    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be 6 digits.")
        return value

class StartupStorySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = models.StartupStory
        fields = [
            'id', 'heading', 'subheading', 'slug', 'summary', 'content',
            'key_takeaways', 'challenges_faced', 'solutions_implemented',
            'featured_image', 'video_url', 'additional_images', 'featured_screen',
            'industry', 'stage', 'tags', 'founder_name', 'company_name',
            'founded_year', 'is_featured', 'is_published', 'views_count',
            'created_at', 'updated_at', 'published_at', 'author_name'
        ]
        read_only_fields = ['id', 'views_count', 'created_at', 'updated_at', 'published_at', 'author_name']


class NeoStorySerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = models.NeoStory
        fields = [
            'id', 'header', 'slug', 'main_image', 'introduction', 'sections',
            'category', 'tags', 'author_name', 'read_time', 'featured_screen',
            'is_featured', 'is_published', 'views_count', 'created_at', 'updated_at',
            'published_at', 'author_username'
        ]
        read_only_fields = ['id', 'views_count', 'created_at', 'updated_at', 'published_at', 'author_username']


class SharXathonSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    time_until_start = serializers.SerializerMethodField()
    time_until_end = serializers.SerializerMethodField()
    participation_percentage = serializers.ReadOnlyField()
    is_registration_open = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = models.SharXathon
        fields = [
            'id', 'name', 'slug', 'description', 'content', 'location', 'is_virtual',
            'start_datetime', 'end_datetime', 'registration_deadline', 'banner_image',
            'logo_image', 'gallery_images', 'featured_screen', 'topic', 'difficulty_level', 'team_size',
            'max_participants', 'current_participants', 'prizes', 'benefits', 'rules',
            'requirements', 'organizer_name', 'organizer_email', 'organizer_phone',
            'website_url', 'registration_url', 'discord_url', 'social_links',
            'judging_criteria', 'sponsors', 'status', 'is_featured', 'is_published',
            'views_count', 'created_at', 'updated_at', 'published_at', 'created_by_username',
            'time_until_start', 'time_until_end', 'participation_percentage',
            'is_registration_open', 'is_active'
        ]
        read_only_fields = [
            'id', 'views_count', 'created_at', 'updated_at', 'published_at',
            'created_by_username', 'time_until_start', 'time_until_end',
            'participation_percentage', 'is_registration_open', 'is_active'
        ]
    
    def get_time_until_start(self, obj):
        """Get time remaining until hackathon starts in detailed format"""
        if obj.time_until_start:
            delta = obj.time_until_start
            return {
                'days': delta.days,
                'hours': delta.seconds // 3600,
                'minutes': (delta.seconds % 3600) // 60,
                'seconds': delta.seconds % 60,
                'total_seconds': int(delta.total_seconds())
            }
        return None
    
    def get_time_until_end(self, obj):
        """Get time remaining until hackathon ends in detailed format"""
        if obj.time_until_end:
            delta = obj.time_until_end
            return {
                'days': delta.days,
                'hours': delta.seconds // 3600,
                'minutes': (delta.seconds % 3600) // 60,
                'seconds': delta.seconds % 60,
                'total_seconds': int(delta.total_seconds())
            }
        return None


class TechNewsSerializer(serializers.ModelSerializer):
    engagement_score = serializers.ReadOnlyField()
    is_recent = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = models.TechNews
        fields = [
            'id', 'title', 'slug', 'subtitle', 'excerpt', 'content', 'category',
            'category_display', 'tags', 'featured_image', 'thumbnail_image', 
            'video_url', 'gallery_images', 'featured_screen', 'source_name', 'source_url', 
            'author_name', 'author_bio', 'author_avatar', 'priority', 
            'priority_display', 'read_time_minutes', 'views_count', 'likes_count',
            'shares_count', 'related_links', 'key_points', 'is_published',
            'is_featured', 'is_breaking', 'is_trending', 'published_at',
            'meta_description', 'meta_keywords', 'created_at', 'updated_at',
            'engagement_score', 'is_recent'
        ]
        read_only_fields = [
            'id', 'slug', 'views_count', 'likes_count', 'shares_count',
            'created_at', 'updated_at', 'engagement_score', 'is_recent',
            'category_display', 'priority_display'
        ]


class TalkEpisodeSerializer(serializers.ModelSerializer):
    youtube_embed_url = serializers.ReadOnlyField()
    
    class Meta:
        model = models.TalkEpisode
        fields = [
            'id',
            'episode_number',
            'title',
            'slug',
            'header',
            'youtube_url',
            'youtube_embed_url',
            'thumbnail_url',
            'description',
            'key_takeaways',
            'featured_screen',
            'speaker_panels',
            'duration_minutes',
            'published_at',
            'is_published',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'youtube_embed_url']


class RoboticsNewsSerializer(serializers.ModelSerializer):
    tag_list = serializers.ReadOnlyField()
    youtube_embed_url = serializers.ReadOnlyField()
    
    class Meta:
        model = models.RoboticsNews
        fields = [
            'id',
            'title',
            'subtitle',
            'slug',
            'summary',
            'content',
            'excerpt',
            'featured_image',
            'additional_images',
            'video_url',
            'youtube_embed_url',
            'category',
            'tags',
            'tag_list',
            'priority',
            'source_name',
            'source_url',
            'author_name',
            'robot_type',
            'company_mentioned',
            'technology_focus',
            'featured_screen',
            'is_featured',
            'is_published',
            'is_breaking',
            'views_count',
            'likes_count',
            'shares_count',
            'comments_count',
            'reading_time',
            'difficulty_level',
            'published_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['slug', 'views_count', 'likes_count', 'shares_count', 'comments_count', 'created_at', 'updated_at', 'published_at', 'youtube_embed_url', 'tag_list']


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    content_title = serializers.CharField(source='get_content_title', read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    is_reply = serializers.BooleanField(read_only=True)
    replies = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Comment
        fields = [
            'id',
            'user',
            'user_name',
            'user_email',
            'content_type',
            'content_slug',
            'text',
            'parent',
            'is_approved',
            'is_flagged',
            'flagged_reason',
            'likes_count',
            'dislikes_count',
            'created_at',
            'updated_at',
            'content_title',
            'reply_count',
            'is_reply',
            'replies',
            'user_reaction',
            'can_delete'
        ]
        read_only_fields = ['user', 'likes_count', 'dislikes_count', 'created_at', 'updated_at', 'is_approved']
    
    def get_replies(self, obj):
        """Get replies to this comment (only if not a reply itself)"""
        if obj.is_reply:
            return []
        
        replies = obj.replies.filter(is_approved=True).order_by('created_at')[:10]  # Limit replies
        return CommentSerializer(replies, many=True, context=self.context).data
    
    def get_user_reaction(self, obj):
        """Get current user's reaction to this comment"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                reaction = models.CommentLike.objects.get(user=request.user, comment=obj)
                return reaction.reaction
            except models.CommentLike.DoesNotExist:
                return None
        return None
    
    def get_can_delete(self, obj):
        """Check if current user can delete this comment"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # User can delete their own comments or admin can delete any
            return obj.user == request.user or request.user.is_staff or request.user.is_superuser
        return False
    
    def create(self, validated_data):
        # Set the user from the request
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating comments"""
    
    class Meta:
        model = models.Comment
        fields = ['content_type', 'content_slug', 'text', 'parent']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        fields = ['comment', 'reaction']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        
        # Update or create the reaction
        comment_like, created = models.CommentLike.objects.update_or_create(
            user=request.user,
            comment=validated_data['comment'],
            defaults={'reaction': validated_data['reaction']}
        )
        
        # Update comment counts
        comment = validated_data['comment']
        comment.likes_count = comment.reactions.filter(reaction='like').count()
        comment.dislikes_count = comment.reactions.filter(reaction='dislike').count()
        comment.save()
        
        return comment_like


class NeoProjectSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    technology_list = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    collaborator_list = serializers.ReadOnlyField()
    
    class Meta:
        model = models.NeoProject
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_description',
            'featured_image', 'demo_url', 'video_url', 'screenshots',
            'category', 'technologies', 'technology_list', 'github_url', 
            'status', 'difficulty_level', 'features', 'installation_instructions',
            'usage_instructions', 'developer_name', 'developer_email',
            'collaborators', 'collaborator_list', 'tags', 'tag_list',
            'license', 'version', 'featured_screen', 'is_featured', 'is_published', 'is_open_source',
            'views_count', 'stars_count', 'created_at', 'updated_at',
            'published_at', 'project_start_date', 'project_completion_date',
            'author_username'
        ]
        read_only_fields = [
            'id', 'views_count', 'created_at', 'updated_at', 'published_at',
            'author_username', 'technology_list', 'tag_list', 'collaborator_list'
        ]


class NeoProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for Neo project detail with full owner information"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    technology_list = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    collaborator_list = serializers.ReadOnlyField()
    
    # Owner information for frontend compatibility
    owner = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = models.NeoProject
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_description',
            'featured_image', 'demo_url', 'video_url', 'screenshots',
            'category', 'technologies', 'technology_list', 'github_url', 
            'status', 'difficulty_level', 'features', 'installation_instructions',
            'usage_instructions', 'developer_name', 'developer_email',
            'collaborators', 'collaborator_list', 'tags', 'tag_list',
            'license', 'version', 'featured_screen', 'is_featured', 'is_published', 'is_open_source',
            'views_count', 'stars_count', 'created_at', 'updated_at',
            'published_at', 'project_start_date', 'project_completion_date',
            'author_username', 'owner', 'links'
        ]
        read_only_fields = [
            'id', 'views_count', 'created_at', 'updated_at', 'published_at',
            'author_username', 'technology_list', 'tag_list', 'collaborator_list', 'owner', 'links'
        ]
    
    def get_owner(self, obj):
        """Return owner information in the format expected by frontend"""
        if obj.author:
            return {
                'id': obj.author.id,
                'name': obj.author.username,
                'username': obj.author.username,
                'email': obj.author.email,
                'title': getattr(obj.author, 'title', ''),
                'company': getattr(obj.author, 'company', ''),
                'bio': getattr(obj.author, 'bio', ''),
                'avatar': getattr(obj.author, 'avatar', None),
                'linkedin_url': getattr(obj.author, 'linkedin_url', ''),
                'github_url': getattr(obj.author, 'github_url', ''),
                'twitter_url': getattr(obj.author, 'twitter_url', ''),
                'website_url': getattr(obj.author, 'website_url', ''),
            }
        return None
    
    def get_links(self, obj):
        """Return additional links (empty for now, can be extended)"""
        return []


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model with all fields"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    is_past_event = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    days_until_event = serializers.ReadOnlyField()
    formatted_date = serializers.ReadOnlyField()
    formatted_time = serializers.ReadOnlyField()
    
    class Meta:
        model = models.Event
        fields = [
            'id', 'name', 'slug', 'description', 'details',
            'event_type', 'category', 'location', 'is_virtual', 'venue_details',
            'event_date', 'start_time', 'end_time', 'event_timezone',
            'featured_image', 'thumbnail_image', 'gallery_images',
            'benefits', 'key_highlights', 'speakers',
            'registration_url', 'registration_deadline', 'is_registration_open',
            'max_participants', 'current_participants',
            'is_free', 'ticket_price', 'early_bird_price', 'early_bird_deadline',
            'organizer_name', 'organizer_email', 'organizer_phone', 'organizer_website',
            'event_website', 'social_links', 'sponsors', 'agenda',
            'is_featured', 'is_published', 'display_order',
            'views_count', 'created_at', 'updated_at', 'published_at',
            'created_by_username', 'is_past_event', 'is_today', 
            'days_until_event', 'formatted_date', 'formatted_time'
        ]
        read_only_fields = [
            'id', 'slug', 'views_count', 'created_at', 'updated_at', 'published_at',
            'created_by_username', 'is_past_event', 'is_today', 
            'days_until_event', 'formatted_date', 'formatted_time'
        ]


class EventListSerializer(serializers.ModelSerializer):
    """Simplified serializer for event lists/cards"""
    formatted_date = serializers.ReadOnlyField()
    formatted_time = serializers.ReadOnlyField()
    days_until_event = serializers.ReadOnlyField()
    
    class Meta:
        model = models.Event
        fields = [
            'id', 'name', 'slug', 'description', 'event_type', 'category',
            'location', 'is_virtual', 'event_date', 'formatted_date', 'formatted_time',
            'featured_image', 'thumbnail_image', 'benefits', 'is_featured',
            'is_registration_open', 'max_participants', 'current_participants',
            'days_until_event', 'is_free', 'ticket_price'
        ]


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating events (admin only)"""
    
    class Meta:
        model = models.Event
        fields = [
            'name', 'description', 'details', 'event_type', 'category',
            'location', 'is_virtual', 'venue_details', 'event_date', 
            'start_time', 'end_time', 'event_timezone', 'featured_image', 
            'thumbnail_image', 'gallery_images', 'benefits', 'key_highlights',
            'speakers', 'registration_url', 'registration_deadline', 
            'is_registration_open', 'max_participants', 'is_free', 
            'ticket_price', 'early_bird_price', 'early_bird_deadline',
            'organizer_name', 'organizer_email', 'organizer_phone', 
            'organizer_website', 'event_website', 'social_links', 
            'sponsors', 'agenda', 'is_featured', 'is_published', 'display_order'
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
