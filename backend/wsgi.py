import os

from django.core.wsgi import get_wsgi_application

# Always use production settings for deployment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')

application = get_wsgi_application()
