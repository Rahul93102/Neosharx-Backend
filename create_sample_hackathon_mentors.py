#!/usr/bin/env python
"""
Script to create sample hackathon mentors and assign them to hackathons
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import HackathonMentor, HackathonMentorLink, SharXathon

def create_sample_mentors():
    """Create sample hackathon mentors"""

    mentors_data = [
        {
            'name': 'Sarah Chen',
            'slug': 'sarah-chen',
            'bio': 'Senior Software Engineer at Google with 8+ years of experience in AI/ML and distributed systems.',
            'avatar': 'https://i.pravatar.cc/150?img=1',
            'email': 'sarah.chen@example.com',
            'linkedin_url': 'https://linkedin.com/in/sarahchen',
            'github_url': 'https://github.com/sarahchen',
            'twitter_url': 'https://twitter.com/sarahchen',
            'website_url': 'https://sarahchen.dev',
            'title': 'Senior Software Engineer',
            'company': 'Google',
            'experience_years': 8,
            'skills': ['Python', 'TensorFlow', 'Kubernetes', 'React', 'Node.js'],
            'expertise_areas': ['Machine Learning', 'Distributed Systems', 'Web Development'],
            'is_featured': True,
            'is_active': True,
        },
        {
            'name': 'Marcus Rodriguez',
            'slug': 'marcus-rodriguez',
            'bio': 'Full-stack developer and startup mentor. Built 3 successful startups and mentored 50+ teams.',
            'avatar': 'https://i.pravatar.cc/150?img=2',
            'email': 'marcus@example.com',
            'linkedin_url': 'https://linkedin.com/in/marcusrodriguez',
            'github_url': 'https://github.com/marcusrodriguez',
            'website_url': 'https://marcusrodriguez.com',
            'title': 'Startup Mentor & Developer',
            'company': 'TechStars',
            'experience_years': 12,
            'skills': ['JavaScript', 'Python', 'AWS', 'Docker', 'MongoDB'],
            'expertise_areas': ['Full-stack Development', 'Startup Growth', 'Product Strategy'],
            'is_featured': True,
            'is_active': True,
        },
        {
            'name': 'Dr. Priya Patel',
            'slug': 'priya-patel',
            'bio': 'PhD in Computer Science, specializing in computer vision and deep learning. Research scientist at MIT.',
            'avatar': 'https://i.pravatar.cc/150?img=3',
            'email': 'priya.patel@mit.edu',
            'linkedin_url': 'https://linkedin.com/in/priyapatel',
            'github_url': 'https://github.com/priyapatel',
            'website_url': 'https://priyapatel.research.mit.edu',
            'title': 'Research Scientist',
            'company': 'MIT',
            'experience_years': 10,
            'skills': ['Computer Vision', 'Deep Learning', 'PyTorch', 'OpenCV', 'Research'],
            'expertise_areas': ['Computer Vision', 'AI Research', 'Academic Mentoring'],
            'is_featured': True,
            'is_active': True,
        },
        {
            'name': 'Alex Thompson',
            'slug': 'alex-thompson',
            'bio': 'DevOps engineer and cloud architect. AWS certified solutions architect with expertise in scalable systems.',
            'avatar': 'https://i.pravatar.cc/150?img=4',
            'email': 'alex.thompson@example.com',
            'linkedin_url': 'https://linkedin.com/in/alexthompson',
            'github_url': 'https://github.com/alexthompson',
            'twitter_url': 'https://twitter.com/alexthompson',
            'title': 'Cloud Architect',
            'company': 'Amazon Web Services',
            'experience_years': 9,
            'skills': ['AWS', 'Terraform', 'Docker', 'Kubernetes', 'CI/CD'],
            'expertise_areas': ['Cloud Architecture', 'DevOps', 'Infrastructure as Code'],
            'is_featured': False,
            'is_active': True,
        },
        {
            'name': 'Lisa Wang',
            'slug': 'lisa-wang',
            'bio': 'UX/UI designer and product manager. Passionate about creating user-centered digital experiences.',
            'avatar': 'https://i.pravatar.cc/150?img=5',
            'email': 'lisa.wang@example.com',
            'linkedin_url': 'https://linkedin.com/in/lisawang',
            'website_url': 'https://lisawang.design',
            'title': 'Product Designer',
            'company': 'Adobe',
            'experience_years': 7,
            'skills': ['Figma', 'Sketch', 'Adobe XD', 'User Research', 'Prototyping'],
            'expertise_areas': ['UX Design', 'Product Management', 'User Research'],
            'is_featured': False,
            'is_active': True,
        }
    ]

    mentors = []
    for mentor_data in mentors_data:
        mentor, created = HackathonMentor.objects.get_or_create(
            slug=mentor_data['slug'],
            defaults=mentor_data
        )
        if created:
            print(f"Created mentor: {mentor.name}")
        else:
            print(f"Mentor already exists: {mentor.name}")
        mentors.append(mentor)

    # Create additional links for mentors
    mentor_links_data = [
        {
            'mentor_slug': 'sarah-chen',
            'title': 'Resume/CV',
            'url': 'https://sarahchen.dev/resume.pdf',
            'link_type': 'resume',
            'description': 'My professional resume',
            'order': 1,
        },
        {
            'mentor_slug': 'sarah-chen',
            'title': 'Research Papers',
            'url': 'https://scholar.google.com/sarahchen',
            'link_type': 'website',
            'description': 'My published research papers',
            'order': 2,
        },
        {
            'mentor_slug': 'marcus-rodriguez',
            'title': 'Portfolio',
            'url': 'https://marcusrodriguez.com/portfolio',
            'link_type': 'portfolio',
            'description': 'My startup portfolio and projects',
            'order': 1,
        },
        {
            'mentor_slug': 'marcus-rodriguez',
            'title': 'Blog',
            'url': 'https://marcusrodriguez.com/blog',
            'link_type': 'blog',
            'description': 'My thoughts on startups and technology',
            'order': 2,
        },
        {
            'mentor_slug': 'priya-patel',
            'title': 'Research Publications',
            'url': 'https://priyapatel.research.mit.edu/publications',
            'link_type': 'website',
            'description': 'My academic publications and research',
            'order': 1,
        },
        {
            'mentor_slug': 'alex-thompson',
            'title': 'AWS Certifications',
            'url': 'https://aws.amazon.com/certifications/alex-thompson',
            'link_type': 'website',
            'description': 'My AWS certifications and achievements',
            'order': 1,
        },
        {
            'mentor_slug': 'lisa-wang',
            'title': 'Design Portfolio',
            'url': 'https://lisawang.design/portfolio',
            'link_type': 'portfolio',
            'description': 'My design work and case studies',
            'order': 1,
        },
        {
            'mentor_slug': 'lisa-wang',
            'title': 'Dribbble',
            'url': 'https://dribbble.com/lisawang',
            'link_type': 'social',
            'description': 'My design inspiration and work',
            'order': 2,
        }
    ]

    for link_data in mentor_links_data:
        mentor = HackathonMentor.objects.get(slug=link_data['mentor_slug'])
        link, created = HackathonMentorLink.objects.get_or_create(
            mentor=mentor,
            title=link_data['title'],
            defaults={
                'url': link_data['url'],
                'link_type': link_data['link_type'],
                'description': link_data['description'],
                'order': link_data['order'],
                'is_active': True,
            }
        )
        if created:
            print(f"Created link for {mentor.name}: {link.title}")
        else:
            print(f"Link already exists for {mentor.name}: {link.title}")

    # Assign mentors to hackathons
    try:
        hackathons = SharXathon.objects.filter(is_published=True)[:3]  # Get first 3 published hackathons
        for hackathon in hackathons:
            # Assign 2-3 random mentors to each hackathon
            import random
            selected_mentors = random.sample(mentors, min(len(mentors), random.randint(2, 3)))
            hackathon.mentors.set(selected_mentors)
            hackathon.save()
            print(f"Assigned mentors to hackathon: {hackathon.name}")
            for mentor in selected_mentors:
                print(f"  - {mentor.name}")
    except Exception as e:
        print(f"Error assigning mentors to hackathons: {e}")

    print("\nSample mentors and links created successfully!")

if __name__ == '__main__':
    create_sample_mentors()