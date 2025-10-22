#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import StartupStory

stories_data = [
    {
        'heading': 'From Dorm Room to Global Impact: The Story of InnovateX',
        'slug': 'innovatex-dorm-room-to-global-impact',
        'summary': 'Follow the inspiring journey of Alex Chen, the founder of InnovateX, as they revolutionize the tech industry with their groundbreaking AI solutions.',
        'content': '<p>Alex Chen built InnovateX from scratch...</p>',
        'key_takeaways': 'Start with passion\nCustomer feedback is key',
        'featured_image': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800',
        'industry': 'ai_ml',
        'stage': 'growth',
        'company_name': 'InnovateX',
        'is_featured': True,
        'is_published': True,
    },
]

for data in stories_data:
    StartupStory.objects.update_or_create(slug=data['slug'], defaults=data)
    print(f"Created: {data['heading']}")

print("Done!")
