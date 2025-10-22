#!/usr/bin/env python
"""Script to check database integrity and reset if needed"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
django.setup()

def check_database_integrity():
    """Check database tables and data integrity"""
    print("🔍 Checking database integrity...")

    with connection.cursor() as cursor:
        # Check what tables exist
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"📋 Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        # Check for any data in key tables
        key_tables = [
            'authentication_customuser',
            'authentication_startupstory',
            'authentication_neostory',
            'authentication_neoproject',
            'authentication_sharxathon',
            'authentication_technews',
            'authentication_talkepisode',
            'authentication_roboticsnews',
            'authentication_event',
            'authentication_youtubevideo'
        ]

        print("\n📊 Data counts in key tables:")
        for table in key_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  - {table}: {count} records")
            except Exception as e:
                print(f"  - {table}: ERROR - {e}")

        # Check for any orphaned foreign keys or constraints
        print("\n🔗 Checking for constraint issues...")
        try:
            cursor.execute("""
                SELECT conname, conrelid::regclass, confrelid::regclass
                FROM pg_constraint
                WHERE contype = 'f'
                ORDER BY conname;
            """)
            constraints = cursor.fetchall()
            print(f"Found {len(constraints)} foreign key constraints")
        except Exception as e:
            print(f"Error checking constraints: {e}")

def reset_database():
    """Reset database by dropping all tables and re-running migrations"""
    print("⚠️  RESETTING DATABASE - This will delete all data!")
    confirm = input("Are you sure you want to reset the database? (type 'YES' to confirm): ")
    if confirm != 'YES':
        print("Database reset cancelled.")
        return

    print("🗑️  Dropping all tables...")
    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        tables = cursor.fetchall()

        # Disable foreign key checks
        cursor.execute("SET CONSTRAINTS ALL DEFERRED;")

        # Drop all tables
        for table in tables:
            table_name = table[0]
            if not table_name.startswith('pg_') and not table_name.startswith('_pg_'):
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
                    print(f"  Dropped: {table_name}")
                except Exception as e:
                    print(f"  Error dropping {table_name}: {e}")

    print("🚀 Re-running migrations...")
    from django.core.management import call_command
    call_command('migrate', verbosity=2, interactive=False)
    print("✅ Database reset complete!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_database()
    else:
        check_database_integrity()