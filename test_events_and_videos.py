#!/usr/bin/env python
"""
Test script for Events and YouTube Videos API
Creates sample data and tests all endpoints
"""

import os
import sys
import django
import requests
from datetime import datetime, date, time, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import Event, YouTubeVideo, CustomUser
from django.utils.text import slugify

# API Base URL
BASE_URL = "http://127.0.0.1:8000/api/auth"

def create_sample_events():
    """Create sample events for testing"""
    print("\n" + "="*60)
    print("Creating Sample Events...")
    print("="*60)
    
    events_data = [
        {
            'name': 'Tech Conference 2025',
            'description': 'Annual technology conference showcasing latest innovations',
            'details': 'Join us for an immersive experience with industry leaders, cutting-edge demos, and networking opportunities.',
            'event_type': 'past',
            'category': 'conference',
            'location': 'San Francisco Convention Center',
            'is_virtual': False,
            'event_date': date(2024, 10, 15),
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'featured_image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?q=80&w=2070&auto=format&fit=crop',
            'is_featured': True,
            'is_published': True,
            'max_participants': 500,
            'is_registration_open': False,
        },
        {
            'name': 'NeoSharX Annual Summit',
            'description': 'The biggest startup and innovation summit of the year',
            'details': 'Connect with founders, investors, and innovators. Featuring keynotes, panels, and pitch competitions.',
            'event_type': 'recent',
            'category': 'summit',
            'location': 'Mumbai Convention Hall',
            'is_virtual': False,
            'event_date': date(2024, 12, 5),
            'start_time': time(10, 0),
            'end_time': time(19, 0),
            'featured_image': 'https://images.unsplash.com/photo-1511578314322-379afb476865?q=80&w=2070&auto=format&fit=crop',
            'is_featured': True,
            'is_published': True,
            'max_participants': 1000,
            'is_registration_open': False,
        },
        {
            'name': 'Robotics Expo',
            'description': 'Explore the future of robotics and automation',
            'details': 'Hands-on demonstrations, workshops, and exhibitions from leading robotics companies.',
            'event_type': 'recent',
            'category': 'expo',
            'location': 'Bangalore Tech Park',
            'is_virtual': False,
            'event_date': date(2024, 11, 28),
            'start_time': time(11, 0),
            'end_time': time(17, 0),
            'featured_image': 'https://images.unsplash.com/photo-1554224312-3e283f83a5e8?q=80&w=2070&auto=format&fit=crop',
            'is_featured': False,
            'is_published': True,
            'max_participants': 300,
            'is_registration_open': False,
        },
        {
            'name': 'Founder\'s Mixer',
            'description': 'Networking event for startup founders',
            'details': 'Casual meetup to connect with fellow entrepreneurs, share experiences, and build valuable relationships.',
            'event_type': 'upcoming',
            'category': 'networking',
            'location': 'Delhi Hub Co-working Space',
            'is_virtual': False,
            'event_date': date(2025, 11, 15),
            'start_time': time(18, 0),
            'end_time': time(21, 0),
            'featured_image': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?q=80&w=2069&auto=format&fit=crop',
            'is_featured': False,
            'is_published': True,
            'max_participants': 100,
            'is_registration_open': True,
            'registration_url': 'https://neosharx.com/register/founders-mixer',
        },
        {
            'name': 'AI Hackathon 2025',
            'description': '48-hour AI/ML hackathon with amazing prizes',
            'details': 'Build innovative AI solutions, compete with top teams, and win prizes worth ₹10 lakhs!',
            'event_type': 'upcoming',
            'category': 'hackathon',
            'location': 'Virtual + Hybrid',
            'is_virtual': True,
            'event_date': date(2025, 12, 1),
            'start_time': time(0, 0),
            'end_time': time(23, 59),
            'featured_image': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=2070&auto=format&fit=crop',
            'is_featured': True,
            'is_published': True,
            'max_participants': 500,
            'is_registration_open': True,
            'registration_url': 'https://neosharx.com/hackathon/ai-2025',
        },
    ]
    
    created_count = 0
    for event_data in events_data:
        slug = slugify(event_data['name'])
        event, created = Event.objects.get_or_create(
            slug=slug,
            defaults=event_data
        )
        if created:
            created_count += 1
            print(f"✅ Created: {event.name} ({event.event_type})")
        else:
            print(f"ℹ️  Already exists: {event.name}")
    
    print(f"\n✨ Total events created: {created_count}")
    print(f"📊 Total events in database: {Event.objects.count()}")
    return created_count > 0


def create_sample_youtube_videos():
    """Create sample YouTube videos for testing"""
    print("\n" + "="*60)
    print("Creating Sample YouTube Videos...")
    print("="*60)
    
    videos_data = [
        {
            'title': 'Building a Successful Startup - Full Guide',
            'description': 'Complete guide to building and scaling your startup from scratch',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'video_id': 'dQw4w9WgXcQ',
            'video_type': 'video',
            'category': 'startup_stories',
            'is_featured': True,
            'is_published': True,
            'display_order': 1,
            'autoplay': True,
        },
        {
            'title': 'AI & Machine Learning in 2025',
            'description': 'Latest trends and breakthroughs in AI/ML technology',
            'youtube_url': 'https://www.youtube.com/watch?v=ScMzIvxBSi4',
            'video_id': 'ScMzIvxBSi4',
            'video_type': 'video',
            'category': 'tech_talks',
            'is_featured': True,
            'is_published': True,
            'display_order': 2,
            'autoplay': True,
        },
        {
            'title': 'Quick Startup Tips',
            'description': '60-second startup wisdom from successful founders',
            'youtube_url': 'https://youtube.com/shorts/ABC123',
            'video_id': 'ABC123',
            'video_type': 'short',
            'category': 'startup_stories',
            'is_featured': False,
            'is_published': True,
            'display_order': 3,
            'autoplay': True,
        },
        {
            'title': 'Hackathon Winners Showcase',
            'description': 'Amazing projects from our recent hackathon',
            'youtube_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
            'video_id': 'jNQXAC9IVRw',
            'video_type': 'video',
            'category': 'hackathons',
            'is_featured': False,
            'is_published': True,
            'display_order': 4,
            'autoplay': True,
        },
        {
            'title': 'Tech Interview Tips',
            'description': 'Ace your next tech interview with these tips',
            'youtube_url': 'https://youtube.com/shorts/XYZ789',
            'video_id': 'XYZ789',
            'video_type': 'short',
            'category': 'tutorials',
            'is_featured': False,
            'is_published': True,
            'display_order': 5,
            'autoplay': True,
        },
    ]
    
    created_count = 0
    for video_data in videos_data:
        slug = slugify(video_data['title'])
        # Generate embed URL
        video_id = video_data['video_id']
        if video_data['video_type'] == 'short':
            embed_url = f'https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}'
        else:
            embed_url = f'https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1'
        
        video_data['slug'] = slug
        video_data['embed_url'] = embed_url
        video_data['auto_thumbnail'] = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
        
        video, created = YouTubeVideo.objects.get_or_create(
            slug=slug,
            defaults=video_data
        )
        if created:
            created_count += 1
            print(f"✅ Created: {video.title} ({video.video_type})")
        else:
            print(f"ℹ️  Already exists: {video.title}")
    
    print(f"\n✨ Total videos created: {created_count}")
    print(f"📊 Total videos in database: {YouTubeVideo.objects.count()}")
    return created_count > 0


def test_events_api():
    """Test Events API endpoints"""
    print("\n" + "="*60)
    print("Testing Events API...")
    print("="*60)
    
    tests = [
        ("All Events", f"{BASE_URL}/events/"),
        ("Past Events", f"{BASE_URL}/events/type/past/"),
        ("Recent Events", f"{BASE_URL}/events/type/recent/"),
        ("Upcoming Events", f"{BASE_URL}/events/type/upcoming/"),
        ("Featured Events", f"{BASE_URL}/events/featured/"),
    ]
    
    for test_name, url in tests:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"✅ {test_name}: {response.status_code} - {count} events")
            else:
                print(f"❌ {test_name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {test_name}: Error - {str(e)}")


def test_youtube_api():
    """Test YouTube Videos API endpoints"""
    print("\n" + "="*60)
    print("Testing YouTube Videos API...")
    print("="*60)
    
    tests = [
        ("All Videos", f"{BASE_URL}/youtube-videos/"),
        ("Featured Videos", f"{BASE_URL}/youtube-videos/featured/"),
        ("YouTube Videos", f"{BASE_URL}/youtube-videos/type/video/"),
        ("YouTube Shorts", f"{BASE_URL}/youtube-videos/type/short/"),
    ]
    
    for test_name, url in tests:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"✅ {test_name}: {response.status_code} - {count} videos")
            else:
                print(f"❌ {test_name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {test_name}: Error - {str(e)}")


def main():
    """Main test function"""
    print("\n" + "="*60)
    print("🚀 NeoSharX Events & YouTube Videos Test Suite")
    print("="*60)
    
    # Create sample data
    events_created = create_sample_events()
    videos_created = create_sample_youtube_videos()
    
    # Test APIs (server should already be running)
    print("\n" + "="*60)
    print("Testing APIs (server on http://127.0.0.1:8000)...")
    print("="*60)
    
    test_events_api()
    test_youtube_api()
    
    print("\n" + "="*60)
    print("✅ Test Suite Completed!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Access Django Admin: http://127.0.0.1:8000/admin/")
    print("2. View Events API: http://127.0.0.1:8000/api/auth/events/")
    print("3. View Videos API: http://127.0.0.1:8000/api/auth/youtube-videos/")
    print("4. Test homepage integration in index.html")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
