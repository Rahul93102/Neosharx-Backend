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
from authentication.models import TechNews

def create_sample_tech_news():
    """Create sample tech news articles for testing"""
    
    # Article 1: AI Breaking News
    article1 = TechNews.objects.create(
        title="OpenAI Launches GPT-5 with Revolutionary Reasoning Capabilities",
        subtitle="The latest AI model shows unprecedented advances in complex problem-solving",
        excerpt="OpenAI has unveiled GPT-5, marking a significant leap in artificial intelligence with advanced reasoning, multimodal understanding, and real-world problem-solving capabilities that surpass all previous models.",
        content="""
        <h2>A New Era in Artificial Intelligence</h2>
        <p>Today marks a historic milestone in the field of artificial intelligence as OpenAI officially launches GPT-5, the most advanced language model ever created. This breakthrough system demonstrates capabilities that were once thought to be years away.</p>
        
        <h3>Key Features</h3>
        <p>GPT-5 introduces several groundbreaking features:</p>
        <ul>
            <li><strong>Enhanced Reasoning:</strong> The model can now solve complex mathematical proofs and multi-step logical problems with near-perfect accuracy.</li>
            <li><strong>True Multimodal Understanding:</strong> Seamless integration of text, images, audio, and video processing in a single unified model.</li>
            <li><strong>Improved Safety:</strong> Advanced alignment techniques ensure the model follows ethical guidelines and refuses harmful requests.</li>
            <li><strong>Extended Context:</strong> Support for up to 1 million tokens, allowing for analysis of entire codebases or books.</li>
        </ul>
        
        <h3>Real-World Applications</h3>
        <p>Early testers report remarkable results across various domains:</p>
        <ul>
            <li>Medical diagnosis assistance with expert-level accuracy</li>
            <li>Legal document analysis and contract review</li>
            <li>Scientific research acceleration through literature review and hypothesis generation</li>
            <li>Software development with near-autonomous coding capabilities</li>
        </ul>
        
        <h3>Industry Impact</h3>
        <p>"This is not just an incremental improvement—it's a paradigm shift," said Dr. Sarah Chen, AI researcher at MIT. "GPT-5's reasoning capabilities approach human-level performance on many complex tasks."</p>
        
        <p>The model is now available through OpenAI's API, with both research and commercial tiers. Pricing starts at $0.03 per 1K tokens for the standard version.</p>
        """,
        category='ai_ml',
        tags=['OpenAI', 'GPT-5', 'AI', 'Machine Learning', 'NLP', 'Reasoning'],
        featured_image='https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200',
        thumbnail_image='https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600',
        author_name='Alex Thompson',
        author_bio='Senior Technology Reporter specializing in AI and emerging technologies',
        author_avatar='https://i.pravatar.cc/150?img=12',
        priority='breaking',
        read_time_minutes=8,
        views_count=15420,
        likes_count=892,
        shares_count=456,
        key_points=[
            "GPT-5 shows unprecedented reasoning capabilities",
            "Supports 1 million token context window",
            "True multimodal understanding across text, image, audio, and video",
            "Enhanced safety features and ethical alignment",
            "Available now through OpenAI API"
        ],
        related_links=[
            {"title": "OpenAI Official Announcement", "url": "https://openai.com/blog/gpt-5"},
            {"title": "Technical Paper", "url": "https://arxiv.org/example"},
            {"title": "API Documentation", "url": "https://platform.openai.com/docs"}
        ],
        is_published=True,
        is_featured=True,
        is_breaking=True,
        is_trending=True,
        published_at=timezone.now() - timedelta(hours=2),
        meta_description="OpenAI launches GPT-5 with revolutionary AI reasoning capabilities, multimodal understanding, and extended context support.",
        meta_keywords="GPT-5, OpenAI, AI, machine learning, artificial intelligence, reasoning"
    )
    
    # Article 2: Blockchain News
    article2 = TechNews.objects.create(
        title="Ethereum 3.0 Roadmap Promises 100x Faster Transactions",
        subtitle="Vitalik Buterin reveals ambitious upgrade plan for world's second-largest blockchain",
        excerpt="Ethereum founder Vitalik Buterin has unveiled the roadmap for Ethereum 3.0, featuring revolutionary sharding technology and zero-knowledge proofs that could process over 100,000 transactions per second.",
        content="""
        <h2>The Future of Ethereum</h2>
        <p>At the Ethereum Developer Conference in Singapore, Vitalik Buterin presented a comprehensive roadmap for Ethereum 3.0, outlining the most significant upgrade in the blockchain's history.</p>
        
        <h3>Technical Innovations</h3>
        <p>The upgrade focuses on three key areas:</p>
        <ul>
            <li><strong>Advanced Sharding:</strong> 64 shard chains processing transactions in parallel</li>
            <li><strong>ZK-SNARKs Integration:</strong> Privacy-preserving transactions built into the protocol</li>
            <li><strong>Quantum Resistance:</strong> Post-quantum cryptography to future-proof the network</li>
        </ul>
        
        <h3>Performance Improvements</h3>
        <p>Current Ethereum can handle approximately 15-30 transactions per second. With Ethereum 3.0, this number is expected to exceed 100,000 TPS while maintaining decentralization.</p>
        
        <h3>Timeline and Migration</h3>
        <p>The rollout is planned in phases over the next 18-24 months. Existing smart contracts will be automatically compatible with the new system.</p>
        """,
        category='blockchain',
        tags=['Ethereum', 'Blockchain', 'Web3', 'Vitalik Buterin', 'Crypto', 'DeFi'],
        featured_image='https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=1200',
        thumbnail_image='https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=600',
        author_name='Maria Garcia',
        author_bio='Blockchain analyst and cryptocurrency expert with 8 years of experience',
        author_avatar='https://i.pravatar.cc/150?img=45',
        priority='high',
        read_time_minutes=6,
        views_count=8950,
        likes_count=567,
        shares_count=234,
        key_points=[
            "100x transaction speed improvement expected",
            "64 shard chains for parallel processing",
            "Built-in privacy with ZK-SNARKs",
            "Quantum-resistant cryptography",
            "Rollout over next 18-24 months"
        ],
        is_published=True,
        is_featured=True,
        is_trending=True,
        published_at=timezone.now() - timedelta(hours=5),
        meta_description="Ethereum 3.0 roadmap promises 100x faster transactions with advanced sharding and zero-knowledge proofs.",
        meta_keywords="Ethereum 3.0, blockchain, cryptocurrency, Web3, sharding, ZK-SNARKs"
    )
    
    # Article 3: Startup Funding
    article3 = TechNews.objects.create(
        title="AI Startup Anthropic Raises $4 Billion in Record-Breaking Series C",
        subtitle="Google and other tech giants back Claude AI creator in massive funding round",
        excerpt="Anthropic, the AI safety company behind Claude, has secured $4 billion in Series C funding, making it one of the largest venture capital rounds in tech history.",
        content="""
        <h2>Historic Funding Round</h2>
        <p>Anthropic has closed a $4 billion Series C round led by Google, with participation from Salesforce Ventures, Zoom Ventures, and other major investors. This brings the company's valuation to $18 billion.</p>
        
        <h3>Claude AI's Success</h3>
        <p>The funding comes on the heels of Claude's rapid adoption by enterprises worldwide. The AI assistant has been praised for its safety features, accuracy, and ethical approach to AI.</p>
        
        <h3>Plans for the Future</h3>
        <p>Anthropic plans to use the funds to:</p>
        <ul>
            <li>Expand its research team by 500+ positions</li>
            <li>Build larger compute infrastructure</li>
            <li>Develop next-generation AI safety techniques</li>
            <li>Launch enterprise-focused features</li>
        </ul>
        """,
        category='funding',
        tags=['Anthropic', 'Claude', 'AI', 'Funding', 'Venture Capital', 'Google'],
        featured_image='https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=1200',
        thumbnail_image='https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=600',
        author_name='David Chen',
        author_bio='Venture capital reporter covering Silicon Valley startups',
        author_avatar='https://i.pravatar.cc/150?img=33',
        priority='high',
        read_time_minutes=5,
        views_count=12300,
        likes_count=743,
        shares_count=389,
        key_points=[
            "$4 billion Series C led by Google",
            "$18 billion valuation reached",
            "Plans to hire 500+ researchers",
            "Focus on AI safety and ethics",
            "Largest AI startup funding this year"
        ],
        is_published=True,
        is_featured=True,
        is_trending=True,
        published_at=timezone.now() - timedelta(hours=8),
        meta_description="Anthropic raises record $4 billion in Series C funding led by Google for Claude AI development.",
        meta_keywords="Anthropic, Claude AI, funding, venture capital, Google, AI startup"
    )
    
    # Article 4: Cybersecurity
    article4 = TechNews.objects.create(
        title="Major Zero-Day Vulnerability Discovered in Windows 11",
        subtitle="Microsoft rushes emergency patch as exploit code circulates online",
        excerpt="A critical zero-day vulnerability affecting Windows 11 has been discovered, allowing attackers to gain system-level access. Microsoft is deploying an emergency patch to all users.",
        content="""
        <h2>Critical Security Alert</h2>
        <p>Security researchers have identified a critical vulnerability in Windows 11 that could allow attackers to execute arbitrary code with system privileges.</p>
        
        <h3>Vulnerability Details</h3>
        <p>The flaw, tracked as CVE-2025-0001, exists in the Windows Print Spooler service. Attackers can exploit it through specially crafted print jobs sent over the network.</p>
        
        <h3>Immediate Actions Required</h3>
        <ul>
            <li>Install the emergency security update immediately</li>
            <li>Disable Print Spooler if not required</li>
            <li>Monitor for suspicious network activity</li>
            <li>Update endpoint protection definitions</li>
        </ul>
        """,
        category='cybersecurity',
        tags=['Windows 11', 'Security', 'Zero-Day', 'Microsoft', 'Vulnerability', 'CVE'],
        featured_image='https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200',
        thumbnail_image='https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600',
        source_name='Microsoft Security Response Center',
        source_url='https://msrc.microsoft.com/update-guide',
        author_name='Jennifer Wu',
        author_bio='Cybersecurity analyst and penetration testing expert',
        author_avatar='https://i.pravatar.cc/150?img=27',
        priority='breaking',
        read_time_minutes=4,
        views_count=23400,
        likes_count=1234,
        shares_count=892,
        is_published=True,
        is_breaking=True,
        published_at=timezone.now() - timedelta(hours=1),
        meta_description="Critical zero-day vulnerability found in Windows 11 Print Spooler. Emergency patch released by Microsoft.",
        meta_keywords="Windows 11, zero-day, vulnerability, security, Microsoft, CVE-2025-0001"
    )
    
    # Article 5: Product Launch
    article5 = TechNews.objects.create(
        title="Apple Unveils Vision Pro 2 with Revolutionary Eye-Tracking Interface",
        subtitle="Second-generation AR headset doubles resolution and adds AI-powered features",
        excerpt="Apple's Vision Pro 2 brings significant improvements with 8K displays, advanced eye-tracking, and seamless AI integration, setting a new standard for spatial computing.",
        content="""
        <h2>Next Generation Spatial Computing</h2>
        <p>Apple CEO Tim Cook took the stage today to introduce Vision Pro 2, the company's most advanced mixed reality headset yet.</p>
        
        <h3>Key Improvements</h3>
        <ul>
            <li>8K micro-OLED displays (4K per eye)</li>
            <li>40% lighter than original Vision Pro</li>
            <li>6-hour battery life (doubled)</li>
            <li>Advanced hand and eye tracking</li>
            <li>Built-in AI assistant for spatial tasks</li>
        </ul>
        
        <h3>New visionOS 3.0</h3>
        <p>The updated operating system brings hundreds of new spatial apps, including productivity tools, games, and creative applications.</p>
        
        <h3>Pricing and Availability</h3>
        <p>Vision Pro 2 starts at $2,999 and will be available in stores next month.</p>
        """,
        category='product_launch',
        tags=['Apple', 'Vision Pro', 'AR', 'VR', 'Spatial Computing', 'Mixed Reality'],
        featured_image='https://images.unsplash.com/photo-1617802690992-15d93263d3a9?w=1200',
        thumbnail_image='https://images.unsplash.com/photo-1617802690992-15d93263d3a9?w=600',
        video_url='https://youtube.com/watch?v=example',
        author_name='Michael Roberts',
        author_bio='Senior tech reviewer specializing in consumer electronics',
        author_avatar='https://i.pravatar.cc/150?img=68',
        priority='high',
        read_time_minutes=7,
        views_count=19800,
        likes_count=1456,
        shares_count=723,
        key_points=[
            "8K displays with exceptional clarity",
            "40% lighter and more comfortable",
            "6-hour battery life",
            "AI-powered spatial interface",
            "Starts at $2,999"
        ],
        is_published=True,
        is_featured=True,
        published_at=timezone.now() - timedelta(hours=12),
        meta_description="Apple Vision Pro 2 features 8K displays, advanced eye-tracking, and AI integration for next-gen spatial computing.",
        meta_keywords="Apple Vision Pro 2, AR headset, mixed reality, spatial computing, visionOS"
    )
    
    print(f"✅ Created article 1: {article1.title} (slug: {article1.slug})")
    print(f"✅ Created article 2: {article2.title} (slug: {article2.slug})")
    print(f"✅ Created article 3: {article3.title} (slug: {article3.slug})")
    print(f"✅ Created article 4: {article4.title} (slug: {article4.slug})")
    print(f"✅ Created article 5: {article5.title} (slug: {article5.slug})")
    print("\n🎉 Sample tech news articles created successfully!")
    print(f"\nTotal articles created: {TechNews.objects.count()}")

if __name__ == "__main__":
    # Clear existing articles (optional)
    print("Clearing existing tech news articles...")
    TechNews.objects.all().delete()
    print("Creating new sample articles...\n")
    
    create_sample_tech_news()
