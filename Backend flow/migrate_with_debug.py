#!/usr/bin/env python
"""Custom management command to run migrations with better error handling"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
django.setup()

def run_migrations():
    """Run migrations with detailed output"""
    print("🔄 Starting database migrations...")
    print(f"Database URL: {settings.DATABASES['default']['NAME'][:50]}...")
    print(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")

    try:
        # Test database connection
        print("🔗 Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")

        # Run migrations
        print("🚀 Running migrations...")
        from django.core.management import call_command
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migrations completed successfully")

    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    run_migrations()