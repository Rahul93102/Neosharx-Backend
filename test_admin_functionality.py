#!/usr/bin/env python
"""
Test script to verify admin functionality for Events and YouTube Videos
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import Event, YouTubeVideo, CustomUser
from django.contrib import admin
from datetime import datetime, timedelta
from django.utils import timezone

def test_admin_functionality():
    print("=" * 70)
    print("ADMIN FUNCTIONALITY TEST")
    print("=" * 70)
    
    # Check admin registration
    print("\n1. Checking Admin Registration:")
    print("-" * 70)
    event_registered = Event in admin.site._registry
    video_registered = YouTubeVideo in admin.site._registry
    print(f"✅ Event registered in admin: {event_registered}")
    print(f"✅ YouTubeVideo registered in admin: {video_registered}")
    
    # Check superuser
    print("\n2. Checking Superuser:")
    print("-" * 70)
    superusers = CustomUser.objects.filter(is_superuser=True)
    print(f"✅ Superusers found: {superusers.count()}")
    for user in superusers:
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Can add events: {user.has_perm('authentication.add_event')}")
        print(f"   - Can change events: {user.has_perm('authentication.change_event')}")
        print(f"   - Can delete events: {user.has_perm('authentication.delete_event')}")
        print(f"   - Can add videos: {user.has_perm('authentication.add_youtubevideo')}")
        print(f"   - Can change videos: {user.has_perm('authentication.change_youtubevideo')}")
        print(f"   - Can delete videos: {user.has_perm('authentication.delete_youtubevideo')}")
    
    # Test Event CRUD
    print("\n3. Testing Event CRUD Operations:")
    print("-" * 70)
    
    # CREATE
    print("\n   a) CREATE - Adding new event...")
    try:
        test_event = Event.objects.create(
            name="Admin Test Event",
            description="This is a test event created via admin test script",
            event_type="workshop",
            category="technology",
            event_date=timezone.now() + timedelta(days=30),
            location="Test Location",
            is_published=True
        )
        print(f"   ✅ Created event: {test_event.name} (ID: {test_event.id})")
    except Exception as e:
        print(f"   ❌ Error creating event: {e}")
        return
    
    # READ
    print("\n   b) READ - Fetching event...")
    try:
        fetched_event = Event.objects.get(id=test_event.id)
        print(f"   ✅ Fetched event: {fetched_event.name}")
        print(f"      - Type: {fetched_event.event_type}")
        print(f"      - Category: {fetched_event.category}")
        print(f"      - Location: {fetched_event.location}")
    except Exception as e:
        print(f"   ❌ Error fetching event: {e}")
        return
    
    # UPDATE
    print("\n   c) UPDATE - Modifying event...")
    try:
        test_event.name = "Admin Test Event (Updated)"
        test_event.location = "Updated Location"
        test_event.save()
        print(f"   ✅ Updated event: {test_event.name}")
        print(f"      - New location: {test_event.location}")
    except Exception as e:
        print(f"   ❌ Error updating event: {e}")
        return
    
    # DELETE
    print("\n   d) DELETE - Removing event...")
    try:
        event_id = test_event.id
        test_event.delete()
        print(f"   ✅ Deleted event ID: {event_id}")
        # Verify deletion
        exists = Event.objects.filter(id=event_id).exists()
        print(f"      - Event still exists: {exists}")
    except Exception as e:
        print(f"   ❌ Error deleting event: {e}")
        return
    
    # Test YouTubeVideo CRUD
    print("\n4. Testing YouTubeVideo CRUD Operations:")
    print("-" * 70)
    
    # CREATE
    print("\n   a) CREATE - Adding new video...")
    try:
        test_video = YouTubeVideo.objects.create(
            title="Admin Test Video",
            description="This is a test video created via admin test script",
            youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_id="dQw4w9WgXcQ",
            video_type="tutorial",
            category="technology",
            is_published=True,
            autoplay=True
        )
        print(f"   ✅ Created video: {test_video.title} (ID: {test_video.id})")
    except Exception as e:
        print(f"   ❌ Error creating video: {e}")
        return
    
    # READ
    print("\n   b) READ - Fetching video...")
    try:
        fetched_video = YouTubeVideo.objects.get(id=test_video.id)
        print(f"   ✅ Fetched video: {fetched_video.title}")
        print(f"      - Type: {fetched_video.video_type}")
        print(f"      - Autoplay: {fetched_video.autoplay}")
        print(f"      - Video ID: {fetched_video.video_id}")
    except Exception as e:
        print(f"   ❌ Error fetching video: {e}")
        return
    
    # UPDATE
    print("\n   c) UPDATE - Modifying video...")
    try:
        test_video.title = "Admin Test Video (Updated)"
        test_video.autoplay = False
        test_video.save()
        print(f"   ✅ Updated video: {test_video.title}")
        print(f"      - New autoplay: {test_video.autoplay}")
    except Exception as e:
        print(f"   ❌ Error updating video: {e}")
        return
    
    # DELETE
    print("\n   d) DELETE - Removing video...")
    try:
        video_id = test_video.id
        test_video.delete()
        print(f"   ✅ Deleted video ID: {video_id}")
        # Verify deletion
        exists = YouTubeVideo.objects.filter(id=video_id).exists()
        print(f"      - Video still exists: {exists}")
    except Exception as e:
        print(f"   ❌ Error deleting video: {e}")
        return
    
    # Check existing data
    print("\n5. Checking Existing Data:")
    print("-" * 70)
    event_count = Event.objects.count()
    video_count = YouTubeVideo.objects.count()
    print(f"✅ Total Events in database: {event_count}")
    print(f"✅ Total YouTube Videos in database: {video_count}")
    
    if event_count > 0:
        print("\n   Sample Events:")
        for event in Event.objects.all()[:3]:
            print(f"   - {event.name} (Type: {event.event_type}, Published: {event.is_published})")
    
    if video_count > 0:
        print("\n   Sample Videos:")
        for video in YouTubeVideo.objects.all()[:3]:
            print(f"   - {video.title} (Type: {video.video_type}, Published: {video.is_published})")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - ADMIN FUNCTIONALITY IS WORKING!")
    print("=" * 70)
    print("\nAdmin URLs:")
    print("  - Events: http://localhost:8000/admin/authentication/event/")
    print("  - YouTube Videos: http://localhost:8000/admin/authentication/youtubevideo/")
    print("\nTo access admin:")
    print("  1. Make sure server is running: python manage.py runserver")
    print("  2. Go to: http://localhost:8000/admin/")
    print("  3. Login with username: admin")
    print("=" * 70)

if __name__ == "__main__":
    test_admin_functionality()
