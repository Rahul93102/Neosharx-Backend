#!/usr/bin/env python
"""
Script to create sample Talk Episodes for NeoSharX Talks
"""

import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import TalkEpisode
from django.utils import timezone

def create_sample_episodes():
    """Create sample talk episodes"""
    
    # Clear existing episodes (optional - comment out if you want to keep existing ones)
    TalkEpisode.objects.all().delete()
    print("✅ Cleared existing episodes")
    
    episodes_data = [
        {
            'episode_number': 1,
            'title': 'The Future of AI and Machine Learning',
            'header': 'Exploring the cutting-edge advancements reshaping technology',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'thumbnail_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
            'description': '''Join us for an insightful discussion on the future of Artificial Intelligence and Machine Learning. 
Our expert panel explores groundbreaking developments in neural networks, deep learning architectures, and the ethical 
implications of AI adoption across industries. This episode covers real-world applications, from autonomous vehicles to 
personalized healthcare, and discusses the challenges we face in creating truly intelligent systems.

We dive deep into transformer models, reinforcement learning techniques, and the latest breakthroughs in natural language 
processing. Our speakers share their experiences building AI systems at scale and provide valuable insights for both 
beginners and experienced practitioners.''',
            'key_takeaways': [
                'Understanding transformer architecture and attention mechanisms',
                'Real-world applications of AI in healthcare, finance, and robotics',
                'Ethical considerations in AI development and deployment',
                'The importance of data quality and bias mitigation',
                'Future trends: Quantum computing meets AI'
            ],
            'speaker_panels': [
                {
                    'name': 'Dr. Sarah Chen',
                    'title': 'Chief AI Officer at TechVision',
                    'bio': 'Dr. Chen has 15 years of experience in AI research and has published over 50 papers on deep learning.',
                    'avatar_url': 'https://randomuser.me/api/portraits/women/44.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/sarahchen',
                        'twitter': 'https://twitter.com/sarahchen_ai'
                    }
                },
                {
                    'name': 'Prof. Michael Rodriguez',
                    'title': 'Professor of Computer Science, MIT',
                    'bio': 'Leading researcher in machine learning with focus on neural architecture search.',
                    'avatar_url': 'https://randomuser.me/api/portraits/men/32.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/mrodriguez',
                        'twitter': 'https://twitter.com/profrodriguez'
                    }
                },
                {
                    'name': 'Emily Watson',
                    'title': 'Senior ML Engineer at Google Brain',
                    'bio': 'Specialized in building production ML systems and MLOps best practices.',
                    'avatar_url': 'https://randomuser.me/api/portraits/women/68.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/emilywatson'
                    }
                }
            ],
            'duration_minutes': 75,
            'published_at': timezone.now() - timedelta(days=30),
            'is_published': True
        },
        {
            'episode_number': 2,
            'title': 'Building Scalable Startups in 2025',
            'header': 'From zero to unicorn: Lessons from successful founders',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'thumbnail_url': 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800',
            'description': '''A compelling conversation with founders who've successfully scaled their startups to unicorn status. 
This episode reveals the unfiltered truth about building companies in the modern era - from securing funding and building 
teams to pivoting strategies and maintaining work-life balance.

Our panelists share their biggest failures, pivotal moments, and the decisions that shaped their journey. Learn about 
product-market fit, growth hacking strategies, and the importance of company culture. Whether you're a first-time founder 
or seasoned entrepreneur, this episode provides actionable insights you can apply immediately.''',
            'key_takeaways': [
                'Finding product-market fit: How to know when you have it',
                'Fundraising strategies: When to bootstrap vs. seek VC funding',
                'Building a team culture that attracts top talent',
                'Growth hacking techniques that actually work',
                'Common pitfalls and how to avoid them'
            ],
            'speaker_panels': [
                {
                    'name': 'James Anderson',
                    'title': 'Co-founder & CEO of CloudScale',
                    'bio': 'Built CloudScale from 3 people to 500+ employees in 4 years, raised $150M Series C.',
                    'avatar_url': 'https://randomuser.me/api/portraits/men/75.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/jamesanderson',
                        'twitter': 'https://twitter.com/jamesa_ceo'
                    }
                },
                {
                    'name': 'Priya Sharma',
                    'title': 'Founder of FinTech Innovations',
                    'bio': 'Serial entrepreneur with 2 successful exits. Currently building her third startup.',
                    'avatar_url': 'https://randomuser.me/api/portraits/women/90.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/priyasharma',
                        'twitter': 'https://twitter.com/priya_founder'
                    }
                }
            ],
            'duration_minutes': 90,
            'published_at': timezone.now() - timedelta(days=15),
            'is_published': True
        },
        {
            'episode_number': 3,
            'title': 'Blockchain Beyond Cryptocurrency',
            'header': 'Real-world applications of distributed ledger technology',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'thumbnail_url': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800',
            'description': '''Move beyond Bitcoin and Ethereum to discover how blockchain technology is revolutionizing industries 
from supply chain management to healthcare records. This episode demystifies blockchain concepts and showcases real-world 
implementations that are solving actual business problems.

Our expert panel discusses smart contracts, decentralized finance (DeFi), NFTs, and the potential of Web3. Learn about 
the technical challenges, scalability solutions, and the future of decentralized systems. We also address common misconceptions 
and explore where blockchain makes sense versus traditional databases.''',
            'key_takeaways': [
                'Understanding blockchain fundamentals: distributed consensus and immutability',
                'Supply chain transparency through blockchain tracking',
                'Smart contracts: Use cases beyond cryptocurrency',
                'DeFi revolution: Reimagining financial services',
                'Environmental concerns and sustainable blockchain solutions'
            ],
            'speaker_panels': [
                {
                    'name': 'Alex Thompson',
                    'title': 'Blockchain Architect at Ethereum Foundation',
                    'bio': 'Core contributor to Ethereum 2.0, expert in consensus mechanisms and scalability.',
                    'avatar_url': 'https://randomuser.me/api/portraits/men/46.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/alexthompson',
                        'twitter': 'https://twitter.com/alex_eth'
                    }
                },
                {
                    'name': 'Dr. Lisa Wang',
                    'title': 'Director of Blockchain Research at IBM',
                    'bio': 'Leading enterprise blockchain initiatives and researching practical applications.',
                    'avatar_url': 'https://randomuser.me/api/portraits/women/27.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/lisawang'
                    }
                },
                {
                    'name': 'Marcus Brown',
                    'title': 'Co-founder of DeFi Protocol',
                    'bio': 'Pioneer in decentralized finance with focus on lending and borrowing protocols.',
                    'avatar_url': 'https://randomuser.me/api/portraits/men/52.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/marcusbrown',
                        'twitter': 'https://twitter.com/marcus_defi'
                    }
                }
            ],
            'duration_minutes': 80,
            'published_at': timezone.now() - timedelta(days=7),
            'is_published': True
        },
        {
            'episode_number': 4,
            'title': 'Cybersecurity in the Age of Remote Work',
            'header': 'Protecting your digital assets in a distributed world',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'thumbnail_url': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800',
            'description': '''The shift to remote work has created unprecedented cybersecurity challenges. This episode brings together 
security experts to discuss the evolving threat landscape and practical strategies for protecting your organization.

From zero-trust architecture to employee training, our panel covers everything you need to know about modern cybersecurity. 
Learn about common attack vectors, incident response planning, and the latest security tools. We also discuss compliance 
requirements and how to build a security-first culture in your organization.''',
            'key_takeaways': [
                'Implementing zero-trust security architecture',
                'Common cyber threats: Phishing, ransomware, and social engineering',
                'Securing remote access: VPNs, MFA, and endpoint protection',
                'Incident response: Preparing for and recovering from breaches',
                'Building a security-aware culture through employee training'
            ],
            'speaker_panels': [
                {
                    'name': 'Rachel Kim',
                    'title': 'Chief Information Security Officer at SecureNet',
                    'bio': 'Former NSA analyst with 20 years of cybersecurity experience.',
                    'avatar_url': 'https://randomuser.me/api/portraits/women/55.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/rachelkim',
                        'twitter': 'https://twitter.com/rachel_infosec'
                    }
                },
                {
                    'name': 'David Martinez',
                    'title': 'Penetration Testing Lead at CyberGuard',
                    'bio': 'Ethical hacker specializing in finding vulnerabilities before attackers do.',
                    'avatar_url': 'https://randomuser.me/api/portraits/men/18.jpg',
                    'social_links': {
                        'linkedin': 'https://linkedin.com/in/davidmartinez',
                        'twitter': 'https://twitter.com/david_hacker'
                    }
                }
            ],
            'duration_minutes': 65,
            'published_at': timezone.now() - timedelta(days=2),
            'is_published': True
        }
    ]
    
    created_count = 0
    for episode_data in episodes_data:
        episode, created = TalkEpisode.objects.get_or_create(
            episode_number=episode_data['episode_number'],
            defaults=episode_data
        )
        
        if created:
            created_count += 1
            print(f"✅ Created Episode {episode.episode_number}: {episode.title}")
        else:
            print(f"⚠️  Episode {episode.episode_number} already exists")
    
    print(f"\n🎉 Created {created_count} new talk episodes!")
    print(f"📊 Total episodes in database: {TalkEpisode.objects.count()}")


if __name__ == '__main__':
    print("🚀 Creating sample Talk Episodes...\n")
    create_sample_episodes()
    print("\n✅ Done!")
