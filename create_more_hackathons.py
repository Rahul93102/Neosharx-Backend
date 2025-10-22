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

def create_more_hackathons():
    print("Creating additional hackathon data...")
    
    # Hackathon 1: Blockchain DeFi Challenge
    hackathon1 = SharXathon.objects.create(
        name="Blockchain DeFi Challenge 2025",
        description="Build decentralized finance applications that democratize access to financial services.",
        content="Join the future of finance! This hackathon challenges developers to create innovative DeFi solutions using blockchain technology. Build applications that can provide financial services to the unbanked, create new lending protocols, or develop decentralized exchanges. Teams will have access to leading blockchain platforms and mentorship from DeFi pioneers.",
        location="Austin, TX",
        is_virtual=False,
        start_datetime=timezone.now() + timedelta(days=45),
        end_datetime=timezone.now() + timedelta(days=47),
        registration_deadline=timezone.now() + timedelta(days=35),
        banner_image="https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&h=400&fit=crop",
        topic="Decentralized Finance & Blockchain",
        difficulty_level="advanced",
        team_size="2-4",
        max_participants=120,
        current_participants=67,
        prizes=[
            {"position": "1st Place", "prize": "$30,000", "description": "Winner receives funding and incubator spot"},
            {"position": "2nd Place", "prize": "$15,000", "description": "Second place gets cash and mentorship"},
            {"position": "3rd Place", "prize": "$8,000", "description": "Third place receives cash prize"},
            {"position": "Best Innovation", "prize": "$5,000", "description": "Most innovative solution"}
        ],
        benefits=[
            "Travel reimbursement up to $500",
            "Hotel accommodation provided",
            "Free meals and refreshments",
            "Access to blockchain infrastructure",
            "Mentorship from Web3 experts",
            "Networking with VCs and investors"
        ],
        rules=[
            "Teams of 2-4 members",
            "Must use Ethereum, Solana, or Polygon",
            "Code must be open source",
            "Deploy working smart contracts",
            "Present live demo with test transactions"
        ],
        organizer_name="DeFi Foundation",
        organizer_email="events@defifoundation.org",
        website_url="https://defi-challenge.com",
        status="registration_open",
        is_featured=True,
        is_published=True,
        judging_criteria=[
            {"criteria": "Innovation", "weight": "30%", "description": "Originality of the DeFi solution"},
            {"criteria": "Technical Excellence", "weight": "25%", "description": "Code quality and smart contract security"},
            {"criteria": "User Experience", "weight": "20%", "description": "Ease of use and interface design"},
            {"criteria": "Business Viability", "weight": "15%", "description": "Market potential and sustainability"},
            {"criteria": "Presentation", "weight": "10%", "description": "Quality of pitch and demo"}
        ]
    )
    print(f"✅ Created: {hackathon1.name}")
    
    # Hackathon 2: Climate Tech Innovation
    hackathon2 = SharXathon.objects.create(
        name="Climate Tech Innovation Summit 2025",
        description="Develop technology solutions to combat climate change and promote environmental sustainability.",
        content="The planet needs innovative solutions, and we need your help! This hackathon brings together developers, scientists, and environmental advocates to create technology that addresses climate change. Whether it's carbon tracking, renewable energy optimization, or sustainable agriculture tech - your solution could make a real impact.",
        location="Seattle, WA",
        is_virtual=False,
        start_datetime=timezone.now() + timedelta(days=60),
        end_datetime=timezone.now() + timedelta(days=62),
        registration_deadline=timezone.now() + timedelta(days=50),
        banner_image="https://images.unsplash.com/photo-1569163139394-de4798aa62b6?w=800&h=400&fit=crop",
        topic="Climate Technology & Sustainability",
        difficulty_level="intermediate",
        team_size="3-5",
        max_participants=250,
        current_participants=123,
        prizes=[
            {"position": "1st Place", "prize": "$25,000", "description": "Winner receives grant and partnership opportunity"},
            {"position": "2nd Place", "prize": "$15,000", "description": "Second place with seed funding support"},
            {"position": "3rd Place", "prize": "$10,000", "description": "Third place cash prize"},
            {"position": "People's Choice", "prize": "$5,000", "description": "Community favorite"}
        ],
        benefits=[
            "Free accommodation for out-of-state participants",
            "All meals and snacks provided",
            "Access to environmental datasets",
            "Mentorship from climate scientists",
            "Workshop on carbon footprint calculation",
            "Certificate of participation"
        ],
        rules=[
            "Teams of 3-5 members",
            "Solution must address a real climate challenge",
            "Use sustainable coding practices",
            "Data sources must be cited",
            "Final presentation must include impact metrics"
        ],
        organizer_name="Green Tech Alliance",
        organizer_email="hackathon@greentechalliance.org",
        website_url="https://climate-tech-summit.org",
        status="registration_open",
        is_featured=True,
        is_published=True,
        judging_criteria=[
            {"criteria": "Environmental Impact", "weight": "35%", "description": "Potential to reduce carbon emissions or environmental harm"},
            {"criteria": "Innovation", "weight": "25%", "description": "Creative approach to solving climate challenges"},
            {"criteria": "Scalability", "weight": "20%", "description": "Ability to scale solution globally"},
            {"criteria": "Technical Implementation", "weight": "15%", "description": "Quality of technical execution"},
            {"criteria": "Presentation", "weight": "5%", "description": "Communication of ideas"}
        ]
    )
    print(f"✅ Created: {hackathon2.name}")
    
    # Hackathon 3: Healthcare AI Challenge
    hackathon3 = SharXathon.objects.create(
        name="Healthcare AI Revolution 2025",
        description="Apply artificial intelligence to improve patient care, diagnostics, and healthcare accessibility.",
        content="Transform healthcare with AI! This hackathon challenges participants to create AI-powered solutions that improve patient outcomes, streamline diagnostics, or increase access to healthcare services. Work with real medical datasets and get guidance from healthcare professionals and AI experts.",
        location="Boston, MA",
        is_virtual=False,
        start_datetime=timezone.now() + timedelta(days=75),
        end_datetime=timezone.now() + timedelta(days=77),
        registration_deadline=timezone.now() + timedelta(days=65),
        banner_image="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&h=400&fit=crop",
        topic="Healthcare AI & Medical Technology",
        difficulty_level="advanced",
        team_size="3-4",
        max_participants=150,
        current_participants=89,
        prizes=[
            {"position": "1st Place", "prize": "$50,000", "description": "Winner gets funding and hospital partnership"},
            {"position": "2nd Place", "prize": "$25,000", "description": "Second place with clinical trial opportunity"},
            {"position": "3rd Place", "prize": "$15,000", "description": "Third place cash prize"},
            {"position": "Best Diagnostic Tool", "prize": "$10,000", "description": "Best AI diagnostic solution"}
        ],
        benefits=[
            "Access to anonymized medical datasets",
            "Mentorship from doctors and AI researchers",
            "GPU computing resources provided",
            "All meals and accommodation included",
            "Certificate and LinkedIn recognition",
            "Opportunity for hospital pilot programs"
        ],
        rules=[
            "Teams of 3-4 members including at least one medical professional or student",
            "HIPAA compliance required for all solutions",
            "Must use ethical AI practices",
            "Data privacy must be maintained",
            "Solution must be clinically viable"
        ],
        organizer_name="HealthTech Innovation Lab",
        organizer_email="events@healthtechinnovation.org",
        website_url="https://healthcare-ai-challenge.org",
        status="registration_open",
        is_featured=True,
        is_published=True,
        judging_criteria=[
            {"criteria": "Clinical Impact", "weight": "30%", "description": "Potential to improve patient outcomes"},
            {"criteria": "AI Innovation", "weight": "25%", "description": "Novel use of AI/ML techniques"},
            {"criteria": "Safety & Ethics", "weight": "20%", "description": "Ethical AI practices and patient safety"},
            {"criteria": "Technical Excellence", "weight": "15%", "description": "Code quality and model performance"},
            {"criteria": "Scalability", "weight": "10%", "description": "Ability to deploy in real healthcare settings"}
        ]
    )
    print(f"✅ Created: {hackathon3.name}")
    
    # Hackathon 4: EdTech Innovation Challenge
    hackathon4 = SharXathon.objects.create(
        name="EdTech Innovation Challenge 2025",
        description="Create educational technology that makes learning more accessible, engaging, and effective for all students.",
        content="Education is the key to the future! This hackathon focuses on creating innovative EdTech solutions that can transform how students learn. From AI tutors to gamified learning platforms, from accessibility tools to virtual classrooms - help us reimagine education for the digital age.",
        location="Virtual Event",
        is_virtual=True,
        start_datetime=timezone.now() + timedelta(days=90),
        end_datetime=timezone.now() + timedelta(days=92),
        registration_deadline=timezone.now() + timedelta(days=80),
        banner_image="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=400&fit=crop",
        topic="Educational Technology & Learning Innovation",
        difficulty_level="beginner",
        team_size="2-5",
        max_participants=300,
        current_participants=145,
        prizes=[
            {"position": "1st Place", "prize": "$20,000", "description": "Winner gets funding and school pilot program"},
            {"position": "2nd Place", "prize": "$12,000", "description": "Second place with EdTech accelerator spot"},
            {"position": "3rd Place", "prize": "$8,000", "description": "Third place cash prize"},
            {"position": "Best K-12 Solution", "prize": "$5,000", "description": "Best solution for primary education"},
            {"position": "Best Accessibility Tool", "prize": "$5,000", "description": "Best tool for students with disabilities"}
        ],
        benefits=[
            "Free access to educational APIs and tools",
            "Mentorship from teachers and EdTech founders",
            "Workshops on instructional design",
            "Certificate of participation",
            "Opportunity to pilot in real schools",
            "Networking with education leaders"
        ],
        rules=[
            "Teams of 2-5 members",
            "Solution must be education-focused",
            "Consider accessibility for all learners",
            "Include a teacher/student testing phase",
            "Provide usage documentation"
        ],
        organizer_name="Global EdTech Foundation",
        organizer_email="hackathon@edtechglobal.org",
        website_url="https://edtech-innovation.org",
        status="registration_open",
        is_featured=False,
        is_published=True,
        judging_criteria=[
            {"criteria": "Educational Impact", "weight": "30%", "description": "Potential to improve learning outcomes"},
            {"criteria": "Innovation", "weight": "25%", "description": "Creative approach to education challenges"},
            {"criteria": "Usability", "weight": "20%", "description": "Ease of use for students and teachers"},
            {"criteria": "Accessibility", "weight": "15%", "description": "Inclusive design for diverse learners"},
            {"criteria": "Scalability", "weight": "10%", "description": "Ability to reach many students"}
        ]
    )
    print(f"✅ Created: {hackathon4.name}")
    
    # Hackathon 5: Cybersecurity Defense Challenge
    hackathon5 = SharXathon.objects.create(
        name="CyberShield Defense Challenge 2025",
        description="Build innovative cybersecurity solutions to protect against emerging digital threats.",
        content="The digital world faces constant threats. This elite cybersecurity hackathon brings together white-hat hackers, security researchers, and developers to create next-generation security solutions. From threat detection systems to secure authentication methods - help us build a safer digital future.",
        location="Las Vegas, NV",
        is_virtual=False,
        start_datetime=timezone.now() + timedelta(days=105),
        end_datetime=timezone.now() + timedelta(days=107),
        registration_deadline=timezone.now() + timedelta(days=95),
        banner_image="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=400&fit=crop",
        topic="Cybersecurity & Digital Defense",
        difficulty_level="advanced",
        team_size="2-3",
        max_participants=100,
        current_participants=78,
        prizes=[
            {"position": "1st Place", "prize": "$40,000", "description": "Winner gets funding and security firm partnership"},
            {"position": "2nd Place", "prize": "$20,000", "description": "Second place with enterprise pilot opportunity"},
            {"position": "3rd Place", "prize": "$12,000", "description": "Third place cash prize"},
            {"position": "Best Threat Detection", "prize": "$8,000", "description": "Best AI-powered threat detection system"}
        ],
        benefits=[
            "Full travel and accommodation covered",
            "Access to enterprise security datasets",
            "Mentorship from security experts",
            "Premium security tools and licenses",
            "All meals and conference pass included",
            "Job placement assistance"
        ],
        rules=[
            "Teams of 2-3 members",
            "Ethical hacking principles must be followed",
            "No malicious code allowed",
            "Solutions must be defensive, not offensive",
            "Document security architecture"
        ],
        organizer_name="CyberShield Security",
        organizer_email="hackathon@cybershield-sec.com",
        website_url="https://cybershield-challenge.com",
        status="registration_open",
        is_featured=True,
        is_published=True,
        judging_criteria=[
            {"criteria": "Security Effectiveness", "weight": "35%", "description": "Ability to prevent/detect threats"},
            {"criteria": "Innovation", "weight": "25%", "description": "Novel security approaches"},
            {"criteria": "Performance", "weight": "20%", "description": "Speed and efficiency of solution"},
            {"criteria": "Scalability", "weight": "15%", "description": "Enterprise-grade scalability"},
            {"criteria": "Documentation", "weight": "5%", "description": "Quality of technical documentation"}
        ]
    )
    print(f"✅ Created: {hackathon5.name}")
    
    print("\n🎉 Successfully created 5 additional hackathons!")
    print(f"Total hackathons in database: {SharXathon.objects.count()}")

if __name__ == '__main__':
    create_more_hackathons()
