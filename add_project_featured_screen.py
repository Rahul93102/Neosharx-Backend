#!/usr/bin/env python
"""
Script to add a featured screen to a Neo Project
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import NeoProject

# Get the first published project
project = NeoProject.objects.filter(is_published=True).first()

if project:
    # Add a featured screen
    project.featured_screen = {
        "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200",
        "type": "image",
        "is_featured": True
    }
    project.save()
    print(f"✅ Added featured screen to Neo Project: {project.title}")
    print(f"   Featured screen: {project.featured_screen}")
else:
    print("❌ No published Neo Projects found")
