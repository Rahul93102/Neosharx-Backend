#!/usr/bin/env python3
"""
Test script to add featured screens to talk episodes
Run: python3 test_featured_screens.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import TalkEpisode

def add_featured_screens():
    """Add featured screens to existing episodes"""
    
    # Sample featured screen URLs
    featured_screens_data = [
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=800&fit=crop",
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1200&h=800&fit=crop",
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=800&fit=crop",
        "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1200&h=800&fit=crop",
        "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=1200&h=800&fit=crop",
    ]
    
    episodes = TalkEpisode.objects.all()
    
    for episode in episodes:
        # Add 3-5 random screens per episode
        import random
        num_screens = random.randint(3, 5)
        episode.featured_screens = random.sample(featured_screens_data, num_screens)
        episode.save()
        print(f"✅ Added {num_screens} featured screens to Episode {episode.episode_number}: {episode.title}")
    
    print(f"\n✅ Successfully updated {episodes.count()} episodes with featured screens!")

if __name__ == '__main__':
    print("Adding featured screens to talk episodes...\n")
    add_featured_screens()
