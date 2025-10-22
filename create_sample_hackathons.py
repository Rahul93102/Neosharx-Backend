#!/usr/bin/env python
import os
import sys
import django
from datetime import timedelta

# Add the project directory to Python path
sys.path.append('/Users/vishaljha/neosharx/Backend flow')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Setup Django
django.setup()

from django.utils import timezone
from authentication.models import SharXathon

def create_sample_hackathons():
    # Create sample hackathon 1
    hackathon1 = SharXathon.objects.create(
        name="AI Innovation Challenge 2024",
        description="Build AI solutions that solve real-world problems in healthcare, education, or sustainability.",
        content="Join us for an exciting 48-hour hackathon where teams will develop innovative AI solutions to address pressing global challenges in healthcare, education, and sustainability. This event brings together the brightest minds in AI to create solutions that can make a real difference in the world.",
        location="Virtual Event",
        is_virtual=True,
        start_datetime=timezone.now() + timedelta(days=30),
        end_datetime=timezone.now() + timedelta(days=32),
        registration_deadline=timezone.now() + timedelta(days=25),
        banner_image="https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        topic="Artificial Intelligence for Social Good",
        difficulty_level="intermediate",
        team_size="4-5",
        max_participants=200,
        current_participants=45,
        prizes=[
            {"position": "1st Place", "prize": "$10,000", "description": "Winner gets cash prize and mentorship"},
            {"position": "2nd Place", "prize": "$5,000", "description": "Second place team receives cash prize"},
            {"position": "3rd Place", "prize": "$2,500", "description": "Third place team receives cash prize"}
        ],
        benefits=[
            "Free meals and snacks throughout the event",
            "Networking opportunities with industry professionals",
            "Workshops and mentorship sessions",
            "Certificate of participation",
            "Access to premium APIs and tools"
        ],
        rules=[
            "Teams must have 4-5 members",
            "All code must be written during the event",
            "Use any programming language or framework",
            "Submit project by the deadline",
            "Final presentation is mandatory"
        ],
        judging_criteria=[
            {"criteria": "Innovation", "weight": "30%", "description": "How innovative and creative is the solution?"},
            {"criteria": "Technical Implementation", "weight": "25%", "description": "Quality of code and technical execution"},
            {"criteria": "Social Impact", "weight": "25%", "description": "Potential to create positive social impact"},
            {"criteria": "Presentation", "weight": "20%", "description": "Quality of final presentation and demo"}
        ],
        organizer_name="NeoSharX Team",
        organizer_email="hackathon@neosharx.com",
        website_url="https://neosharx.com",
        status="registration_open",
        is_featured=True,
        is_published=True
    )
    
    # Create sample hackathon 2
    hackathon2 = SharXathon.objects.create(
        name="Web3 Builder Bootcamp",
        description="Create decentralized applications and smart contracts using modern Web3 technologies.",
        content="Dive into the world of Web3 and blockchain technology. This intensive bootcamp will challenge you to build decentralized applications, smart contracts, and innovative blockchain solutions.",
        location="San Francisco, CA",
        is_virtual=False,
        start_datetime=timezone.now() + timedelta(days=60),
        end_datetime=timezone.now() + timedelta(days=62),
        registration_deadline=timezone.now() + timedelta(days=50),
        banner_image="https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        topic="Web3 & Blockchain Development",
        difficulty_level="advanced",
        team_size="individual",
        max_participants=100,
        current_participants=23,
        prizes=[
            {"position": "1st Place", "prize": "$25,000", "description": "Winner gets cash prize and accelerator program"},
            {"position": "2nd Place", "prize": "$15,000", "description": "Second place receives cash prize and mentorship"},
            {"position": "3rd Place", "prize": "$10,000", "description": "Third place receives cash prize"}
        ],
        benefits=[
            "Accommodation and meals provided",
            "Access to top blockchain developers",
            "Hands-on workshops with Web3 tools",
            "Networking with VCs and investors",
            "Job placement assistance"
        ],
        rules=[
            "Individual participation only",
            "Must have prior blockchain experience",
            "Use Ethereum, Solana, or Polygon",
            "Deploy working dApp by deadline",
            "Present live demo to judges"
        ],
        organizer_name="Web3 Foundation",
        organizer_email="bootcamp@web3foundation.org",
        status="upcoming",
        is_featured=True,
        is_published=True
    )
    
    # Create sample hackathon 3
    hackathon3 = SharXathon.objects.create(
        name="Startup Weekend 2024",
        description="Turn your startup idea into reality in just 54 hours with mentorship and networking.",
        content="The ultimate startup experience! Pitch your idea, form a team, and build a startup in just one weekend. Get mentorship from successful entrepreneurs and present to real investors.",
        location="New York, NY",
        is_virtual=False,  
        start_datetime=timezone.now() - timedelta(days=2),
        end_datetime=timezone.now() + timedelta(hours=10),
        registration_deadline=timezone.now() - timedelta(days=7),
        banner_image="https://images.unsplash.com/photo-1504384308090-c894fdcc538d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        topic="Entrepreneurship & Startup Development",
        difficulty_level="beginner",
        team_size="2-3",
        max_participants=150,
        current_participants=150,
        prizes=[
            {"position": "1st Place", "prize": "$15,000", "description": "Winner gets seed funding and incubator access"},
            {"position": "2nd Place", "prize": "$8,000", "description": "Second place receives cash prize"},
            {"position": "People's Choice", "prize": "$5,000", "description": "Audience favorite receives special prize"}
        ],
        benefits=[
            "Free meals throughout the weekend",
            "Mentorship from successful entrepreneurs",  
            "Networking with investors and VCs",
            "Legal and business development workshops",
            "Pitch coaching and feedback"
        ],
        rules=[
            "Teams of 2-3 members preferred",
            "Must pitch idea on Friday evening",
            "Build MVP over the weekend",
            "Final pitch on Sunday evening",
            "No pre-existing code allowed"
        ],
        organizer_name="Startup Weekend NYC",
        organizer_email="nyc@startupweekend.org",
        status="ongoing", 
        is_featured=False,
        is_published=True
    )
    
    print(f"Created hackathon 1: {hackathon1.name} (slug: {hackathon1.slug})")
    print(f"Created hackathon 2: {hackathon2.name} (slug: {hackathon2.slug})")
    print(f"Created hackathon 3: {hackathon3.name} (slug: {hackathon3.slug})")
    print("Sample hackathons created successfully!")

if __name__ == "__main__":
    create_sample_hackathons()