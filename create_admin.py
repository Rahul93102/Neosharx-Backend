#!/usr/bin/env python
"""
Script to create admin credentials for NeoSharX backend
Run this on the deployed server or locally to create admin user
"""
import os
import django
import sys

# Setup Django
if len(sys.argv) > 1 and sys.argv[1] == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
    print("Using PRODUCTION settings")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    print("Using DEVELOPMENT settings")

django.setup()

from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

User = get_user_model()

def create_admin_user():
    print("=" * 60)
    print("NEOSHARX ADMIN USER CREATION")
    print("=" * 60)

    # Check if admin already exists
    existing_admins = User.objects.filter(is_superuser=True)
    if existing_admins.exists():
        print("⚠️  Existing admin users found:")
        for admin in existing_admins:
            print(f"   - {admin.username} ({admin.email})")
        print("\nDo you want to create another admin user? (y/n): ", end="")
        response = input().lower().strip()
        if response != 'y':
            print("Admin creation cancelled.")
            return

    print("\nCreating new admin user...")
    print("-" * 40)

    # Get admin credentials
    username = input("Enter admin username [admin]: ").strip() or "admin"
    email = input("Enter admin email [admin@neosharx.com]: ").strip() or "admin@neosharx.com"
    password = input("Enter admin password [admin123]: ").strip() or "admin123"

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        return

    if User.objects.filter(email=email).exists():
        print(f"❌ Email '{email}' already exists!")
        return

    # Create superuser
    try:
        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        print("✅ Admin user created successfully!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Superuser: {admin_user.is_superuser}")
        print(f"   Staff: {admin_user.is_staff}")

        print("\n" + "=" * 60)
        print("ADMIN LOGIN CREDENTIALS")
        print("=" * 60)
        print(f"URL: https://backend-neosharx.onrender.com/admin/")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

def list_admin_users():
    print("=" * 60)
    print("EXISTING ADMIN USERS")
    print("=" * 60)

    admins = User.objects.filter(is_superuser=True)
    if not admins.exists():
        print("❌ No admin users found!")
        return

    for i, admin in enumerate(admins, 1):
        print(f"{i}. Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Active: {admin.is_active}")
        print(f"   Last login: {admin.last_login}")
        print()

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'list':
            list_admin_users()
            return
        elif sys.argv[1] == 'prod':
            pass  # Already handled above

    print("NeoSharX Admin User Management")
    print("1. Create new admin user")
    print("2. List existing admin users")
    print("3. Exit")

    choice = input("Choose an option (1-3): ").strip()

    if choice == '1':
        create_admin_user()
    elif choice == '2':
        list_admin_users()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == '__main__':
    main()