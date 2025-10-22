#!/usr/bin/env python
"""
Script to create sample events for testing
"""
import os
import django
import sys

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import Event, CustomUser
from datetime import date, time, timedelta

def create_sample_events():
    """Create sample events for testing"""
    
    # Get or create admin user
    admin_user, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@neosharx.com',
            'phone_number': '+1234567890',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Created admin user")
    
    # Clear existing events
    Event.objects.all().delete()
    print("✓ Cleared existing events")
    
    today = date.today()
    
    # Past Events
    past_events = [
        {
            'name': 'Tech Conference 2023',
            'description': 'Annual technology conference featuring industry leaders',
            'details': 'Join us for a full day of inspiring talks, networking opportunities, and hands-on workshops covering the latest in technology and innovation.',
            'event_type': 'past',
            'category': 'conference',
            'location': 'San Francisco Convention Center',
            'is_virtual': False,
            'venue_details': '747 Howard St, San Francisco, CA 94103',
            'event_date': today - timedelta(days=150),
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'event_timezone': 'America/Los_Angeles',
            'featured_image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400',
            'benefits': [
                'Networking with 500+ professionals',
                'Access to all workshop sessions',
                'Free meals and refreshments',
                'Certificate of attendance',
                'Exclusive swag bag'
            ],
            'key_highlights': [
                'Keynote by tech industry leaders',
                '20+ interactive sessions',
                'Startup pitch competition',
                'Job fair with top companies'
            ],
            'is_featured': False,
            'is_published': True,
            'display_order': 1,
            'max_participants': 500,
            'current_participants': 487,
            'is_free': False,
            'ticket_price': 199.00,
            'organizer_name': 'NeoSharX Events Team'
        },
        {
            'name': 'Startup Pitch Night',
            'description': 'Showcase your startup idea to investors and mentors',
            'details': 'An evening dedicated to emerging startups presenting their innovative ideas to a panel of experienced investors and industry mentors.',
            'event_type': 'past',
            'category': 'networking',
            'location': 'Innovation Hub',
            'is_virtual': False,
            'event_date': today - timedelta(days=90),
            'start_time': time(18, 0),
            'end_time': time(21, 0),
            'event_timezone': 'America/New_York',
            'featured_image': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=400',
            'benefits': [
                'Direct feedback from investors',
                'Networking with fellow entrepreneurs',
                'Media coverage opportunity',
                'Potential funding connections'
            ],
            'is_featured': False,
            'is_published': True,
            'display_order': 2,
            'max_participants': 100,
            'current_participants': 95,
            'is_free': True,
            'organizer_name': 'NeoSharX Startups'
        }
    ]
    
    # Recent Events
    recent_events = [
        {
            'name': 'NeoSharX Annual Summit',
            'description': 'Our biggest annual gathering of innovators and creators',
            'details': 'A comprehensive two-day summit bringing together entrepreneurs, developers, and innovators from around the world to share knowledge and build connections.',
            'event_type': 'recent',
            'category': 'summit',
            'location': 'Downtown Convention Center',
            'is_virtual': False,
            'event_date': today - timedelta(days=15),
            'start_time': time(8, 30),
            'end_time': time(17, 30),
            'event_timezone': 'America/Chicago',
            'featured_image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400',
            'benefits': [
                'Two days of intensive learning',
                'Access to all keynote speakers',
                'VIP networking dinner',
                'Exclusive merchandise',
                'One-on-one mentor sessions'
            ],
            'key_highlights': [
                '50+ speaker sessions',
                'Product demo showcase',
                'Awards ceremony',
                'After-party networking'
            ],
            'is_featured': True,
            'is_published': True,
            'display_order': 1,
            'max_participants': 1000,
            'current_participants': 973,
            'is_free': False,
            'ticket_price': 299.00,
            'organizer_name': 'NeoSharX Team'
        },
        {
            'name': 'Robotics Expo',
            'description': 'Discover the latest in robotics and automation technology',
            'details': 'An immersive expo featuring cutting-edge robotics demonstrations, workshops, and competitions for all age groups.',
            'event_type': 'recent',
            'category': 'expo',
            'location': 'Tech Innovation Center',
            'is_virtual': False,
            'event_date': today - timedelta(days=7),
            'start_time': time(10, 0),
            'end_time': time(19, 0),
            'event_timezone': 'America/Los_Angeles',
            'featured_image': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400',
            'benefits': [
                'Hands-on robot demonstrations',
                'Meet leading robotics companies',
                'Participate in competitions',
                'Free robotics starter kit',
                'Workshop certificates'
            ],
            'key_highlights': [
                'Robot battle competitions',
                'AI & ML workshops',
                'Industry expert talks',
                'Kids robotics zone'
            ],
            'is_featured': True,
            'is_published': True,
            'display_order': 2,
            'max_participants': 750,
            'current_participants': 692,
            'is_free': True,
            'organizer_name': 'NeoSharX Robotics'
        }
    ]
    
    # Upcoming Events
    upcoming_events = [
        {
            'name': 'Cyber Security Conclave',
            'description': 'Learn about the latest cybersecurity threats and solutions',
            'details': 'A comprehensive conference covering cybersecurity best practices, threat intelligence, and hands-on security workshops.',
            'event_type': 'upcoming',
            'category': 'conference',
            'location': 'Virtual & Hybrid',
            'is_virtual': True,
            'event_date': today + timedelta(days=45),
            'start_time': time(9, 0),
            'end_time': time(17, 0),
            'event_timezone': 'UTC',
            'featured_image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400',
            'benefits': [
                'Live and recorded sessions',
                'Certification opportunity',
                'Security tools trial access',
                'Expert Q&A sessions',
                'Networking in virtual lounges'
            ],
            'key_highlights': [
                'Ethical hacking workshop',
                'Live threat simulation',
                'Security tool demonstrations',
                'Career guidance sessions'
            ],
            'is_featured': True,
            'is_published': True,
            'display_order': 1,
            'max_participants': 2000,
            'current_participants': 456,
            'is_free': False,
            'ticket_price': 149.00,
            'early_bird_price': 99.00,
            'organizer_name': 'NeoSharX Security',
            'is_registration_open': True
        },
        {
            'name': 'Future of Work Summit',
            'description': 'Exploring remote work, AI, and the changing workplace',
            'details': 'Join industry leaders discussing the transformation of work in the age of AI, remote collaboration, and digital transformation.',
            'event_type': 'upcoming',
            'category': 'summit',
            'location': 'Hybrid - Seattle & Online',
            'is_virtual': True,
            'event_date': today + timedelta(days=60),
            'start_time': time(10, 0),
            'end_time': time(16, 0),
            'event_timezone': 'America/Los_Angeles',
            'featured_image': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400',
            'benefits': [
                'Future of work insights',
                'AI tools for productivity',
                'Remote work best practices',
                'Employer branding strategies',
                'Exclusive research reports'
            ],
            'key_highlights': [
                'Panel with Fortune 500 CHROs',
                'AI productivity demos',
                'Remote work case studies',
                'Networking breakout rooms'
            ],
            'is_featured': True,
            'is_published': True,
            'display_order': 2,
            'max_participants': 1500,
            'current_participants': 234,
            'is_free': False,
            'ticket_price': 199.00,
            'organizer_name': 'NeoSharX Future Lab',
            'is_registration_open': True
        },
        {
            'name': 'AI & Machine Learning Workshop',
            'description': 'Hands-on workshop for beginners and intermediate learners',
            'details': 'A practical, hands-on workshop covering the fundamentals of AI and machine learning with real-world projects.',
            'event_type': 'upcoming',
            'category': 'workshop',
            'location': 'Tech Campus - Building A',
            'is_virtual': False,
            'event_date': today + timedelta(days=30),
            'start_time': time(13, 0),
            'end_time': time(18, 0),
            'event_timezone': 'America/New_York',
            'featured_image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200',
            'thumbnail_image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400',
            'benefits': [
                'Hands-on coding exercises',
                'Free cloud computing credits',
                'Course completion certificate',
                'Access to learning materials',
                'Mentorship opportunity'
            ],
            'key_highlights': [
                'Build your first ML model',
                'Deep learning basics',
                'Real-world datasets',
                'Project showcase'
            ],
            'is_featured': False,
            'is_published': True,
            'display_order': 3,
            'max_participants': 150,
            'current_participants': 89,
            'is_free': False,
            'ticket_price': 79.00,
            'organizer_name': 'NeoSharX Academy',
            'is_registration_open': True
        }
    ]
    
    # Create all events
    all_events = past_events + recent_events + upcoming_events
    created_count = 0
    
    for event_data in all_events:
        event_data['created_by'] = admin_user
        event = Event.objects.create(**event_data)
        created_count += 1
        print(f"✓ Created event: {event.name} ({event.event_type})")
    
    print(f"\n✅ Successfully created {created_count} sample events!")
    print(f"   - Past events: {len(past_events)}")
    print(f"   - Recent events: {len(recent_events)}")
    print(f"   - Upcoming events: {len(upcoming_events)}")
    
    return created_count

if __name__ == '__main__':
    print("Creating sample events...\n")
    try:
        count = create_sample_events()
        print(f"\n🎉 All done! Created {count} events total.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
