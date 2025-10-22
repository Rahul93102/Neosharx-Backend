#!/usr/bin/env python3.11
"""
Test script for NeoSharx Authentication System
Tests all API endpoints with the provided phone number: 9310270910
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/auth"
TEST_PHONE = "+919310270910"  # Your phone number with India country code
TEST_USER = {
    "username": "testuser_" + str(int(time.time())),
    "email": "test@neosharx.com",
    "phone_number": TEST_PHONE,
    "password": "testpass123",
    "confirm_password": "testpass123"
}

def test_endpoint(method, endpoint, data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*50}")
    print(f"Testing: {method} {url}")
    print(f"Data: {json.dumps(data, indent=2) if data else 'None'}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    print("🚀 Testing NeoSharx Authentication System")
    print("="*50)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Phone: {TEST_PHONE}")
    
    # Step 1: Test Registration
    print("\n\n1️⃣  TESTING USER REGISTRATION")
    register_response = test_endpoint("POST", "/register/", TEST_USER)
    
    if not register_response or register_response.status_code != 201:
        print("❌ Registration failed!")
        return
    
    # Extract token from registration response
    register_data = register_response.json()
    auth_token = register_data.get("token")
    user_id = register_data.get("user_id")
    
    print(f"✅ Registration successful!")
    print(f"Token: {auth_token}")
    print(f"User ID: {user_id}")
    
    headers = {"Authorization": f"Token {auth_token}"}
    
    # Step 2: Test Login
    print("\n\n2️⃣  TESTING USER LOGIN")
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    login_response = test_endpoint("POST", "/login/", login_data)
    
    if login_response and login_response.status_code == 200:
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")
    
    # Step 3: Test Send OTP
    print("\n\n3️⃣  TESTING SEND OTP")
    otp_data = {"phone_number": TEST_PHONE}
    otp_response = test_endpoint("POST", "/send-otp/", otp_data, headers)
    
    if otp_response and otp_response.status_code == 200:
        print("✅ OTP sent successfully!")
        print(f"📱 Please check your phone ({TEST_PHONE}) for the OTP")
        
        # Wait for user to receive OTP
        otp_code = input("\n🔐 Enter the OTP you received: ").strip()
        
        if otp_code:
            # Step 4: Test Verify OTP
            print("\n\n4️⃣  TESTING VERIFY OTP")
            verify_data = {
                "phone_number": TEST_PHONE,
                "otp": otp_code
            }
            verify_response = test_endpoint("POST", "/verify-otp/", verify_data, headers)
            
            if verify_response and verify_response.status_code == 200:
                print("✅ OTP verification successful!")
            else:
                print("❌ OTP verification failed!")
        else:
            print("⚠️  No OTP provided, skipping verification test")
    else:
        print("❌ Failed to send OTP!")
    
    # Step 5: Test Get Profile
    print("\n\n5️⃣  TESTING GET PROFILE")
    profile_response = test_endpoint("GET", "/profile/", headers=headers)
    
    if profile_response and profile_response.status_code == 200:
        print("✅ Profile retrieval successful!")
    else:
        print("❌ Profile retrieval failed!")
    
    # Step 6: Test Update Profile
    print("\n\n6️⃣  TESTING UPDATE PROFILE")
    update_data = {
        "email": "updated_test@neosharx.com"
    }
    update_response = test_endpoint("PUT", "/profile/update/", update_data, headers)
    
    if update_response and update_response.status_code == 200:
        print("✅ Profile update successful!")
    else:
        print("❌ Profile update failed!")
    
    # Step 7: Test Logout
    print("\n\n7️⃣  TESTING LOGOUT")
    logout_response = test_endpoint("POST", "/logout/", headers=headers)
    
    if logout_response and logout_response.status_code == 200:
        print("✅ Logout successful!")
    else:
        print("❌ Logout failed!")
    
    print("\n\n" + "="*50)
    print("🎉 Testing completed!")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")