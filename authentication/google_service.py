import requests
import jwt
import json
from urllib.parse import urlencode
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class GoogleService:
    """
    Service for handling Google OAuth 2.0 with OpenID Connect
    """
    
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
    
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scope = settings.GOOGLE_SCOPE
    
    def get_authorization_url(self, state=None):
        """
        Generate Google authorization URL for OAuth flow
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'state': state or 'default_state',
            'access_type': 'online',
            'prompt': 'select_account'
        }
        
        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
        logger.info(f"Generated Google auth URL: {auth_url}")
        return auth_url
    
    def exchange_code_for_tokens(self, code):
        """
        Exchange authorization code for access token and ID token
        """
        try:
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(self.TOKEN_URL, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            logger.info(f"Successfully obtained tokens from Google")
            return {
                'success': True,
                'access_token': token_data.get('access_token'),
                'id_token': token_data.get('id_token'),
                'expires_in': token_data.get('expires_in')
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Google token exchange failed: {str(e)}")
            return {
                'success': False,
                'error': f'Token exchange failed: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error during token exchange: {str(e)}")
            return {
                'success': False,
                'error': 'An unexpected error occurred'
            }
    
    def decode_id_token(self, id_token):
        """
        Decode Google ID token (JWT) without verification for development
        Note: In production, you should verify the JWT signature
        """
        try:
            # For development, we'll decode without verification
            # In production, implement proper JWT verification with Google's JWKS
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
            logger.info(f"Successfully decoded ID token")
            return {
                'success': True,
                'data': decoded_token
            }
        except Exception as e:
            logger.error(f"Failed to decode ID token: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to decode ID token: {str(e)}'
            }
    
    def get_user_info(self, access_token):
        """
        Get user information from Google userinfo endpoint
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(self.USERINFO_URL, headers=headers)
            response.raise_for_status()
            
            user_data = response.json()
            logger.info(f"Successfully retrieved user info from Google")
            return {
                'success': True,
                'data': user_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get Google user info: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get user info: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error getting user info: {str(e)}")
            return {
                'success': False,
                'error': 'An unexpected error occurred'
            }
    
    def create_or_get_user(self, google_data):
        """
        Create or get existing user based on Google data
        """
        try:
            email = google_data.get('email')
            google_id = google_data.get('id')
            
            if not email:
                return {
                    'success': False,
                    'error': 'Email not provided by Google'
                }
            
            # Try to find existing user by email
            try:
                user = User.objects.get(email=email)
                logger.info(f"Found existing user with email: {email}")
            except User.DoesNotExist:
                # Create new user
                username = email.split('@')[0]  # Use email prefix as username
                counter = 1
                original_username = username
                
                # Ensure username is unique
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                # Generate unique phone number for OAuth users (since Google doesn't provide phone)
                phone_number = None  # OAuth users don't have phone numbers
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=google_data.get('given_name', ''),
                    last_name=google_data.get('family_name', ''),
                    phone_number=phone_number  # None for OAuth users
                )
                logger.info(f"Created new OAuth user: {username}")
            
            # Create or get auth token
            token, created = Token.objects.get_or_create(user=user)
            
            return {
                'success': True,
                'user': user,
                'token': token.key,
                'user_data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'google_id': google_id,
                    'picture': google_data.get('picture', '')
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating/getting user: {str(e)}")
            return {
                'success': False,
                'error': f'User creation failed: {str(e)}'
            }
