#!/usr/bin/env python
"""
Comprehensive script to add sample data to all NeoSharX backend tables
"""
import os
import django
import sys
from datetime import date, time, timedelta, datetime
from django.utils import timezone

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
django.setup()

from authentication.models import (
    Event, NeoProject, NeoStory, RoboticsNews, SharXathon,
    StartupStory, TalkEpisode, TechNews, YouTubeVideo, CustomUser
)

def create_admin_user():
    """Create admin user if not exists"""
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
        print("✓ Created admin user")
    return admin_user

def add_events():
    """Add sample events"""
    print("\n--- Adding Events ---")
    Event.objects.all().delete()

    today = date.today()

    events_data = [
        {
            'name': 'AI & ML Bootcamp 2025',
            'description': 'Intensive 3-day bootcamp on Artificial Intelligence and Machine Learning',
            'details': 'Join industry experts for hands-on training in AI/ML fundamentals, deep learning, and practical applications. Perfect for students and professionals looking to upskill.',
            'event_type': 'upcoming',
            'category': 'workshop',
            'location': 'IIT Delhi, New Delhi',
            'is_virtual': False,
            'event_date': today + timedelta(days=30),
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'featured_image': 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200',
            'benefits': ['Hands-on AI/ML training', 'Industry expert mentors', 'Certificate of completion', 'Networking opportunities'],
            'is_featured': True,
            'is_published': True,
            'max_participants': 200,
            'is_free': False,
            'ticket_price': 150.00,
        },
        {
            'name': 'Startup Founder Meetup',
            'description': 'Monthly meetup for startup founders and entrepreneurs',
            'details': 'Connect with fellow founders, share experiences, and learn from successful entrepreneurs in our monthly networking session.',
            'event_type': 'upcoming',
            'category': 'meetup',
            'location': 'Virtual Event',
            'is_virtual': True,
            'event_date': today + timedelta(days=15),
            'start_time': time(19, 0),
            'end_time': time(21, 0),
            'featured_image': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1200',
            'benefits': ['Networking with founders', 'Mentorship opportunities', 'Free refreshments', 'Knowledge sharing'],
            'is_featured': False,
            'is_published': True,
            'max_participants': 100,
            'is_free': True,
        },
        {
            'name': 'Tech Conference 2024',
            'description': 'Annual technology conference featuring industry leaders',
            'details': 'Our flagship annual conference bringing together 500+ tech professionals, featuring keynote speeches, workshops, and networking opportunities.',
            'event_type': 'recent',
            'category': 'conference',
            'location': 'Bangalore International Center',
            'is_virtual': False,
            'event_date': today - timedelta(days=10),
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'featured_image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200',
            'benefits': ['500+ attendees', 'Keynote speeches', 'Workshop sessions', 'Networking dinner'],
            'is_featured': True,
            'is_published': True,
            'max_participants': 500,
            'current_participants': 487,
            'is_free': False,
            'ticket_price': 250.00,
        }
    ]

    for event_data in events_data:
        event = Event.objects.create(**event_data)
        print(f"✓ Created event: {event.name}")

def add_neo_projects():
    """Add sample Neo Projects"""
    print("\n--- Adding Neo Projects ---")
    NeoProject.objects.all().delete()

    projects_data = [
        {
            'title': 'AI-Powered Code Review Assistant',
            'description': 'An intelligent code review tool that uses machine learning to identify bugs and suggest improvements.',
            'detailed_description': 'Built with Python and TensorFlow, this tool analyzes code patterns and provides automated feedback to developers, helping improve code quality and reduce review time by 60%.',
            'category': 'ai_ml',
            'technologies': 'Python, TensorFlow, FastAPI, PostgreSQL',
            'github_url': 'https://github.com/neosharx/ai-code-review',
            'status': 'completed',
            'difficulty_level': 'advanced',
            'features': ['Automated bug detection', 'Code quality scoring', 'Performance suggestions', 'Integration with GitHub'],
            'developer_name': 'Rahul Sharma',
            'developer_email': 'rahul@neosharx.com',
            'is_featured': True,
            'is_published': True,
            'is_open_source': True,
            'featured_image': 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800',
        },
        {
            'title': 'Smart Agriculture IoT Platform',
            'description': 'IoT platform for precision farming with real-time monitoring and automated irrigation.',
            'detailed_description': 'A comprehensive IoT solution for modern farming that monitors soil moisture, temperature, and crop health using sensors and provides automated irrigation recommendations.',
            'category': 'iot',
            'technologies': 'React, Node.js, MongoDB, Raspberry Pi, MQTT',
            'github_url': 'https://github.com/neosharx/smart-agri-iot',
            'status': 'beta',
            'difficulty_level': 'intermediate',
            'features': ['Real-time sensor monitoring', 'Automated irrigation', 'Mobile app dashboard', 'Weather integration'],
            'developer_name': 'Priya Patel',
            'developer_email': 'priya@neosharx.com',
            'is_featured': True,
            'is_published': True,
            'is_open_source': True,
            'featured_image': 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800',
        },
        {
            'title': 'Blockchain Voting System',
            'description': 'Secure and transparent voting platform built on blockchain technology.',
            'detailed_description': 'A decentralized voting system that ensures election integrity through blockchain technology, providing transparency and eliminating voter fraud.',
            'category': 'blockchain',
            'technologies': 'Solidity, Web3.js, React, Ethereum, IPFS',
            'github_url': 'https://github.com/neosharx/blockchain-voting',
            'status': 'in_development',
            'difficulty_level': 'expert',
            'features': ['Decentralized voting', 'Zero-knowledge proofs', 'Real-time results', 'Immutable audit trail'],
            'developer_name': 'Arun Kumar',
            'developer_email': 'arun@neosharx.com',
            'is_featured': False,
            'is_published': True,
            'is_open_source': True,
            'featured_image': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800',
        }
    ]

    for project_data in projects_data:
        project = NeoProject.objects.create(**project_data)
        print(f"✓ Created project: {project.title}")

def add_neo_stories():
    """Add sample Neo Stories"""
    print("\n--- Adding Neo Stories ---")
    NeoStory.objects.all().delete()

    stories_data = [
        {
            'header': 'From College Dropout to Unicorn Founder',
            'introduction': 'How a 19-year-old college dropout built a $1B company in just 3 years',
            'sections': [
                {
                    'subheading': 'The Beginning',
                    'paragraph': 'It all started in a small garage in Bangalore when Rahul realized the traditional education system wasn\'t for him. At 19, he dropped out of IIT Bombay to pursue his dream of building technology that could solve real-world problems.',
                    'media_type': 'image',
                    'media_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800',
                    'media_caption': 'Rahul working in his first office space'
                },
                {
                    'subheading': 'The Breakthrough',
                    'paragraph': 'After months of coding and iterating, Rahul developed an AI-powered logistics platform that could predict delivery times with 99% accuracy. This innovation caught the attention of major investors.',
                    'media_type': 'image',
                    'media_url': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=800',
                    'media_caption': 'The first version of the logistics platform'
                },
                {
                    'subheading': 'Scaling to Success',
                    'paragraph': 'With seed funding secured, the team grew from 3 to 300 employees in 18 months. Today, the company serves millions of customers across 15 countries.',
                    'media_type': 'video',
                    'media_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'media_caption': 'Company growth journey'
                }
            ],
            'category': 'entrepreneurship',
            'tags': 'startup, entrepreneurship, AI, logistics',
            'author_name': 'Sarah Johnson',
            'read_time': 8,
            'main_image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200',
            'is_featured': True,
            'is_published': True,
        },
        {
            'header': 'Revolutionizing Healthcare with AI',
            'introduction': 'How Dr. Priya\'s AI diagnostic tool is saving lives in rural India',
            'sections': [
                {
                    'subheading': 'The Healthcare Challenge',
                    'paragraph': 'In rural India, access to quality healthcare remains a major challenge. Dr. Priya noticed that many patients were misdiagnosed due to lack of specialist doctors in remote areas.',
                    'media_type': 'image',
                    'media_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800',
                    'media_caption': 'Rural healthcare center in India'
                },
                {
                    'subheading': 'Building the Solution',
                    'paragraph': 'Combining her medical expertise with AI knowledge, Dr. Priya developed an affordable diagnostic tool that can identify common diseases with 95% accuracy using just a smartphone camera.',
                    'media_type': 'image',
                    'media_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=800',
                    'media_caption': 'The AI diagnostic device'
                }
            ],
            'category': 'social_impact',
            'tags': 'healthcare, AI, rural development, diagnostics',
            'author_name': 'Michael Chen',
            'read_time': 6,
            'main_image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1200',
            'is_featured': True,
            'is_published': True,
        }
    ]

    for story_data in stories_data:
        story = NeoStory.objects.create(**story_data)
        print(f"✓ Created story: {story.header}")

def add_robotics_news():
    """Add sample Robotics News"""
    print("\n--- Adding Robotics News ---")
    RoboticsNews.objects.all().delete()

    news_data = [
        {
            'title': 'Boston Dynamics Atlas Robot Achieves Human-Level Parkour',
            'subtitle': 'Revolutionary breakthrough in robotic locomotion',
            'summary': 'Boston Dynamics\' Atlas robot has demonstrated unprecedented agility, performing complex parkour moves that were previously thought impossible for robots.',
            'content': 'In a stunning display of robotic capabilities, Boston Dynamics\' Atlas humanoid robot has successfully performed parkour maneuvers including flips, jumps, and complex navigation through obstacle courses. This breakthrough brings us closer to robots that can navigate human environments with natural fluidity.',
            'category': 'ai_robotics',
            'tags': 'Boston Dynamics, Atlas, parkour, humanoid robots',
            'priority': 'high',
            'featured_image': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800',
            'source_name': 'TechCrunch',
            'author_name': 'Sarah Mitchell',
            'robot_type': 'Humanoid Robot',
            'technology_focus': 'Advanced locomotion, AI control systems',
            'is_featured': True,
            'is_published': True,
            'reading_time': 4,
        },
        {
            'title': 'Agricultural Robots Reduce Crop Losses by 40%',
            'subtitle': 'Precision farming technology transforms agriculture',
            'summary': 'New autonomous robots equipped with AI vision systems are revolutionizing precision farming by detecting crop diseases early and applying targeted treatments.',
            'content': 'Autonomous agricultural robots developed by AgriBot Inc. have demonstrated a 40% reduction in crop losses through early disease detection and precision pesticide application. The robots use advanced computer vision and machine learning algorithms to identify problems before they spread.',
            'category': 'agriculture',
            'tags': 'agriculture, precision farming, AI, crop monitoring',
            'priority': 'medium',
            'featured_image': 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800',
            'source_name': 'Agricultural Technology Review',
            'author_name': 'Dr. Robert Green',
            'robot_type': 'Agricultural Drone/Robot',
            'technology_focus': 'Computer vision, machine learning, precision agriculture',
            'is_featured': False,
            'is_published': True,
            'reading_time': 5,
        }
    ]

    for news_item in news_data:
        news = RoboticsNews.objects.create(**news_item)
        print(f"✓ Created robotics news: {news.title}")

def add_sharxathons():
    """Add sample SharXathons"""
    print("\n--- Adding SharXathons ---")
    SharXathon.objects.all().delete()

    today = date.today()

    hackathons_data = [
        {
            'name': 'AI Innovation Challenge 2025',
            'description': 'Build the next generation of AI applications in 48 hours',
            'content': 'Join hundreds of developers, designers, and AI enthusiasts for a 48-hour coding marathon focused on creating innovative AI solutions. Whether you\'re a beginner or expert, this hackathon offers tracks for all skill levels.',
            'topic': 'Artificial Intelligence & Machine Learning',
            'difficulty_level': 'intermediate',
            'team_size': '4-5',
            'max_participants': 300,
            'start_datetime': timezone.make_aware(datetime.combine(today + timedelta(days=45), time(18, 0))),
            'end_datetime': timezone.make_aware(datetime.combine(today + timedelta(days=47), time(18, 0))),
            'registration_deadline': timezone.make_aware(datetime.combine(today + timedelta(days=30), time(23, 59))),
            'location': 'IIT Bombay, Mumbai',
            'banner_image': 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200',
            'prizes': [
                {'position': '1st Place', 'prize': '₹2,50,000 + Internship', 'description': 'Cash prize plus internship opportunities'},
                {'position': '2nd Place', 'prize': '₹1,50,000', 'description': 'Cash prize for second position'},
                {'position': '3rd Place', 'prize': '₹75,000', 'description': 'Cash prize for third position'}
            ],
            'benefits': ['Free meals and snacks', 'Mentorship from industry experts', 'Networking opportunities', 'Certificate of participation'],
            'rules': ['Teams of 2-5 members', 'All code must be written during event', 'Use any programming language', 'Submit project by deadline'],
            'judging_criteria': [
                {'criteria': 'Innovation', 'weight': '30%', 'description': 'How innovative and creative is the solution?'},
                {'criteria': 'Technical Implementation', 'weight': '25%', 'description': 'Quality of code and technical execution'},
                {'criteria': 'Impact', 'weight': '25%', 'description': 'Potential real-world impact of the solution'},
                {'criteria': 'Presentation', 'weight': '20%', 'description': 'Quality of project presentation and demo'}
            ],
            'is_featured': True,
            'is_published': True,
        },
        {
            'name': 'FinTech Revolution Hackathon',
            'description': 'Revolutionize financial services with cutting-edge technology',
            'content': 'Create innovative financial solutions that can transform how people manage money, invest, and access financial services. Open to developers, designers, and finance enthusiasts.',
            'topic': 'Financial Technology & Blockchain',
            'difficulty_level': 'advanced',
            'team_size': '2-3',
            'max_participants': 200,
            'start_datetime': timezone.make_aware(datetime.combine(today + timedelta(days=60), time(9, 0))),
            'end_datetime': timezone.make_aware(datetime.combine(today + timedelta(days=61), time(18, 0))),
            'registration_deadline': timezone.make_aware(datetime.combine(today + timedelta(days=45), time(23, 59))),
            'location': 'Virtual Event',
            'is_virtual': True,
            'banner_image': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200',
            'prizes': [
                {'position': '1st Place', 'prize': '₹3,00,000', 'description': 'Top prize for best financial innovation'},
                {'position': '2nd Place', 'prize': '₹2,00,000', 'description': 'Second place prize'},
                {'position': '3rd Place', 'prize': '₹1,00,000', 'description': 'Third place prize'}
            ],
            'benefits': ['Virtual participation', 'Expert mentorship', 'Investment opportunities', 'Global networking'],
            'is_featured': False,
            'is_published': True,
        }
    ]

    for hackathon_data in hackathons_data:
        hackathon = SharXathon.objects.create(**hackathon_data)
        print(f"✓ Created hackathon: {hackathon.name}")

def add_startup_stories():
    """Add sample Startup Stories"""
    print("\n--- Adding Startup Stories ---")
    StartupStory.objects.all().delete()

    stories_data = [
        {
            'heading': 'From Dorm Room to $50M Exit',
            'subheading': 'How two college friends built India\'s largest online tutoring platform',
            'slug': 'dorm-room-to-50m-exit',
            'summary': 'Two IIT graduates started with $500 in a college dorm and built a platform that now serves 2 million students across India.',
            'content': 'It all began in 2018 when Arjun and Vikram, both IIT Delhi graduates, noticed the lack of quality online education in India. Starting with just $500 from their savings, they built an MVP in 3 months and launched during the pandemic when online education became crucial.',
            'key_takeaways': ['Start with a real problem', 'Validate with real users early', 'Scale gradually but consistently', 'Never give up on your vision'],
            'challenges_faced': 'Initial funding challenges, competition from established players, technical scalability issues',
            'solutions_implemented': 'Bootstrapped for first year, focused on niche market, invested heavily in technology infrastructure',
            'industry': 'edtech',
            'stage': 'exit',
            'tags': 'education, online learning, entrepreneurship',
            'founder_name': 'Arjun Mehta & Vikram Singh',
            'company_name': 'EduTech Solutions',
            'founded_year': 2018,
            'featured_image': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800',
            'is_featured': True,
            'is_published': True,
        },
        {
            'heading': 'Sustainability Meets Technology',
            'subheading': 'Building eco-friendly solutions for urban waste management',
            'slug': 'sustainability-meets-technology',
            'summary': 'How a team of environmental engineers created smart waste management solutions that reduced urban waste by 60%.',
            'content': 'Recognizing the growing waste management crisis in Indian cities, the founders combined IoT technology with sustainable practices to create smart waste collection and recycling solutions.',
            'key_takeaways': ['Technology can solve environmental problems', 'Government partnerships are crucial', 'Sustainability sells itself', 'Impact investing is real'],
            'challenges_faced': 'High initial costs, regulatory hurdles, technology adoption in traditional sectors',
            'solutions_implemented': 'Strategic partnerships with municipal corporations, pilot programs in small cities first',
            'industry': 'cleantech',
            'stage': 'series_a',
            'tags': 'sustainability, IoT, waste management, smart cities',
            'founder_name': 'Priya Sharma',
            'company_name': 'EcoSmart Solutions',
            'founded_year': 2020,
            'featured_image': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800',
            'is_featured': True,
            'is_published': True,
        }
    ]

    for story_data in stories_data:
        story = StartupStory.objects.create(**story_data)
        print(f"✓ Created startup story: {story.heading}")

def add_talk_episodes():
    """Add sample Talk Episodes"""
    print("\n--- Adding Talk Episodes ---")
    TalkEpisode.objects.all().delete()

    episodes_data = [
        {
            'episode_number': 1,
            'title': 'Building Scalable Startups in India',
            'header': 'Lessons from a Decade of Entrepreneurship',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'In this inaugural episode, we sit down with Rajesh Kumar, founder of three successful startups, to discuss the challenges and opportunities of building scalable businesses in the Indian market.',
            'key_takeaways': ['Focus on unit economics from day one', 'Hire for culture fit first', 'Customer feedback is your best product manager', 'Cash flow management is critical'],
            'speaker_panels': [
                {
                    'name': 'Rajesh Kumar',
                    'title': 'Serial Entrepreneur & Investor',
                    'bio': 'Founder of 3 successful startups, angel investor, and mentor to 50+ startups',
                    'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
                    'social_links': {'linkedin': 'https://linkedin.com/in/rajesh-kumar', 'twitter': 'https://twitter.com/rajeshk'}
                }
            ],
            'published_at': timezone.make_aware(datetime.now() - timedelta(days=30)),
            'duration_minutes': 45,
            'is_published': True,
        },
        {
            'episode_number': 2,
            'title': 'AI in Healthcare: Revolution or Hype?',
            'header': 'Exploring the Future of Medical Technology',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'Dr. Anita Desai joins us to discuss how artificial intelligence is transforming healthcare delivery, from diagnostic tools to personalized treatment plans.',
            'key_takeaways': ['AI can improve diagnostic accuracy by 30%', 'Data privacy is the biggest challenge', 'Human-AI collaboration is key', 'Regulatory frameworks are evolving'],
            'speaker_panels': [
                {
                    'name': 'Dr. Anita Desai',
                    'title': 'Chief Medical Officer, HealthTech Solutions',
                    'bio': 'Former head of AI research at Apollo Hospitals, published 50+ papers on medical AI',
                    'avatar_url': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=200',
                    'social_links': {'linkedin': 'https://linkedin.com/in/dr-anita-desai'}
                }
            ],
            'published_at': timezone.make_aware(datetime.now() - timedelta(days=15)),
            'duration_minutes': 52,
            'is_published': True,
        }
    ]

    for episode_data in episodes_data:
        episode = TalkEpisode.objects.create(**episode_data)
        print(f"✓ Created talk episode: {episode.title}")

def add_tech_news():
    """Add sample Tech News"""
    print("\n--- Adding Tech News ---")
    TechNews.objects.all().delete()

    news_data = [
        {
            'title': 'OpenAI Launches GPT-5 with Multimodal Capabilities',
            'subtitle': 'Next-generation AI model can process text, images, and code simultaneously',
            'excerpt': 'OpenAI has unveiled GPT-5, their most advanced AI model yet, featuring unprecedented multimodal capabilities that can understand and generate content across text, images, and programming code.',
            'content': 'In a groundbreaking announcement, OpenAI revealed GPT-5, marking a significant leap forward in artificial intelligence capabilities. The new model can seamlessly process and generate content across multiple modalities including text, images, and code, opening up new possibilities for creative and technical applications.',
            'category': 'ai_ml',
            'tags': ['OpenAI', 'GPT-5', 'artificial intelligence', 'multimodal AI'],
            'priority': 'breaking',
            'featured_image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
            'author_name': 'Sarah Chen',
            'read_time_minutes': 5,
            'is_featured': True,
            'is_published': True,
            'is_breaking': True,
            'meta_description': 'OpenAI launches GPT-5 with revolutionary multimodal capabilities',
        },
        {
            'title': 'SpaceX Successfully Lands Starship on Mars',
            'subtitle': 'Historic achievement marks new era in interplanetary exploration',
            'excerpt': 'SpaceX has achieved the first successful landing of a Starship spacecraft on Mars, paving the way for future crewed missions and permanent human settlement on the Red Planet.',
            'content': 'After years of development and testing, SpaceX\'s Starship has successfully touched down on the Martian surface. This historic achievement represents a major milestone in humanity\'s quest to become a multi-planetary species.',
            'category': 'space',
            'tags': ['SpaceX', 'Starship', 'Mars', 'space exploration'],
            'priority': 'high',
            'featured_image': 'https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800',
            'author_name': 'Mike Rodriguez',
            'read_time_minutes': 4,
            'is_featured': True,
            'is_published': True,
            'meta_description': 'SpaceX achieves historic Starship landing on Mars',
        },
        {
            'title': 'Quantum Computing Breakthrough Achieved',
            'subtitle': 'Scientists demonstrate error-corrected quantum computer with 100+ qubits',
            'excerpt': 'A team of researchers has successfully demonstrated a quantum computer with over 100 error-corrected qubits, bringing practical quantum computing applications closer to reality.',
            'content': 'In a major breakthrough, scientists at Quantum Labs have developed a quantum computer capable of maintaining quantum states for extended periods, overcoming one of the biggest challenges in quantum computing.',
            'category': 'quantum',
            'tags': ['quantum computing', 'error correction', 'qubits', 'breakthrough'],
            'priority': 'high',
            'featured_image': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800',
            'author_name': 'Dr. Lisa Wang',
            'read_time_minutes': 6,
            'is_featured': False,
            'is_published': True,
            'meta_description': 'Major quantum computing breakthrough with error-corrected 100+ qubit system',
        }
    ]

    for news_item in news_data:
        news = TechNews.objects.create(**news_item)
        print(f"✓ Created tech news: {news.title}")

def add_youtube_videos():
    """Add sample YouTube Videos"""
    print("\n--- Adding YouTube Videos ---")
    YouTubeVideo.objects.all().delete()

    videos_data = [
        {
            'title': 'Building Your First Startup: Complete Guide',
            'description': 'A comprehensive guide for aspiring entrepreneurs on how to validate ideas, build MVPs, and launch successful startups.',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'video_type': 'video',
            'category': 'startup_stories',
            'tags': 'startup, entrepreneurship, guide, beginners',
            'is_featured': True,
            'is_published': True,
            'display_order': 1,
            'duration': '15:30',
            'view_count': 125000,
            'published_date': date.today() - timedelta(days=7),
        },
        {
            'title': 'AI Tools Every Developer Should Know in 2025',
            'description': 'Explore the most powerful AI tools and frameworks that are revolutionizing software development in 2025.',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'video_type': 'video',
            'category': 'tutorials',
            'tags': 'AI, development tools, productivity, 2025',
            'is_featured': True,
            'is_published': True,
            'display_order': 2,
            'duration': '22:45',
            'view_count': 89000,
            'published_date': date.today() - timedelta(days=3),
        },
        {
            'title': 'NeoSharX Hackathon Highlights #2024',
            'description': 'Amazing projects and innovations from our annual hackathon. Watch the winning teams present their solutions!',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'video_type': 'video',
            'category': 'hackathons',
            'tags': 'hackathon, innovation, winners, showcase',
            'is_featured': False,
            'is_published': True,
            'display_order': 3,
            'duration': '12:15',
            'view_count': 67000,
            'published_date': date.today() - timedelta(days=14),
        },
        {
            'title': 'Quick Tips for Startup Pitching',
            'description': '5-minute guide to crafting compelling startup pitches that attract investors.',
            'youtube_url': 'https://youtube.com/shorts/dQw4w9WgXcQ',
            'video_type': 'short',
            'category': 'startup_stories',
            'tags': 'pitching, investors, startups, tips',
            'is_featured': False,
            'is_published': True,
            'display_order': 4,
            'duration': '0:45',
            'view_count': 45000,
            'published_date': date.today() - timedelta(days=1),
        }
    ]

    for video_data in videos_data:
        video = YouTubeVideo.objects.create(**video_data)
        print(f"✓ Created YouTube video: {video.title}")

def main():
    """Main function to run all data creation"""
    print("🚀 Starting comprehensive NeoSharX data population...")

    # Create admin user first
    admin_user = create_admin_user()

    # Add data to all tables
    add_events()
    add_neo_projects()
    add_neo_stories()
    add_robotics_news()
    add_sharxathons()
    add_startup_stories()
    add_talk_episodes()
    add_tech_news()
    add_youtube_videos()

    print("\n✅ All sample data has been successfully added to NeoSharX backend!")
    print("\n📊 Summary:")
    print(f"   • Events: {Event.objects.count()}")
    print(f"   • Neo Projects: {NeoProject.objects.count()}")
    print(f"   • Neo Stories: {NeoStory.objects.count()}")
    print(f"   • Robotics News: {RoboticsNews.objects.count()}")
    print(f"   • SharXathons: {SharXathon.objects.count()}")
    print(f"   • Startup Stories: {StartupStory.objects.count()}")
    print(f"   • Talk Episodes: {TalkEpisode.objects.count()}")
    print(f"   • Tech News: {TechNews.objects.count()}")
    print(f"   • YouTube Videos: {YouTubeVideo.objects.count()}")

    print("\n🔄 Next Steps:")
    print("1. Run the Django development server: python manage.py runserver")
    print("2. Access the Django admin at: http://localhost:8000/admin/")
    print("3. Login with: admin / admin123")
    print("4. Check that all data appears in the admin interface")
    print("5. Test the frontend API endpoints to ensure data is being served correctly")
    print("6. Update frontend components to display the new data")
    print("7. Test the complete user flow from frontend to backend")

if __name__ == '__main__':
    main()
