"""
Add featured screens to talk episodes for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import TalkEpisode

# Get first few episodes
episodes = TalkEpisode.objects.all()[:3]

if episodes:
    # Add featured screen to first episode (image)
    ep1 = episodes[0]
    ep1.featured_screen = {
        "url": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=800",
        "type": "image",
        "is_featured": True
    }
    ep1.save()
    print(f"✓ Added featured image to Episode {ep1.episode_number}: {ep1.title}")

    # Add featured screen to second episode (video)
    if len(episodes) > 1:
        ep2 = episodes[1]
        ep2.featured_screen = {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "type": "video",
            "is_featured": True
        }
        ep2.save()
        print(f"✓ Added featured video to Episode {ep2.episode_number}: {ep2.title}")

    # Add non-featured screen to third episode
    if len(episodes) > 2:
        ep3 = episodes[2]
        ep3.featured_screen = {
            "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800",
            "type": "image",
            "is_featured": False
        }
        ep3.save()
        print(f"✓ Added non-featured screen to Episode {ep3.episode_number}: {ep3.title}")

    print("\n✅ Featured screens added successfully!")
    print("Featured episodes (will show in slider):", 2)
    print("Non-featured episodes (only in card):", 1)
else:
    print("❌ No episodes found. Please create episodes first.")
