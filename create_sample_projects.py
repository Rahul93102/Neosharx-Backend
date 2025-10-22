#!/usr/bin/env python
"""
Script to create sample Neo Projects for testing
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from authentication.models import NeoProject, CustomUser

def create_sample_projects():
    """Create sample Neo Projects"""
    
    # Get or create an admin user
    admin_user, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@neosharx.com',
            'phone_number': '+1234567890',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Sample projects data
    projects_data = [
        {
            'title': 'AI-Powered Task Manager',
            'description': 'A smart task management application that uses AI to prioritize tasks and suggest optimal work schedules.',
            'detailed_description': '''This project combines modern web development with artificial intelligence to create a revolutionary task management experience. The application learns from user behavior patterns and uses machine learning algorithms to provide intelligent suggestions for task prioritization and time management. Built with React frontend and Python backend, it showcases the power of AI in everyday productivity tools.''',
            'category': 'ai_ml',
            'technologies': 'React, Python, TensorFlow, PostgreSQL, Docker',
            'status': 'completed',
            'difficulty_level': 'intermediate',
            'features': ['AI-powered task prioritization', 'Smart scheduling', 'Real-time collaboration', 'Analytics dashboard', 'Mobile responsive design'],
            'installation_instructions': '''1. Clone the repository\n2. Install dependencies with npm install\n3. Set up Python virtual environment\n4. Install Python requirements\n5. Configure database settings\n6. Run migrations\n7. Start the development server''',
            'usage_instructions': '''1. Create an account or login\n2. Add your tasks and projects\n3. Let the AI analyze your patterns\n4. Follow AI suggestions for optimal productivity\n5. Track your progress with built-in analytics''',
            'developer_name': 'NeoSharX Team',
            'developer_email': 'projects@neosharx.com',
            'tags': 'ai, productivity, react, python, machine learning',
            'license': 'MIT',
            'version': '2.1.0',
            'is_featured': True,
            'is_published': True,
            'is_open_source': True,
            'views_count': 1250,
            'stars_count': 89,
            'featured_image': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=450&fit=crop',
            'demo_url': 'https://ai-taskmanager-demo.neosharx.com',
            'github_url': 'https://github.com/neosharx/ai-task-manager',
            'screenshots': [
                'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop'
            ]
        },
        {
            'title': 'Blockchain Voting System',
            'description': 'A secure, transparent voting system built on blockchain technology ensuring tamper-proof elections.',
            'detailed_description': '''This innovative voting system leverages blockchain technology to create a completely transparent and secure voting process. Each vote is recorded as a transaction on the blockchain, making it immutable and verifiable by all participants. The system includes voter authentication, ballot creation, real-time vote counting, and comprehensive audit trails.''',
            'category': 'blockchain',
            'technologies': 'Ethereum, Solidity, Web3.js, React, Node.js',
            'status': 'beta',
            'difficulty_level': 'advanced',
            'features': ['Blockchain-based voting', 'Smart contracts', 'Voter authentication', 'Real-time results', 'Audit trails', 'Mobile-friendly interface'],
            'installation_instructions': '''1. Install Node.js and npm\n2. Install Truffle framework\n3. Set up Ethereum test network\n4. Clone the repository\n5. Install dependencies\n6. Deploy smart contracts\n7. Configure Web3 connection\n8. Launch the application''',
            'usage_instructions': '''1. Connect your Ethereum wallet\n2. Verify your voter eligibility\n3. Browse available elections\n4. Cast your vote securely\n5. Verify your vote on the blockchain\n6. View real-time results''',
            'developer_name': 'Alex Johnson',
            'developer_email': 'alex@blockchainvoting.com',
            'collaborators': 'Sarah Chen, Mike Rodriguez',
            'tags': 'blockchain, voting, ethereum, smart contracts, democracy',
            'license': 'GPL-3.0',
            'version': '1.0.0-beta',
            'is_featured': True,
            'is_published': True,
            'is_open_source': True,
            'views_count': 890,
            'stars_count': 124,
            'featured_image': 'https://images.unsplash.com/photo-1639322537228-f710d846310a?w=800&h=450&fit=crop',
            'demo_url': 'https://blockchain-voting-demo.com',
            'github_url': 'https://github.com/alexj/blockchain-voting',
            'screenshots': [
                'https://images.unsplash.com/photo-1639322537228-f710d846310a?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=600&h=400&fit=crop'
            ]
        },
        {
            'title': 'IoT Smart Home Dashboard',
            'description': 'A comprehensive dashboard for managing IoT devices in smart homes with real-time monitoring and control.',
            'detailed_description': '''This project creates a centralized control hub for smart home devices, allowing users to monitor and control all their IoT devices from a single, intuitive dashboard. It supports various protocols like MQTT, WiFi, and Zigbee, and provides real-time data visualization, automated routines, and energy consumption tracking.''',
            'category': 'iot',
            'technologies': 'Vue.js, Node.js, MQTT, InfluxDB, Grafana, Arduino',
            'status': 'in_development',
            'difficulty_level': 'intermediate',
            'features': ['Multi-protocol device support', 'Real-time monitoring', 'Automated routines', 'Energy tracking', 'Mobile app', 'Voice control integration'],
            'installation_instructions': '''1. Set up Node.js environment\n2. Install MQTT broker\n3. Configure InfluxDB\n4. Clone repository\n5. Install dependencies\n6. Configure device connections\n7. Set up Grafana dashboards\n8. Launch the application''',
            'usage_instructions': '''1. Add your IoT devices\n2. Configure device settings\n3. Create automation routines\n4. Monitor real-time data\n5. Control devices remotely\n6. View energy consumption reports''',
            'developer_name': 'Tech Innovators',
            'developer_email': 'contact@techinnovators.io',
            'collaborators': 'Emma Wilson, David Park',
            'tags': 'iot, smart home, dashboard, automation, monitoring',
            'license': 'Apache-2.0',
            'version': '0.8.5',
            'is_featured': False,
            'is_published': True,
            'is_open_source': True,
            'views_count': 567,
            'stars_count': 45,
            'featured_image': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=450&fit=crop',
            'demo_url': 'https://smarthome-dashboard-demo.io',
            'github_url': 'https://github.com/techinnovators/smart-home-dashboard',
            'screenshots': [
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?w=600&h=400&fit=crop'
            ]
        },
        {
            'title': 'AR Shopping Experience',
            'description': 'An augmented reality application that allows users to visualize products in their real environment before purchasing.',
            'detailed_description': '''This cutting-edge AR application revolutionizes online shopping by allowing customers to place 3D models of products in their real environment using their smartphone camera. Built with ARKit/ARCore, it provides realistic product visualization, scale accuracy, and interactive features to enhance the shopping experience.''',
            'category': 'ar_vr',
            'technologies': 'Unity, ARKit, ARCore, C#, Firebase, 3D Modeling',
            'status': 'completed',
            'difficulty_level': 'expert',
            'features': ['AR product visualization', '3D model interaction', 'Real-world scaling', 'Product catalog integration', 'Social sharing', 'Purchase integration'],
            'installation_instructions': '''1. Install Unity 2021.3 or later\n2. Set up ARKit/ARCore SDK\n3. Clone the repository\n4. Import Unity project\n5. Configure AR settings\n6. Build for iOS/Android\n7. Deploy to device''',
            'usage_instructions': '''1. Launch the app\n2. Grant camera permissions\n3. Scan your environment\n4. Browse product catalog\n5. Place products in AR\n6. Interact and customize\n7. Share or purchase''',
            'developer_name': 'AR Solutions Inc',
            'developer_email': 'info@arsolutions.com',
            'tags': 'ar, shopping, unity, 3d, mobile, ecommerce',
            'license': 'Commercial',
            'version': '3.2.1',
            'is_featured': True,
            'is_published': True,
            'is_open_source': False,
            'views_count': 2100,
            'stars_count': 156,
            'featured_image': 'https://images.unsplash.com/photo-1592478411213-6153e4ebc696?w=800&h=450&fit=crop',
            'demo_url': 'https://ar-shopping-demo.com',
            'screenshots': [
                'https://images.unsplash.com/photo-1592478411213-6153e4ebc696?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=400&fit=crop'
            ]
        },
        {
            'title': 'Machine Learning Analytics Platform',
            'description': 'A comprehensive platform for data analysis and machine learning model deployment with an intuitive interface.',
            'detailed_description': '''This platform provides a complete solution for data scientists and analysts to perform advanced analytics and machine learning operations. It features automated data preprocessing, model training, hyperparameter tuning, and deployment capabilities. The platform supports various ML algorithms and provides visualization tools for model performance analysis.''',
            'category': 'data_science',
            'technologies': 'Python, Scikit-learn, TensorFlow, Django, React, PostgreSQL',
            'status': 'maintained',
            'difficulty_level': 'advanced',
            'features': ['Automated ML pipelines', 'Data visualization', 'Model deployment', 'Performance monitoring', 'Collaboration tools', 'API integration'],
            'installation_instructions': '''1. Set up Python 3.8+ environment\n2. Install required packages\n3. Configure PostgreSQL database\n4. Clone the repository\n5. Run database migrations\n6. Set up Redis for task queue\n7. Start Django backend\n8. Launch React frontend''',
            'usage_instructions': '''1. Upload your dataset\n2. Configure preprocessing steps\n3. Select ML algorithms\n4. Train and validate models\n5. Deploy best performing model\n6. Monitor model performance\n7. Collaborate with team members''',
            'developer_name': 'DataTech Solutions',
            'developer_email': 'team@datatech.com',
            'collaborators': 'Dr. Lisa Wang, James Miller, Ana Santos',
            'tags': 'machine learning, data science, analytics, python, ai',
            'license': 'BSD-3-Clause',
            'version': '4.1.2',
            'is_featured': False,
            'is_published': True,
            'is_open_source': True,
            'views_count': 1800,
            'stars_count': 203,
            'featured_image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=450&fit=crop',
            'demo_url': 'https://ml-analytics-demo.datatech.com',
            'github_url': 'https://github.com/datatech/ml-analytics-platform',
            'screenshots': [
                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop'
            ]
        }
    ]
    
    # Create the projects
    created_count = 0
    for project_data in projects_data:
        project, created = NeoProject.objects.get_or_create(
            title=project_data['title'],
            defaults={**project_data, 'author': admin_user}
        )
        if created:
            created_count += 1
            print(f"✅ Created project: {project.title}")
        else:
            print(f"⚠️  Project already exists: {project.title}")
    
    print(f"\n🎉 Successfully created {created_count} new projects!")
    print(f"📊 Total projects in database: {NeoProject.objects.count()}")

if __name__ == '__main__':
    create_sample_projects()