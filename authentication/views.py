from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from .models import CustomUser, OTPVerification, StartupStory, NeoStory, NeoProject, SharXathon, TechNews, TalkEpisode, RoboticsNews, Comment, CommentLike, Event
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    OTPRequestSerializer, 
    OTPVerificationSerializer,
    UserProfileSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ForgotUsernameSerializer,
    RecoverUsernameSerializer,
    StartupStorySerializer,
    NeoStorySerializer,
    NeoProjectSerializer,
    NeoProjectDetailSerializer,
    SharXathonSerializer,
    TechNewsSerializer,
    TalkEpisodeSerializer,
    RoboticsNewsSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CommentLikeSerializer,
    EventSerializer,
    EventListSerializer,
    EventCreateUpdateSerializer
)
from .services import TwilioService

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    User registration endpoint
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'token': token.key,
            'phone_verified': user.is_phone_verified
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    User login endpoint
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user_id': user.id,
            'token': token.key,
            'phone_verified': user.is_phone_verified
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    User logout endpoint
    """
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_otp(request):
    """
    Send OTP verification code to phone number
    """
    serializer = OTPRequestSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        
        # Send OTP using Twilio
        twilio_service = TwilioService()
        result = twilio_service.send_verification_code(phone_number)
        
        if result['success']:
            return Response({
                'message': 'OTP sent successfully',
                'phone_number': phone_number
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_otp(request):
    """
    Verify OTP code
    """
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp']
        
        # Verify OTP using Twilio
        twilio_service = TwilioService()
        result = twilio_service.verify_code(phone_number, otp_code)
        
        if result['success']:
            # Update user's phone verification status
            user = request.user
            user.phone_number = phone_number
            user.is_phone_verified = True
            user.save()
            
            return Response({
                'message': 'Phone number verified successfully',
                'phone_verified': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get user profile
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile
    """
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Send OTP for password reset
    """
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'No user found with this phone number'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Send OTP using Twilio
        twilio_service = TwilioService()
        result = twilio_service.send_verification_code(phone_number)
        
        if result['success']:
            return Response({
                'message': 'Password reset OTP sent successfully',
                'phone_number': phone_number
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Reset password with OTP verification
    """
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'No user found with this phone number'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verify OTP using Twilio
        twilio_service = TwilioService()
        result = twilio_service.verify_code(phone_number, otp_code)
        
        if result['success']:
            # Update user's password
            user.set_password(new_password)
            user.save()
            
            return Response({
                'message': 'Password reset successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_username(request):
    """
    Send username via OTP to registered phone number
    """
    serializer = ForgotUsernameSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'No user found with this phone number'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Send OTP using Twilio
        twilio_service = TwilioService()
        result = twilio_service.send_verification_code(phone_number)
        
        if result['success']:
            return Response({
                'message': 'Username recovery OTP sent successfully',
                'phone_number': phone_number
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def recover_username(request):
    """
    Recover username with OTP verification
    """
    serializer = RecoverUsernameSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp']
        
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'No user found with this phone number'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verify OTP using Twilio
        twilio_service = TwilioService()
        result = twilio_service.verify_code(phone_number, otp_code)
        
        if result['success']:
            return Response({
                'message': 'Username recovered successfully',
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LinkedIn OAuth Views
from .linkedin_service import LinkedInService

@api_view(['GET'])
@permission_classes([AllowAny])
def linkedin_login_url(request):
    """
    Get LinkedIn OAuth authorization URL
    """
    try:
        linkedin_service = LinkedInService()
        state = request.GET.get('state', 'default_state')
        # Add signup indicator to state if this is for signup
        flow_type = request.GET.get('flow', 'login')
        if flow_type == 'signup':
            state = f"signup_{state}"

        auth_url = linkedin_service.get_authorization_url(state)

        return Response({
            'authorization_url': auth_url,
            'state': state
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Failed to generate LinkedIn auth URL: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def linkedin_callback(request):
    """
    Handle LinkedIn OAuth callback and authenticate user
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        code = data.get('code')
        state = data.get('state')
        
        if not code:
            return JsonResponse({
                'error': 'Authorization code not provided'
            }, status=400)
        
        linkedin_service = LinkedInService()
        
        # Exchange code for tokens
        token_result = linkedin_service.exchange_code_for_tokens(code)
        if not token_result['success']:
            return JsonResponse({
                'error': token_result['error']
            }, status=400)
        
        access_token = token_result['access_token']
        id_token = token_result.get('id_token')
        
        # Get user info from LinkedIn
        user_info_result = linkedin_service.get_user_info(access_token)
        if not user_info_result['success']:
            return JsonResponse({
                'error': user_info_result['error']
            }, status=400)
        
        linkedin_data = user_info_result['data']
        
        # Create or get user
        user_result = linkedin_service.create_or_get_user(linkedin_data)
        if not user_result['success']:
            return JsonResponse({
                'error': user_result['error']
            }, status=400)
        
        user = user_result['user']
        token = user_result['token']
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'message': 'LinkedIn login successful',
            'token': token,
            'user': user_result['user_data']
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'error': f'LinkedIn authentication failed: {str(e)}'
        }, status=500)


# Google OAuth Views
from .google_service import GoogleService

@api_view(['GET'])
@permission_classes([AllowAny])
def google_login_url(request):
    """
    Get Google OAuth authorization URL
    """
    try:
        google_service = GoogleService()
        # Generate a secure random state for CSRF protection
        import secrets
        state = secrets.token_urlsafe(32)
        # Add signup indicator to state if this is for signup
        flow_type = request.GET.get('flow', 'login')
        if flow_type == 'signup':
            state = f"signup_{state}"

        auth_url = google_service.get_authorization_url(state)

        return Response({
            'authorization_url': auth_url,
            'state': state
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Failed to generate Google auth URL: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def google_callback(request):
    """
    Handle Google OAuth callback and authenticate user
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        code = data.get('code')
        state = data.get('state')
        
        if not code:
            return JsonResponse({
                'error': 'Authorization code not provided'
            }, status=400)
        
        google_service = GoogleService()
        
        # Exchange code for tokens
        token_result = google_service.exchange_code_for_tokens(code)
        if not token_result['success']:
            return JsonResponse({
                'error': token_result['error']
            }, status=400)
        
        access_token = token_result['access_token']
        id_token = token_result.get('id_token')
        
        # Get user info from Google
        user_info_result = google_service.get_user_info(access_token)
        if not user_info_result['success']:
            return JsonResponse({
                'error': user_info_result['error']
            }, status=400)
        
        google_data = user_info_result['data']
        
        # Create or get user
        user_result = google_service.create_or_get_user(google_data)
        if not user_result['success']:
            return JsonResponse({
                'error': user_result['error']
            }, status=400)
        
        user = user_result['user']
        token = user_result['token']
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'message': 'Google login successful',
            'token': token,
            'user': user_result['user_data']
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Google authentication failed: {str(e)}'
        }, status=500)


# ==================== Startup Stories API ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def list_startup_stories(request):
    """
    List all published startup stories with optional filtering
    """
    stories = StartupStory.objects.filter(is_published=True)
    
    # Filter by industry
    industry = request.GET.get('industry')
    if industry:
        stories = stories.filter(industry=industry)
    
    # Filter by stage
    stage = request.GET.get('stage')
    if stage:
        stories = stories.filter(stage=stage)
    
    # Filter featured stories
    featured = request.GET.get('featured')
    if featured == 'true':
        stories = stories.filter(is_featured=True)
    
    # Search by text
    search = request.GET.get('search')
    if search:
        stories = stories.filter(
            Q(heading__icontains=search) | 
            Q(summary__icontains=search) |
            Q(company_name__icontains=search) |
            Q(founder_name__icontains=search)
        )
    
    # Sort options
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', '-views_count', 'views_count', 'heading']
    if sort_by in valid_sorts:
        stories = stories.order_by(sort_by)
    
    serializer = StartupStorySerializer(stories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_startup_story(request, slug):
    """
    Get a single startup story by slug and increment views
    """
    try:
        story = StartupStory.objects.get(slug=slug, is_published=True)
        
        # Increment view count
        story.views_count += 1
        story.save(update_fields=['views_count'])
        
        serializer = StartupStorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except StartupStory.DoesNotExist:
        return Response({
            'error': 'Story not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_story(request):
    """
    Get the most recent featured story
    """
    try:
        story = StartupStory.objects.filter(is_published=True, is_featured=True).first()
        if not story:
            return Response({
                'error': 'No featured story available'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StartupStorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_story_filters(request):
    """
    Get available filter options for stories
    """
    industries = StartupStory.INDUSTRY_CHOICES
    stages = StartupStory.STAGE_CHOICES
    
    return Response({
        'industries': [{'value': i[0], 'label': i[1]} for i in industries],
        'stages': [{'value': s[0], 'label': s[1]} for s in stages]
    }, status=status.HTTP_200_OK)


# Neo Stories Views
@api_view(['GET'])
@permission_classes([AllowAny])
def list_neo_stories(request):
    """
    List all published Neo stories with optional filters
    """
    try:
        stories = NeoStory.objects.filter(is_published=True)
        
        # Apply filters
        category = request.GET.get('category', None)
        if category:
            stories = stories.filter(category=category)
        
        # Apply search
        search = request.GET.get('search', None)
        if search:
            stories = stories.filter(
                Q(header__icontains=search) |
                Q(introduction__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Apply sorting
        sort_by = request.GET.get('sort', 'recent')
        if sort_by == 'popular':
            stories = stories.order_by('-views_count', '-created_at')
        elif sort_by == 'oldest':
            stories = stories.order_by('created_at')
        else:  # recent
            stories = stories.order_by('-created_at')
        
        serializer = NeoStorySerializer(stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_neo_story(request, slug):
    """
    Get a single Neo story by slug and increment view count
    """
    try:
        story = NeoStory.objects.get(slug=slug, is_published=True)
        
        # Increment view count
        story.views_count += 1
        story.save(update_fields=['views_count'])
        
        serializer = NeoStorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except NeoStory.DoesNotExist:
        return Response(
            {'error': 'Neo story not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_neo_story(request):
    """
    Get the featured Neo story
    """
    try:
        story = NeoStory.objects.filter(is_published=True, is_featured=True).first()
        
        if not story:
            return Response(
                {'message': 'No featured Neo story available'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = NeoStorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_neo_story_filters(request):
    """
    Get available filter options for Neo stories
    """
    categories = NeoStory.CATEGORY_CHOICES
    
    return Response({
        'categories': [{'value': c[0], 'label': c[1]} for c in categories]
    }, status=status.HTTP_200_OK)


# Neo Projects Views
@api_view(['GET'])
@permission_classes([AllowAny])
def list_neo_projects(request):
    """
    List all published Neo projects with filters and search
    """
    try:
        projects = NeoProject.objects.filter(is_published=True)
        
        # Apply filters
        category = request.GET.get('category', None)
        if category:
            projects = projects.filter(category=category)
        
        status_filter = request.GET.get('status', None)
        if status_filter:
            projects = projects.filter(status=status_filter)
        
        difficulty = request.GET.get('difficulty', None)
        if difficulty:
            projects = projects.filter(difficulty_level=difficulty)
        
        is_open_source = request.GET.get('open_source', None)
        if is_open_source is not None:
            projects = projects.filter(is_open_source=is_open_source.lower() == 'true')
        
        # Apply search
        search = request.GET.get('search', None)
        if search:
            projects = projects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(technologies__icontains=search) |
                Q(tags__icontains=search) |
                Q(developer_name__icontains=search)
            )
        
        # Apply sorting
        sort_by = request.GET.get('sort', 'recent')
        if sort_by == 'popular':
            projects = projects.order_by('-views_count', '-stars_count', '-created_at')
        elif sort_by == 'stars':
            projects = projects.order_by('-stars_count', '-created_at')
        elif sort_by == 'oldest':
            projects = projects.order_by('created_at')
        else:  # recent
            projects = projects.order_by('-created_at')
        
        serializer = NeoProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_neo_project(request, slug):
    """
    Get a single Neo project by slug and increment view count
    """
    try:
        project = NeoProject.objects.get(slug=slug, is_published=True)
        
        # Increment view count
        project.views_count += 1
        project.save(update_fields=['views_count'])
        
        serializer = NeoProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except NeoProject.DoesNotExist:
        return Response(
            {'error': 'Neo project not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_neo_project_detail(request, slug):
    """
    Get a single Neo project by slug with full owner information
    """
    try:
        project = NeoProject.objects.get(slug=slug, is_published=True)
        
        # Increment view count
        project.views_count += 1
        project.save(update_fields=['views_count'])
        
        serializer = NeoProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except NeoProject.DoesNotExist:
        return Response(
            {'error': 'Neo project not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_neo_projects(request):
    """
    Get featured Neo projects
    """
    try:
        projects = NeoProject.objects.filter(is_published=True, is_featured=True).order_by('-created_at')
        serializer = NeoProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_neo_project_filters(request):
    """
    Get available filter options for Neo projects
    """
    categories = NeoProject.CATEGORY_CHOICES
    statuses = NeoProject.STATUS_CHOICES
    difficulties = NeoProject.DIFFICULTY_CHOICES
    
    return Response({
        'categories': [{'value': c[0], 'label': c[1]} for c in categories],
        'statuses': [{'value': s[0], 'label': s[1]} for s in statuses],
        'difficulties': [{'value': d[0], 'label': d[1]} for d in difficulties]
    }, status=status.HTTP_200_OK)


# SharXathon (Hackathon) Views
@api_view(['GET'])
@permission_classes([AllowAny])
def get_sharxathons(request):
    """
    Get list of hackathons with filtering and pagination
    """
    try:
        hackathons = SharXathon.objects.filter(is_published=True)
        
        # Filter by status
        status_filter = request.GET.get('status')
        if status_filter:
            hackathons = hackathons.filter(status=status_filter)
        
        # Filter by difficulty
        difficulty = request.GET.get('difficulty')
        if difficulty:
            hackathons = hackathons.filter(difficulty_level=difficulty)
        
        # Filter by team size
        team_size = request.GET.get('team_size')
        if team_size:
            hackathons = hackathons.filter(team_size=team_size)
        
        # Filter by location type
        is_virtual = request.GET.get('is_virtual')
        if is_virtual is not None:
            hackathons = hackathons.filter(is_virtual=is_virtual.lower() == 'true')
        
        # Search by name or topic
        search = request.GET.get('search')
        if search:
            hackathons = hackathons.filter(
                Q(name__icontains=search) | 
                Q(topic__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Order by start date
        hackathons = hackathons.order_by('-start_datetime')
        
        # Pagination
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 12))
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        total_count = hackathons.count()
        hackathons_page = hackathons[start_index:end_index]
        
        # Serialize data with countdown information
        serializer = SharXathonSerializer(hackathons_page, many=True)
        
        return Response({
            'hackathons': serializer.data,
            'pagination': {
                'current_page': page,
                'total_pages': (total_count + limit - 1) // limit,
                'total_count': total_count,
                'has_next': end_index < total_count,
                'has_previous': page > 1
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sharxathon_detail(request, slug):
    """
    Get detailed information about a specific hackathon
    """
    try:
        hackathon = SharXathon.objects.get(slug=slug, is_published=True)
        
        # Increment views count
        hackathon.views_count += 1
        hackathon.save(update_fields=['views_count'])
        
        serializer = SharXathonSerializer(hackathon)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except SharXathon.DoesNotExist:
        return Response(
            {'message': 'Hackathon not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_sharxathons(request):
    """
    Get featured hackathons for homepage
    """
    try:
        hackathons = SharXathon.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('-start_datetime')[:3]
        
        serializer = SharXathonSerializer(hackathons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_upcoming_sharxathons(request):
    """
    Get upcoming hackathons with registration still open
    """
    try:
        from django.utils import timezone as tz
        now = tz.now()
        
        hackathons = SharXathon.objects.filter(
            is_published=True,
            registration_deadline__gt=now,
            start_datetime__gt=now
        ).order_by('start_datetime')[:6]
        
        serializer = SharXathonSerializer(hackathons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sharxathon_filters(request):
    """
    Get available filter options for hackathons
    """
    return Response({
        'status_choices': [{'value': s[0], 'label': s[1]} for s in SharXathon.STATUS_CHOICES],
        'difficulty_choices': [{'value': d[0], 'label': d[1]} for d in SharXathon.DIFFICULTY_CHOICES],
        'team_size_choices': [{'value': t[0], 'label': t[1]} for t in SharXathon.TEAM_SIZE_CHOICES],
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sharxathon_countdown(request, slug):
    """
    Get real-time countdown information for a specific hackathon
    """
    try:
        hackathon = SharXathon.objects.get(slug=slug, is_published=True)
        
        from django.utils import timezone as tz
        now = tz.now()
        
        countdown_data = {
            'name': hackathon.name,
            'status': hackathon.status,
            'current_time': now.isoformat(),
            'registration_deadline': hackathon.registration_deadline.isoformat(),
            'start_datetime': hackathon.start_datetime.isoformat(),
            'end_datetime': hackathon.end_datetime.isoformat(),
            'is_registration_open': hackathon.is_registration_open,
            'is_active': hackathon.is_active,
        }
        
        # Calculate time remaining
        if hackathon.time_until_start:
            delta = hackathon.time_until_start
            countdown_data['time_until_start'] = {
                'days': delta.days,
                'hours': delta.seconds // 3600,
                'minutes': (delta.seconds % 3600) // 60,
                'seconds': delta.seconds % 60,
                'total_seconds': delta.total_seconds()
            }
        
        if hackathon.time_until_end:
            delta = hackathon.time_until_end
            countdown_data['time_until_end'] = {
                'days': delta.days,
                'hours': delta.seconds // 3600,
                'minutes': (delta.seconds % 3600) // 60,
                'seconds': delta.seconds % 60,
                'total_seconds': delta.total_seconds()
            }
        
        return Response(countdown_data, status=status.HTTP_200_OK)
        
    except SharXathon.DoesNotExist:
        return Response(
            {'message': 'Hackathon not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Tech News Views

@api_view(['GET'])
@permission_classes([AllowAny])
def get_tech_news(request):
    """
    Get list of tech news articles with filtering and pagination
    """
    try:
        # Get published articles only
        articles = TechNews.objects.filter(is_published=True)
        
        # Filter by category
        category = request.GET.get('category')
        if category:
            articles = articles.filter(category=category)
        
        # Filter by priority
        priority = request.GET.get('priority')
        if priority:
            articles = articles.filter(priority=priority)
        
        # Filter by tags
        tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__contains=[tag])
        
        # Search in title, subtitle, excerpt
        search = request.GET.get('search')
        if search:
            articles = articles.filter(
                Q(title__icontains=search) |
                Q(subtitle__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(content__icontains=search) |
                Q(author_name__icontains=search)
            )
        
        # Featured only
        featured_only = request.GET.get('featured')
        if featured_only == 'true':
            articles = articles.filter(is_featured=True)
        
        # Breaking only
        breaking_only = request.GET.get('breaking')
        if breaking_only == 'true':
            articles = articles.filter(is_breaking=True)
        
        # Trending only
        trending_only = request.GET.get('trending')
        if trending_only == 'true':
            articles = articles.filter(is_trending=True)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        start = (page - 1) * page_size
        end = start + page_size
        
        total_count = articles.count()
        articles = articles[start:end]
        
        serializer = TechNewsSerializer(articles, many=True)
        
        return Response({
            'articles': serializer.data,
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size,
                'has_next': end < total_count,
                'has_previous': page > 1
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_tech_news(request):
    """
    Get featured tech news articles
    """
    try:
        articles = TechNews.objects.filter(is_published=True, is_featured=True)[:6]
        serializer = TechNewsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_breaking_tech_news(request):
    """
    Get breaking tech news articles
    """
    try:
        articles = TechNews.objects.filter(is_published=True, is_breaking=True)[:5]
        serializer = TechNewsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_trending_tech_news(request):
    """
    Get trending tech news articles
    """
    try:
        articles = TechNews.objects.filter(is_published=True, is_trending=True)[:8]
        serializer = TechNewsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tech_news_categories(request):
    """
    Get available categories and their counts
    """
    try:
        from django.db.models import Count
        
        categories = []
        for value, label in TechNews.CATEGORY_CHOICES:
            count = TechNews.objects.filter(is_published=True, category=value).count()
            if count > 0:
                categories.append({
                    'value': value,
                    'label': label,
                    'count': count
                })
        
        return Response({
            'categories': categories,
            'priorities': [{'value': v, 'label': l} for v, l in TechNews.PRIORITY_CHOICES]
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tech_news_detail(request, slug):
    """
    Get detailed information about a specific tech news article
    """
    try:
        article = TechNews.objects.get(slug=slug, is_published=True)
        
        # Increment view count
        article.views_count += 1
        article.save(update_fields=['views_count'])
        
        serializer = TechNewsSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except TechNews.DoesNotExist:
        return Response(
            {'message': 'Article not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def like_tech_news(request, slug):
    """
    Like a tech news article
    """
    try:
        article = TechNews.objects.get(slug=slug, is_published=True)
        article.likes_count += 1
        article.save(update_fields=['likes_count'])
        
        return Response({
            'message': 'Article liked successfully',
            'likes_count': article.likes_count
        }, status=status.HTTP_200_OK)
        
    except TechNews.DoesNotExist:
        return Response(
            {'message': 'Article not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def share_tech_news(request, slug):
    """
    Share a tech news article (increments share count)
    """
    try:
        article = TechNews.objects.get(slug=slug, is_published=True)
        article.shares_count += 1
        article.save(update_fields=['shares_count'])
        
        return Response({
            'message': 'Article shared successfully',
            'shares_count': article.shares_count
        }, status=status.HTTP_200_OK)
        
    except TechNews.DoesNotExist:
        return Response(
            {'message': 'Article not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =============================================================================
# TALK EPISODES VIEWS
# =============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def talk_episodes_list(request):
    """
    List all published talk episodes with filtering and search
    """
    try:
        episodes = TalkEpisode.objects.filter(is_published=True)
        
        # Search by title, header, or description
        search = request.GET.get('search', '')
        if search:
            from django.db.models import Q
            episodes = episodes.filter(
                Q(title__icontains=search) |
                Q(header__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Order by episode number (descending - latest first)
        episodes = episodes.order_by('-episode_number')
        
        serializer = TalkEpisodeSerializer(episodes, many=True)
        
        return Response({
            'episodes': serializer.data,
            'count': episodes.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def talk_episode_detail(request, slug):
    """
    Get single talk episode by slug
    """
    try:
        episode = TalkEpisode.objects.get(slug=slug, is_published=True)
        serializer = TalkEpisodeSerializer(episode)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except TalkEpisode.DoesNotExist:
        return Response(
            {'message': 'Episode not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def talk_episode_by_number(request, episode_number):
    """
    Get single talk episode by episode number
    """
    try:
        episode = TalkEpisode.objects.get(
            episode_number=episode_number,
            is_published=True
        )
        serializer = TalkEpisodeSerializer(episode)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except TalkEpisode.DoesNotExist:
        return Response(
            {'message': 'Episode not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== ROBOTICS NEWS VIEWS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_robotics_news(request):
    """
    Get robotics news articles with filtering and search
    """
    try:
        articles = RoboticsNews.objects.filter(is_published=True)
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            articles = articles.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
        
        # Category filter
        category = request.GET.get('category', '')
        if category:
            articles = articles.filter(category=category)
        
        # Order by creation date (newest first)
        articles = articles.order_by('-created_at')
        
        # Pagination
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        total_count = articles.count()
        articles = articles[offset:offset + limit]
        
        serializer = RoboticsNewsSerializer(articles, many=True)
        
        return Response({
            'results': serializer.data,
            'count': total_count,
            'limit': limit,
            'offset': offset
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_robotics_news(request):
    """
    Get featured robotics news articles
    """
    try:
        articles = RoboticsNews.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('-created_at')
        
        limit = int(request.GET.get('limit', 1))
        articles = articles[:limit]
        
        serializer = RoboticsNewsSerializer(articles, many=True)
        
        return Response({
            'results': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_trending_robotics_news(request):
    """
    Get trending robotics news based on views and likes
    """
    try:
        articles = RoboticsNews.objects.filter(
            is_published=True
        ).order_by('-views_count', '-likes_count', '-created_at')
        
        limit = int(request.GET.get('limit', 4))
        articles = articles[:limit]
        
        serializer = RoboticsNewsSerializer(articles, many=True)
        
        return Response({
            'results': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_robotics_news_detail(request, slug):
    """
    Get single robotics news article by slug
    """
    try:
        article = RoboticsNews.objects.get(
            slug=slug,
            is_published=True
        )
        
        # Increment views count
        article.views_count += 1
        article.save(update_fields=['views_count'])
        
        serializer = RoboticsNewsSerializer(article)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except RoboticsNews.DoesNotExist:
        return Response(
            {'message': 'Article not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def like_robotics_news(request, slug):
    """
    Like/unlike a robotics news article
    """
    try:
        article = RoboticsNews.objects.get(
            slug=slug,
            is_published=True
        )
        
        # Simple increment (in real app, you'd track user likes)
        article.likes_count += 1
        article.save(update_fields=['likes_count'])
        
        return Response({
            'message': 'Article liked successfully',
            'likes_count': article.likes_count
        }, status=status.HTTP_200_OK)
        
    except RoboticsNews.DoesNotExist:
        return Response(
            {'message': 'Article not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def share_robotics_news(request, slug):
    """
    Share a robotics news article (increment share count)
    """
    try:
        article = RoboticsNews.objects.get(
            slug=slug,
            is_published=True
        )
        
        # Increment shares count
        article.shares_count += 1
        article.save(update_fields=['shares_count'])
        
        return Response({
            'message': 'Article shared successfully',
            'shares_count': article.shares_count
        }, status=status.HTTP_200_OK)
        
    except RoboticsNews.DoesNotExist:
        return Response(
            {'message': 'Article not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== COMMENT SYSTEM VIEWS ====================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # GET is open, but POST requires auth (checked in view)
def comments_list_create(request):
    """
    GET: List comments for specific content
    POST: Create new comment (requires authentication)
    """
    if request.method == 'GET':
        # Get comments for specific content
        content_type = request.GET.get('content_type')
        content_slug = request.GET.get('content_slug')
        
        if not content_type or not content_slug:
            return Response(
                {'error': 'content_type and content_slug are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get top-level comments (not replies)
            comments = Comment.objects.filter(
                content_type=content_type,
                content_slug=content_slug,
                parent__isnull=True,
                is_approved=True
            ).order_by('-created_at')
            
            # Pagination
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))
            total_count = comments.count()
            comments = comments[offset:offset + limit]
            
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            
            return Response({
                'results': serializer.data,
                'count': total_count,
                'limit': limit,
                'offset': offset
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        # Create new comment (requires authentication)
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required to post comments'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            serializer = CommentCreateSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                comment = serializer.save()
                
                # Return the created comment with full details
                response_serializer = CommentSerializer(comment, context={'request': request})
                
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id):
    """
    PUT: Update comment (only by owner)
    DELETE: Delete comment (by owner or admin)
    """
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {'message': 'Comment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'PUT':
        # Only comment owner can edit
        if comment.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            serializer = CommentCreateSerializer(comment, data=request.data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                updated_comment = serializer.save()
                response_serializer = CommentSerializer(updated_comment, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'DELETE':
        # Comment owner or admin can delete
        if comment.user != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            comment.delete()
            return Response(
                {'message': 'Comment deleted successfully'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_like_toggle(request):
    """
    Toggle like/dislike on a comment
    """
    try:
        comment_id = request.data.get('comment_id')
        reaction = request.data.get('reaction')  # 'like' or 'dislike'
        
        if not comment_id or reaction not in ['like', 'dislike']:
            return Response(
                {'error': 'comment_id and valid reaction (like/dislike) are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {'message': 'Comment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user already reacted
        try:
            existing_reaction = CommentLike.objects.get(user=request.user, comment=comment)
            
            if existing_reaction.reaction == reaction:
                # Remove reaction if same as existing
                existing_reaction.delete()
                action = 'removed'
            else:
                # Update reaction if different
                existing_reaction.reaction = reaction
                existing_reaction.save()
                action = 'updated'
                
        except CommentLike.DoesNotExist:
            # Create new reaction
            CommentLike.objects.create(
                user=request.user,
                comment=comment,
                reaction=reaction
            )
            action = 'added'
        
        # Update comment counts
        comment.likes_count = comment.reactions.filter(reaction='like').count()
        comment.dislikes_count = comment.reactions.filter(reaction='dislike').count()
        comment.save()
        
        return Response({
            'message': f'Reaction {action} successfully',
            'action': action,
            'likes_count': comment.likes_count,
            'dislikes_count': comment.dislikes_count,
            'user_reaction': reaction if action != 'removed' else None
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_flag(request, comment_id):
    """
    Flag a comment for moderation (admin only or report inappropriate content)
    """
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {'message': 'Comment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        reason = request.data.get('reason', 'Inappropriate content')
        
        # Only allow flagging if user is admin or it's not their own comment
        if comment.user == request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'You cannot flag your own comment'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment.is_flagged = True
        comment.flagged_reason = reason
        comment.save()
        
        return Response({
            'message': 'Comment flagged for review',
            'reason': reason
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_comments(request):
    """
    Get current user's comments across all content
    """
    try:
        comments = Comment.objects.filter(user=request.user).order_by('-created_at')
        
        # Pagination
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        total_count = comments.count()
        comments = comments[offset:offset + limit]
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        
        return Response({
            'results': serializer.data,
            'count': total_count,
            'limit': limit,
            'offset': offset
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Admin-only views for comment moderation
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_flagged_comments(request):
    """
    Get flagged comments for admin review
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        comments = Comment.objects.filter(is_flagged=True).order_by('-created_at')
        
        # Pagination
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        total_count = comments.count()
        comments = comments[offset:offset + limit]
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        
        return Response({
            'results': serializer.data,
            'count': total_count,
            'limit': limit,
            'offset': offset
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== EVENT ENDPOINTS ====================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def events_list_create(request):
    """
    GET: List all published events
    POST: Create new event (admin only)
    """
    from .models import Event
    from .serializers import EventListSerializer, EventCreateUpdateSerializer
    
    if request.method == 'GET':
        try:
            # Get query parameters
            event_type = request.GET.get('type')  # past, recent, upcoming
            category = request.GET.get('category')
            is_featured = request.GET.get('featured')
            
            # Base queryset - only published events
            events = Event.objects.filter(is_published=True)
            
            # Apply filters
            if event_type:
                events = events.filter(event_type=event_type)
            if category:
                events = events.filter(category=category)
            if is_featured == 'true':
                events = events.filter(is_featured=True)
            
            # Pagination
            limit = int(request.GET.get('limit', 20))
            offset = int(request.GET.get('offset', 0))
            total_count = events.count()
            events = events[offset:offset + limit]
            
            serializer = EventListSerializer(events, many=True)
            
            return Response({
                'results': serializer.data,
                'count': total_count,
                'limit': limit,
                'offset': offset
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        # Check if user is admin
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            serializer = EventCreateUpdateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                event = serializer.save()
                return Response(
                    EventListSerializer(event).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def events_by_type(request, event_type):
    """
    Get events by type (past, recent, upcoming)
    """
    from .models import Event
    from .serializers import EventListSerializer
    
    try:
        if event_type not in ['past', 'recent', 'upcoming']:
            return Response(
                {'error': 'Invalid event type. Must be: past, recent, or upcoming'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        events = Event.objects.filter(
            is_published=True,
            event_type=event_type
        ).order_by('display_order', '-event_date')
        
        # Pagination
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        total_count = events.count()
        events = events[offset:offset + limit]
        
        serializer = EventListSerializer(events, many=True)
        
        return Response({
            'results': serializer.data,
            'count': total_count,
            'limit': limit,
            'offset': offset,
            'event_type': event_type
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def event_detail(request, slug):
    """
    GET: Get event details by slug
    PUT: Update event (admin only)
    DELETE: Delete event (admin only)
    """
    from .models import Event
    from .serializers import EventSerializer, EventCreateUpdateSerializer
    
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        # Allow only published events for non-admin users
        if not event.is_published and not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
            return Response(
                {'error': 'Event not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Increment view count
        event.views_count += 1
        event.save(update_fields=['views_count'])
        
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        # Check if user is admin
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = EventCreateUpdateSerializer(event, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_event = serializer.save()
            return Response(
                EventSerializer(updated_event).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Check if user is admin
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        event.delete()
        return Response(
            {'message': 'Event deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def events_featured(request):
    """
    Get all featured events
    """
    from .models import Event
    from .serializers import EventListSerializer
    
    try:
        events = Event.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('display_order', '-event_date')
        
        serializer = EventListSerializer(events, many=True)
        
        return Response({
            'results': serializer.data,
            'count': events.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def events_categories(request):
    """
    Get all event categories with counts
    """
    from .models import Event
    from django.db.models import Count
    
    try:
        categories = Event.objects.filter(
            is_published=True
        ).values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'categories': list(categories)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== YOUTUBE VIDEOS API ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_videos_list(request):
    """
    Get all published YouTube videos/shorts
    Supports filtering by video_type, category, and featured status
    """
    from .models import YouTubeVideo
    
    try:
        # Get query parameters
        video_type = request.query_params.get('video_type', None)
        category = request.query_params.get('category', None)
        is_featured = request.query_params.get('featured', None)
        limit = request.query_params.get('limit', None)
        
        # Base queryset - only published videos
        videos = YouTubeVideo.objects.filter(is_published=True)
        
        # Apply filters
        if video_type:
            videos = videos.filter(video_type=video_type)
        
        if category:
            videos = videos.filter(category=category)
        
        if is_featured is not None:
            is_featured_bool = is_featured.lower() in ['true', '1', 'yes']
            videos = videos.filter(is_featured=is_featured_bool)
        
        # Order by display_order and created_at
        videos = videos.order_by('display_order', '-created_at')
        
        # Apply limit if specified
        if limit:
            try:
                limit = int(limit)
                videos = videos[:limit]
            except ValueError:
                pass
        
        # Serialize data
        videos_data = []
        for video in videos:
            videos_data.append({
                'id': video.id,
                'title': video.title,
                'description': video.description,
                'slug': video.slug,
                'youtube_url': video.youtube_url,
                'video_id': video.video_id,
                'embed_url': video.embed_url,
                'video_type': video.video_type,
                'category': video.category,
                'tags': video.tags,
                'thumbnail': video.thumbnail,
                'is_featured': video.is_featured,
                'autoplay': video.autoplay,
                'display_order': video.display_order,
                'duration': video.duration,
                'view_count': video.view_count,
                'internal_views': video.internal_views,
                'created_at': video.created_at.isoformat() if video.created_at else None,
                'watch_url': video.watch_url,
            })
        
        return Response({
            'count': len(videos_data),
            'videos': videos_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_video_detail(request, slug):
    """
    Get detailed information about a specific YouTube video
    Increments internal view count
    """
    from .models import YouTubeVideo
    
    try:
        video = YouTubeVideo.objects.get(slug=slug, is_published=True)
        
        # Increment internal views
        video.internal_views += 1
        video.save(update_fields=['internal_views'])
        
        video_data = {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'slug': video.slug,
            'youtube_url': video.youtube_url,
            'video_id': video.video_id,
            'embed_url': video.embed_url,
            'video_type': video.video_type,
            'category': video.category,
            'tags': video.tags,
            'thumbnail': video.thumbnail,
            'thumbnail_url': video.thumbnail_url,
            'auto_thumbnail': video.auto_thumbnail,
            'is_featured': video.is_featured,
            'autoplay': video.autoplay,
            'display_order': video.display_order,
            'duration': video.duration,
            'view_count': video.view_count,
            'like_count': video.like_count,
            'internal_views': video.internal_views,
            'published_date': video.published_date.isoformat() if video.published_date else None,
            'created_at': video.created_at.isoformat() if video.created_at else None,
            'updated_at': video.updated_at.isoformat() if video.updated_at else None,
            'watch_url': video.watch_url,
        }
        
        return Response(video_data, status=status.HTTP_200_OK)
        
    except YouTubeVideo.DoesNotExist:
        return Response(
            {'error': 'Video not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_videos_featured(request):
    """
    Get featured YouTube videos/shorts for homepage
    """
    from .models import YouTubeVideo
    
    try:
        videos = YouTubeVideo.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('display_order', '-created_at')
        
        videos_data = []
        for video in videos:
            videos_data.append({
                'id': video.id,
                'title': video.title,
                'description': video.description,
                'slug': video.slug,
                'video_id': video.video_id,
                'embed_url': video.embed_url,
                'video_type': video.video_type,
                'category': video.category,
                'thumbnail': video.thumbnail,
                'autoplay': video.autoplay,
                'duration': video.duration,
                'watch_url': video.watch_url,
            })
        
        return Response({
            'count': len(videos_data),
            'featured_videos': videos_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_videos_by_type(request, video_type):
    """
    Get YouTube videos filtered by type (video or short)
    """
    from .models import YouTubeVideo
    
    try:
        if video_type not in ['video', 'short']:
            return Response(
                {'error': 'Invalid video type. Use "video" or "short"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        videos = YouTubeVideo.objects.filter(
            is_published=True,
            video_type=video_type
        ).order_by('display_order', '-created_at')
        
        videos_data = []
        for video in videos:
            videos_data.append({
                'id': video.id,
                'title': video.title,
                'slug': video.slug,
                'video_id': video.video_id,
                'embed_url': video.embed_url,
                'category': video.category,
                'thumbnail': video.thumbnail,
                'autoplay': video.autoplay,
                'watch_url': video.watch_url,
            })
        
        return Response({
            'count': len(videos_data),
            'video_type': video_type,
            'videos': videos_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== USER PREFERENCES API ENDPOINT ====================

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def user_preferences(request):
    """
    Handle user preferences from signup
    POST: Create new user preference
    GET: List all user preferences (admin only)
    """
    from .models import UserPreference
    
    if request.method == 'POST':
        try:
            data = request.data
            
            # Validate required fields
            if not data.get('user_type') or not data.get('interest'):
                return Response(
                    {'error': 'user_type and interest are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create user preference
            preference = UserPreference.objects.create(
                user_type=data.get('user_type'),
                interest=data.get('interest'),
                email=data.get('email', ''),
                provider=data.get('provider', '')
            )
            
            return Response({
                'success': True,
                'message': 'User preferences saved successfully',
                'data': {
                    'id': preference.id,
                    'user_type': preference.user_type,
                    'interest': preference.interest,
                    'created_at': preference.created_at.isoformat()
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'GET':
        try:
            preferences = UserPreference.objects.all().order_by('-created_at')[:100]
            
            preferences_data = []
            for pref in preferences:
                preferences_data.append({
                    'id': pref.id,
                    'user_type': pref.user_type,
                    'interest': pref.interest,
                    'email': pref.email,
                    'provider': pref.provider,
                    'created_at': pref.created_at.isoformat()
                })
            
            return Response({
                'count': len(preferences_data),
                'preferences': preferences_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
