#!/usr/bin/env python
"""
Simple test for comment system functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import CustomUser, Comment, RoboticsNews
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token

def test_comment_system():
    """Test the comment system with existing users"""
    print("Testing comment system functionality...")
    
    # Get existing users or create simple ones
    existing_admin = CustomUser.objects.filter(username='admin').first()
    if not existing_admin:
        print("No admin user found. Please create one first.")
        return
    
    # Create test users with unique phone numbers
    import time
    timestamp = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
    
    try:
        test_user = CustomUser.objects.create_user(
            username=f'commenter_{timestamp}',
            email=f'commenter_{timestamp}@test.com',
            password='test123',
            phone_number=f'+91{timestamp}0001',
            first_name='Test',
            last_name='Commenter'
        )
        test_token, created = Token.objects.get_or_create(user=test_user)
        print(f"Created test user: {test_user.username}")
        print(f"Login token: {test_token.key}")
    except Exception as e:
        print(f"Error creating test user: {e}")
        return
    
    # Get or create a robotics article
    robotics_article = RoboticsNews.objects.first()
    if not robotics_article:
        robotics_article = RoboticsNews.objects.create(
            title="Test Robotics Article for Comments",
            slug="test-robotics-comments",
            excerpt="This is a test article for the comment system.",
            content="This article is created specifically for testing the comment system functionality. Users can comment on this article to test the features.",
            is_published=True
        )
        print(f"Created test article: {robotics_article.title}")
    else:
        print(f"Using existing article: {robotics_article.title}")
    
    # Create test comments
    robotics_ct = ContentType.objects.get_for_model(RoboticsNews)
    
    # Main comment
    main_comment = Comment.objects.create(
        user=test_user,
        text="This is a test comment to verify the comment system is working properly!",
        content_type='robotics_news',
        content_slug=robotics_article.slug,
        is_approved=True
    )
    print(f"Created main comment: {main_comment.id}")
    
    # Reply comment
    reply_comment = Comment.objects.create(
        user=existing_admin,
        text="Thanks for testing the comment system! It looks like it's working well.",
        content_type='robotics_news',
        content_slug=robotics_article.slug,
        parent=main_comment,
        is_approved=True
    )
    print(f"Created reply comment: {reply_comment.id}")
    
    print("\n" + "="*60)
    print("COMMENT SYSTEM TEST SETUP COMPLETE")
    print("="*60)
    print(f"Test User: {test_user.username}")
    print(f"Password: test123")
    print(f"Token: {test_token.key}")
    print(f"Test Article: {robotics_article.title}")
    print(f"Article Slug: {robotics_article.slug}")
    print(f"Comments Created: 2 (1 main + 1 reply)")
    print("\nYou can now test the comment system by:")
    print("1. Starting the Django server")
    print("2. Opening the robotics article page")
    print("3. Logging in with the test user")
    print("4. Testing comment features (post, reply, like, etc.)")
    print("="*60)

if __name__ == '__main__':
    test_comment_system()