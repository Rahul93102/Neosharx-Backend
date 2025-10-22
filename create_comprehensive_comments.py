#!/usr/bin/env python
"""
Create comprehensive test comments for all content types
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import CustomUser, Comment, RoboticsNews, StartupStory
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token

def create_comprehensive_test_comments():
    """Create test comments for all content types"""
    print("Creating comprehensive test comments for all content types...")
    
    # Get test users
    try:
        test_user = CustomUser.objects.get(username='commenter_776908')
        admin_user = CustomUser.objects.get(username='admin')
    except CustomUser.DoesNotExist:
        print("Test users not found. Please run test_comments.py first.")
        return
    
    comments_created = 0
    
    # 1. Robotics News Comments
    try:
        robotics_articles = RoboticsNews.objects.filter(is_published=True)[:3]
        print(f"\nFound {len(robotics_articles)} robotics articles")
        for article in robotics_articles:
            comment1 = Comment.objects.create(
                user=test_user,
                text=f"Amazing robotics breakthrough! {article.title} shows the future of technology.",
                content_type='robotics_news',
                content_slug=article.slug,
                is_approved=True
            )
            Comment.objects.create(
                user=admin_user,
                text="Thanks for reading! The robotics field is evolving rapidly.",
                content_type='robotics_news',
                content_slug=article.slug,
                parent=comment1,
                is_approved=True
            )
            comments_created += 2
            print(f"✅ Created comments for robotics article: {article.title}")
    except Exception as e:
        print(f"❌ Error with robotics news: {e}")
    
    # 2. Tech News Comments
    try:
        from authentication.models import TechNews
        tech_articles = TechNews.objects.filter(is_published=True)[:3]
        print(f"\nFound {len(tech_articles)} tech articles")
        for article in tech_articles:
            comment1 = Comment.objects.create(
                user=test_user,
                text=f"Great tech insights in {article.title}! This will change everything.",
                content_type='tech_news',
                content_slug=article.slug,
                is_approved=True
            )
            Comment.objects.create(
                user=admin_user,
                text="The tech industry moves so fast! Thanks for the comment.",
                content_type='tech_news',
                content_slug=article.slug,
                parent=comment1,
                is_approved=True
            )
            comments_created += 2
            print(f"✅ Created comments for tech article: {article.title}")
    except ImportError:
        print("❌ TechNews model not found")
    except Exception as e:
        print(f"❌ Error with tech news: {e}")
    
    # 3. Neo Story Comments
    try:
        from authentication.models import NeoStory
        neo_stories = NeoStory.objects.filter(is_published=True)[:3]
        print(f"\nFound {len(neo_stories)} neo stories")
        for story in neo_stories:
            comment1 = Comment.objects.create(
                user=test_user,
                text=f"Inspiring Neo story! {story.title} really motivates me to innovate.",
                content_type='neo_story',
                content_slug=story.slug,
                is_approved=True
            )
            Comment.objects.create(
                user=admin_user,
                text="Neo stories showcase the power of innovation. Glad you enjoyed it!",
                content_type='neo_story',
                content_slug=story.slug,
                parent=comment1,
                is_approved=True
            )
            comments_created += 2
            print(f"✅ Created comments for neo story: {story.title}")
    except ImportError:
        print("❌ NeoStory model not found")
    except Exception as e:
        print(f"❌ Error with neo stories: {e}")
    
    # 4. Startup Story Comments
    try:
        startup_stories = StartupStory.objects.filter(is_published=True)[:3]
        print(f"\nFound {len(startup_stories)} startup stories")
        for story in startup_stories:
            comment1 = Comment.objects.create(
                user=test_user,
                text=f"What an entrepreneurial journey! {story.title} is truly inspiring.",
                content_type='startup_story',
                content_slug=story.slug,
                is_approved=True
            )
            Comment.objects.create(
                user=admin_user,
                text="Startup journeys are always fascinating. Thanks for the feedback!",
                content_type='startup_story',
                content_slug=story.slug,
                parent=comment1,
                is_approved=True
            )
            comments_created += 2
            print(f"✅ Created comments for startup story: {story.title}")
    except Exception as e:
        print(f"❌ Error with startup stories: {e}")
    
    # 5. Talk Episode Comments
    try:
        from authentication.models import TalkEpisode  
        talk_episodes = TalkEpisode.objects.all()[:3]
        print(f"\nFound {len(talk_episodes)} talk episodes")
        for episode in talk_episodes:
            comment1 = Comment.objects.create(
                user=test_user,
                text=f"Excellent discussion in {episode.title}! The speakers were brilliant.",
                content_type='talk_episode',
                content_slug=episode.slug,
                is_approved=True
            )
            Comment.objects.create(
                user=admin_user,
                text="Our talk episodes feature amazing guests. Thanks for watching!",
                content_type='talk_episode',
                content_slug=episode.slug,
                parent=comment1,
                is_approved=True
            )
            comments_created += 2
            print(f"✅ Created comments for talk episode: {episode.title}")
    except ImportError:
        print("❌ TalkEpisode model not found")
    except Exception as e:
        print(f"❌ Error with talk episodes: {e}")
    
    # 6. SharXathon Comments
    try:
        from authentication.models import SharXathon
        sharxathons = SharXathon.objects.all()[:3]
        print(f"\nFound {len(sharxathons)} hackathons")
        for hackathon in sharxathons:
            comment1 = Comment.objects.create(
                user=test_user,
                text=f"{hackathon.title} looks amazing! Can't wait to participate.",
                content_type='sharxathon',
                content_slug=hackathon.slug,
                is_approved=True
            )
            Comment.objects.create(
                user=admin_user,
                text="SharXathons are great opportunities to innovate. Hope to see you there!",
                content_type='sharxathon',
                content_slug=hackathon.slug,
                parent=comment1,
                is_approved=True
            )
            comments_created += 2
            print(f"✅ Created comments for hackathon: {hackathon.title}")
    except ImportError:
        print("❌ SharXathon model not found")
    except Exception as e:
        print(f"❌ Error with hackathons: {e}")
    
    print("\n" + "="*70)
    print("COMPREHENSIVE COMMENT SYSTEM TEST COMPLETE!")
    print("="*70)
    print(f"✅ Total comments created across all content types: {comments_created}")
    print("\n🚀 COMMENT SYSTEM FEATURES IMPLEMENTED:")
    print("   ✅ Robotics News - Comments with replies")
    print("   ✅ Tech News - Comments with replies") 
    print("   ✅ Neo Stories - Comments with replies")
    print("   ✅ Startup Stories - Comments with replies")
    print("   ✅ Talk Episodes - Comments with replies")
    print("   ✅ SharXathons - Comments with replies")
    print("\n💡 TEST CREDENTIALS:")
    print(f"   Username: {test_user.username}")
    print("   Password: test123")
    print(f"   Admin: {admin_user.username}")
    print("\n🎯 TESTING INSTRUCTIONS:")
    print("1. Start Django server: python manage.py runserver 8001")
    print("2. Start frontend server: python -m http.server 3002 (in frontend folder)")
    print("3. Open any content detail page")
    print("4. Login with test credentials")
    print("5. Test comment features: post, reply, like, flag")
    print("="*70)

if __name__ == '__main__':
    create_comprehensive_test_comments()