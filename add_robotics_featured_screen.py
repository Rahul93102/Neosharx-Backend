#!/usr/bin/env python
"""
Script to add a featured screen to a Robotics News article
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import RoboticsNews

# Get the first published article
article = RoboticsNews.objects.filter(is_published=True).first()

if article:
    # Add a featured screen
    article.featured_screen = {
        "url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200",
        "type": "image",
        "is_featured": True
    }
    article.save()
    print(f"✅ Added featured screen to Robotics News: {article.title}")
    print(f"   Featured screen: {article.featured_screen}")
else:
    print("❌ No published Robotics News found")
