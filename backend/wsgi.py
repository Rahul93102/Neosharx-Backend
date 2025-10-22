import os

from django.core.wsgi import get_wsgi_application

# Use production settings if DJANGO_ENV is set to 'production'
if os.environ.get('DJANGO_ENV') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
