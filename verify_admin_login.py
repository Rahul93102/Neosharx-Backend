#!/usr/bin/env python
"""
Script to verify admin login functionality
"""
import requests
import json

BASE_URL = "https://backend-neosharx.onrender.com"

def test_admin_login():
    print("=" * 60)
    print("NEOSHARX ADMIN LOGIN VERIFICATION")
    print("=" * 60)

    # Test admin interface accessibility
    print("\n1. Testing admin interface accessibility...")
    admin_response = requests.get(f"{BASE_URL}/admin/")
    print(f"   Status: {admin_response.status_code}")

    if admin_response.status_code in [200, 302]:
        print("   ✅ Admin interface accessible")
    else:
        print("   ❌ Admin interface not accessible")
        return

    # Test admin login
    print("\n2. Testing admin login...")

    # First, get the login page to extract CSRF token if needed
    login_page = requests.get(f"{BASE_URL}/admin/login/")
    csrf_token = None

    if "csrfmiddlewaretoken" in login_page.text:
        # Extract CSRF token from the form
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print("   ✅ CSRF token extracted")

    # Prepare login data
    login_data = {
        "username": "admin",
        "password": "admin123",
        "next": "/admin/"
    }

    headers = {
        "Referer": f"{BASE_URL}/admin/login/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    if csrf_token:
        login_data["csrfmiddlewaretoken"] = csrf_token
        headers["X-CSRFToken"] = csrf_token

    # Attempt login
    login_response = requests.post(
        f"{BASE_URL}/admin/login/",
        data=login_data,
        headers=headers,
        allow_redirects=True
    )

    print(f"   Login response status: {login_response.status_code}")

    if login_response.status_code == 200:
        if "/admin/" in login_response.url and "login" not in login_response.url:
            print("   ✅ Admin login successful!")
            print(f"   Redirected to: {login_response.url}")
        else:
            print("   ⚠️  Login response received, but may not be fully authenticated")
            print(f"   Final URL: {login_response.url}")
    else:
        print("   ❌ Admin login failed")
        print(f"   Response: {login_response.text[:200]}...")

    # Test API login as well
    print("\n3. Testing API authentication...")

    api_login_data = {
        "username": "admin",
        "password": "admin123"
    }

    api_response = requests.post(f"{BASE_URL}/api/auth/login/", json=api_login_data)
    print(f"   API login status: {api_response.status_code}")

    if api_response.status_code == 200:
        try:
            tokens = api_response.json()
            if "access" in tokens and "refresh" in tokens:
                print("   ✅ API login successful - JWT tokens received")
                print("   ✅ Admin user exists and can authenticate")
            else:
                print("   ⚠️  API login response format unexpected")
        except:
            print("   ❌ Could not parse API login response")
    elif api_response.status_code == 401:
        print("   ❌ Invalid credentials - admin user may not exist")
        print("   💡 Run create_admin_oneliner.py on the server first")
    else:
        print(f"   ❌ API login failed with status {api_response.status_code}")

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_admin_login()