#!/usr/bin/env python
"""Custom management command to run migrations with better error handling"""
import os
import sys

print("🚀 Starting migrate_with_debug.py script...")

try:
    import django
    from django.core.management import execute_from_command_line
    from django.db import connection
    from django.conf import settings

    print("📦 Django imports successful")

    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
    print(f"⚙️  DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

    django.setup()
    print("✅ Django setup completed")

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

            # Check current migration status
            print("� Checking migration status...")
            from django.core.management import call_command
            from io import StringIO
            output = StringIO()
            call_command('showmigrations', stdout=output, verbosity=1)
            migrations_output = output.getvalue()
            print("Current migrations status:")
            print(migrations_output)

            # Check if there are any pending migrations
            output = StringIO()
            call_command('migrate', stdout=output, verbosity=1, dry_run=True, interactive=False)
            dry_run_output = output.getvalue()
            if "No migrations to apply" in dry_run_output:
                print("✅ No pending migrations")
            else:
                print("⚠️  Pending migrations found:")
                print(dry_run_output)

            # Run migrations
            print("🚀 Running migrations...")
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

except Exception as e:
    print(f"💥 Script failed before Django setup: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)