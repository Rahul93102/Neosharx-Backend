#!/usr/bin/env python
"""
Script to add a featured screen to a Neo Story
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import NeoStory

# Get the first published story
story = NeoStory.objects.filter(is_published=True).first()

if story:
    # Add a featured screen
    story.featured_screen = {
        "url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200",
        "type": "image",
        "is_featured": True
    }
    story.save()
    print(f"✅ Added featured screen to Neo Story: {story.header}")
    print(f"   Featured screen: {story.featured_screen}")
else:
    print("❌ No published Neo Stories found")
