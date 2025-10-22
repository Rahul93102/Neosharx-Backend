#!/usr/bin/env python
"""
Create test data for comment system testing
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

def create_test_users():
    """Create test users for comment system"""
    print("Creating test users...")
    
    # Create regular test users
    try:
        user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            phone_number='+1234567890',
            first_name='Test',
            last_name='User1'
        )
        token1, created = Token.objects.get_or_create(user=user1)
        print(f"Created user: {user1.username} with token: {token1.key}")
    except Exception as e:
        try:
            user1 = CustomUser.objects.get(username='testuser1')
            token1, created = Token.objects.get_or_create(user=user1)
            print(f"User {user1.username} already exists with token: {token1.key}")
        except CustomUser.DoesNotExist:
            print(f"Error creating testuser1: {e}")
            return None, None, None
    
    try:
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            phone_number='+1234567891',
            first_name='Test',
            last_name='User2'
        )
        token2, created = Token.objects.get_or_create(user=user2)
        print(f"Created user: {user2.username} with token: {token2.key}")
    except Exception as e:
        try:
            user2 = CustomUser.objects.get(username='testuser2')
            token2, created = Token.objects.get_or_create(user=user2)
            print(f"User {user2.username} already exists with token: {token2.key}")
        except CustomUser.DoesNotExist:
            print(f"Error creating testuser2: {e}")
            return None, None, None
    
    # Create admin user
    try:
        admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            phone_number='+1234567892',
            first_name='Admin',
            last_name='User'
        )
        admin_token, created = Token.objects.get_or_create(user=admin_user)
        print(f"Created admin: {admin_user.username} with token: {admin_token.key}")
    except Exception as e:
        try:
            admin_user = CustomUser.objects.get(username='admin')
            admin_token, created = Token.objects.get_or_create(user=admin_user)
            print(f"Admin {admin_user.username} already exists with token: {admin_token.key}")
        except CustomUser.DoesNotExist:
            print(f"Error creating admin: {e}")
            return None, None, None
    
    return user1, user2, admin_user

def create_sample_comments():
    """Create sample comments for testing"""
    print("\nCreating sample comments...")
    
    # Get users
    user1 = CustomUser.objects.get(username='testuser1')
    user2 = CustomUser.objects.get(username='testuser2')
    
    # Get robotics news articles
    robotics_articles = RoboticsNews.objects.all()[:3]
    if not robotics_articles:
        print("No robotics articles found. Creating a sample article...")
        sample_article = RoboticsNews.objects.create(
            title="Sample Robotics Article for Testing",
            slug="sample-robotics-testing",
            excerpt="This is a sample article for testing the comment system.",
            content="This is a sample robotics article created for testing the comment system functionality.",
            is_published=True
        )
        robotics_articles = [sample_article]
    
    # Get content type for robotics news
    robotics_ct = ContentType.objects.get_for_model(RoboticsNews)
    
    comments_created = 0
    for article in robotics_articles:
        # Create main comments
        comment1 = Comment.objects.create(
            author=user1,
            content=f"Great article about {article.title}! Really insightful.",
            content_type=robotics_ct,
            object_id=article.id,
            is_approved=True
        )
        comments_created += 1
        
        comment2 = Comment.objects.create(
            author=user2,
            content=f"I learned a lot from this {article.title} article. Thanks for sharing!",
            content_type=robotics_ct,
            object_id=article.id,
            is_approved=True
        )
        comments_created += 1
        
        # Create reply to first comment
        reply1 = Comment.objects.create(
            author=user2,
            content="I totally agree! The insights are very valuable.",
            content_type=robotics_ct,
            object_id=article.id,
            parent=comment1,
            is_approved=True
        )
        comments_created += 1
        
        # Create reply to second comment
        reply2 = Comment.objects.create(
            author=user1,
            content="You're welcome! Glad you found it helpful.",
            content_type=robotics_ct,
            object_id=article.id,
            parent=comment2,
            is_approved=True
        )
        comments_created += 1
        
        print(f"Created comments for article: {article.title}")
    
    print(f"Total comments created: {comments_created}")

def print_test_credentials():
    """Print test credentials for easy access"""
    print("\n" + "="*50)
    print("TEST CREDENTIALS")
    print("="*50)
    
    for username in ['testuser1', 'testuser2', 'admin']:
        try:
            user = CustomUser.objects.get(username=username)
            token = Token.objects.get(user=user)
            password = 'testpass123' if username.startswith('test') else 'admin123'
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Token: {token.key}")
            print(f"Is Admin: {user.is_superuser}")
            print("-" * 30)
        except Exception as e:
            print(f"Error getting credentials for {username}: {e}")

if __name__ == '__main__':
    print("Setting up test data for comment system...")
    
    # Create test users
    create_test_users()
    
    # Create sample comments
    create_sample_comments()
    
    # Print credentials
    print_test_credentials()
    
    print("\nTest data setup complete!")
    print("You can now test the comment system with the credentials above.")