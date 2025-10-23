#!/usr/bin/env python
"""
One-liner script to create admin user on production server
Usage: python create_admin_oneliner.py
"""
import os
import django

# Setup Django for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = "admin"
    email = "admin@neosharx.com"
    password = "admin123"

    # Check if admin already exists
    if User.objects.filter(username=username).exists():
        print("Admin user already exists!")
        return

    # Create superuser
    admin_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    print("✅ Admin user created successfully!")
    print(f"Username: {admin_user.username}")
    print(f"Email: {admin_user.email}")
    print(f"Password: {password}")
    print("\nAdmin URL: https://backend-neosharx.onrender.com/admin/")

if __name__ == '__main__':
    create_admin()