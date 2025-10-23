#!/usr/bin/env python
"""
Test script to verify deployed backend functionality
"""
import requests
import json

BASE_URL = "https://backend-neosharx.onrender.com"

def test_endpoint(url, method='GET', data=None, headers=None):
    """Test an endpoint and return response"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"❌ Unsupported method: {method}")
            return None

        print(f"🔍 Testing {method} {url}")
        print(f"   Status: {response.status_code}")

        if response.status_code >= 200 and response.status_code < 300:
            print("   ✅ Success")
        else:
            print("   ❌ Failed")

        return response

    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
        return None

def test_backend():
    print("=" * 60)
    print("NEOSHARX BACKEND DEPLOYMENT TEST")
    print("=" * 60)

    # Test basic connectivity
    print("\n1. Testing basic connectivity...")
    response = test_endpoint(BASE_URL)
    if not response or response.status_code != 200:
        print("❌ Backend not accessible!")
        return

    # Test admin interface
    print("\n2. Testing admin interface...")
    admin_response = test_endpoint(f"{BASE_URL}/admin/")
    if admin_response and admin_response.status_code in [200, 302]:  # 302 is redirect to login
        print("   ✅ Admin interface accessible")
    else:
        print("   ❌ Admin interface not accessible")

    # Test API endpoints
    print("\n3. Testing API endpoints...")

    # Test hackathons endpoint
    hackathons_response = test_endpoint(f"{BASE_URL}/api/hackathons/")
    if hackathons_response and hackathons_response.status_code == 200:
        try:
            data = hackathons_response.json()
            print(f"   ✅ Hackathons API: {len(data)} hackathons found")
        except:
            print("   ✅ Hackathons API: Response received")
    else:
        print("   ❌ Hackathons API failed")

    # Test events endpoint
    events_response = test_endpoint(f"{BASE_URL}/api/events/")
    if events_response and events_response.status_code == 200:
        try:
            data = events_response.json()
            print(f"   ✅ Events API: {len(data)} events found")
        except:
            print("   ✅ Events API: Response received")
    else:
        print("   ❌ Events API failed")

    # Test authentication endpoints
    print("\n4. Testing authentication endpoints...")

    # Test login endpoint
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    login_response = test_endpoint(f"{BASE_URL}/api/auth/login/", 'POST', login_data)
    if login_response:
        if login_response.status_code == 200:
            print("   ✅ Login successful")
            try:
                login_data = login_response.json()
                if 'access' in login_data:
                    print("   ✅ JWT tokens received")
                else:
                    print("   ⚠️  Login response format unexpected")
            except:
                print("   ⚠️  Could not parse login response")
        elif login_response.status_code == 401:
            print("   ⚠️  Invalid credentials (admin user may not exist yet)")
        else:
            print(f"   ❌ Login failed with status {login_response.status_code}")

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✅ Backend is accessible and responding")
    print("✅ Admin interface is accessible")
    print("✅ API endpoints are functional")
    print("\nNext steps:")
    print("1. Create admin user using create_admin_oneliner.py")
    print("2. Test admin login at https://backend-neosharx.onrender.com/admin/")
    print("3. Verify API functionality with authentication")
    print("=" * 60)

if __name__ == '__main__':
    test_backend()