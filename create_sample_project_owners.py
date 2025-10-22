#!/usr/bin/env python
"""
Script to create sample project owners and links for testing
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import ProjectOwner, ProjectLink, NeoProject

def create_sample_owners():
    """Create sample project owners"""
    owners_data = [
        {
            'name': 'Alex Johnson',
            'slug': 'alex-johnson',
            'bio': 'Full-stack developer and blockchain enthusiast with 8+ years of experience in web technologies and decentralized systems.',
            'email': 'alex@blockchainvoting.com',
            'linkedin_url': 'https://linkedin.com/in/alexjohnson',
            'github_url': 'https://github.com/alexj',
            'title': 'Senior Software Engineer',
            'company': 'Blockchain Solutions Inc.',
            'skills': ['Ethereum', 'Solidity', 'React', 'Node.js', 'Python'],
            'interests': ['Blockchain', 'Cryptocurrency', 'Web3', 'Open Source'],
            'is_featured': True
        },
        {
            'name': 'Sarah Chen',
            'slug': 'sarah-chen',
            'bio': 'AI/ML engineer passionate about creating intelligent systems that solve real-world problems.',
            'email': 'sarah@neosharx.com',
            'linkedin_url': 'https://linkedin.com/in/sarahchen',
            'github_url': 'https://github.com/sarahc',
            'title': 'AI Engineer',
            'company': 'NeoSharX',
            'skills': ['Python', 'TensorFlow', 'React', 'Django', 'Machine Learning'],
            'interests': ['AI Ethics', 'Computer Vision', 'Natural Language Processing'],
            'is_featured': True
        },
        {
            'name': 'DataTech Solutions',
            'slug': 'datatech-solutions',
            'bio': 'Leading provider of data analytics and machine learning solutions for enterprise clients.',
            'email': 'team@datatech.com',
            'linkedin_url': 'https://linkedin.com/company/datatech',
            'github_url': 'https://github.com/datatech',
            'title': 'Data Science Team',
            'company': 'DataTech Solutions',
            'skills': ['Python', 'Scikit-learn', 'TensorFlow', 'PostgreSQL', 'Docker'],
            'interests': ['Big Data', 'Analytics', 'Machine Learning', 'Cloud Computing'],
            'is_featured': False
        }
    ]

    owners = []
    for owner_data in owners_data:
        owner, created = ProjectOwner.objects.get_or_create(
            slug=owner_data['slug'],
            defaults=owner_data
        )
        if created:
            print(f"Created project owner: {owner.name}")
        else:
            print(f"Project owner already exists: {owner.name}")
        owners.append(owner)

    return owners

def create_sample_links():
    """Create sample project links"""
    # Get projects
    projects = NeoProject.objects.filter(is_published=True)[:3]  # Get first 3 projects

    links_data = [
        {
            'project_slug': 'ai-powered-task-manager',
            'links': [
                {
                    'title': 'Live Demo',
                    'url': 'https://ai-taskmanager-demo.neosharx.com',
                    'link_type': 'demo',
                    'description': 'Try the AI-powered task manager live',
                    'order': 1
                },
                {
                    'title': 'API Documentation',
                    'url': 'https://api.neosharx.com/taskmanager',
                    'link_type': 'api',
                    'description': 'Complete API documentation for developers',
                    'order': 2
                },
                {
                    'title': 'Blog Post',
                    'url': 'https://neosharx.com/blog/ai-task-manager',
                    'link_type': 'blog',
                    'description': 'Detailed blog post about the project',
                    'order': 3
                }
            ]
        },
        {
            'project_slug': 'blockchain-voting-system',
            'links': [
                {
                    'title': 'White Paper',
                    'url': 'https://blockchain-voting.com/whitepaper.pdf',
                    'link_type': 'documentation',
                    'description': 'Technical white paper explaining the system',
                    'order': 1
                },
                {
                    'title': 'Smart Contracts',
                    'url': 'https://github.com/alexj/blockchain-voting/tree/main/contracts',
                    'link_type': 'other',
                    'description': 'View the Solidity smart contracts on GitHub',
                    'order': 2
                }
            ]
        },
        {
            'project_slug': 'machine-learning-analytics-platform',
            'links': [
                {
                    'title': 'Research Paper',
                    'url': 'https://datatech.com/research/ml-platform.pdf',
                    'link_type': 'documentation',
                    'description': 'Academic research paper on the platform',
                    'order': 1
                },
                {
                    'title': 'Case Studies',
                    'url': 'https://datatech.com/case-studies',
                    'link_type': 'website',
                    'description': 'Real-world case studies and implementations',
                    'order': 2
                }
            ]
        }
    ]

    for project_data in links_data:
        try:
            project = NeoProject.objects.get(slug=project_data['project_slug'])
            for link_data in project_data['links']:
                link, created = ProjectLink.objects.get_or_create(
                    project=project,
                    title=link_data['title'],
                    defaults=link_data
                )
                if created:
                    print(f"Created link '{link.title}' for project '{project.title}'")
                else:
                    print(f"Link '{link.title}' already exists for project '{project.title}'")
        except NeoProject.DoesNotExist:
            print(f"Project with slug '{project_data['project_slug']}' not found")

def assign_owners_to_projects():
    """Assign owners to existing projects"""
    owner_assignments = {
        'ai-powered-task-manager': 'sarah-chen',
        'blockchain-voting-system': 'alex-johnson',
        'machine-learning-analytics-platform': 'datatech-solutions'
    }

    for project_slug, owner_slug in owner_assignments.items():
        try:
            project = NeoProject.objects.get(slug=project_slug)
            owner = ProjectOwner.objects.get(slug=owner_slug)
            project.owner = owner
            project.save()
            print(f"Assigned owner '{owner.name}' to project '{project.title}'")
        except (NeoProject.DoesNotExist, ProjectOwner.DoesNotExist) as e:
            print(f"Error assigning owner: {e}")

if __name__ == '__main__':
    print("Creating sample project owners and links...")

    # Create owners
    owners = create_sample_owners()

    # Create links
    create_sample_links()

    # Assign owners to projects
    assign_owners_to_projects()

    print("\nSample data creation completed!")
    print(f"Created {len(owners)} project owners")
    print(f"Created project links for existing projects")
    print("Assigned owners to projects")