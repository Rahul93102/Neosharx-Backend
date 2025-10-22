#!/usr/bin/env python3
"""
Test script for forgot password functionality
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_forgot_password():
    print("🧪 Testing Forgot Password Feature")
    print("=" * 50)
    
    # Test 1: Send OTP for password reset
    print("\n1️⃣ Testing forgot-password endpoint...")
    
    data = {
        "phone_number": "+919310270910"
    }
    
    response = requests.post(f"{BASE_URL}/forgot-password/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Forgot password OTP sent successfully!")
        print("📱 Please check your phone for the OTP")
        
        # Wait for user to receive OTP
        otp = input("\n🔢 Enter the OTP you received: ").strip()
        
        if otp:
            # Test 2: Reset password with OTP
            print(f"\n2️⃣ Testing reset-password endpoint with OTP: {otp}")
            
            reset_data = {
                "phone_number": "+919310270910",
                "otp": otp,
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
            
            reset_response = requests.post(f"{BASE_URL}/reset-password/", json=reset_data)
            print(f"Status Code: {reset_response.status_code}")
            print(f"Response: {json.dumps(reset_response.json(), indent=2)}")
            
            if reset_response.status_code == 200:
                print("✅ Password reset successfully!")
                
                # Test 3: Try logging in with new password
                print("\n3️⃣ Testing login with new password...")
                
                login_data = {
                    "username": "otp_test_user",
                    "password": "newpassword123"
                }
                
                login_response = requests.post(f"{BASE_URL}/login/", json=login_data)
                print(f"Status Code: {login_response.status_code}")
                print(f"Response: {json.dumps(login_response.json(), indent=2)}")
                
                if login_response.status_code == 200:
                    print("✅ Login with new password successful!")
                    print("🎉 Forgot password feature is working perfectly!")
                else:
                    print("❌ Login with new password failed")
            else:
                print("❌ Password reset failed")
        else:
            print("⚠️ No OTP provided, skipping reset test")
    else:
        print("❌ Forgot password failed")
    
    # Test 4: Test with non-existent phone number
    print("\n4️⃣ Testing with non-existent phone number...")
    
    invalid_data = {
        "phone_number": "+919999999999"
    }
    
    invalid_response = requests.post(f"{BASE_URL}/forgot-password/", json=invalid_data)
    print(f"Status Code: {invalid_response.status_code}")
    print(f"Response: {json.dumps(invalid_response.json(), indent=2)}")
    
    if invalid_response.status_code == 404:
        print("✅ Non-existent phone number properly rejected")
    else:
        print("⚠️ Unexpected response for non-existent phone number")

if __name__ == "__main__":
    test_forgot_password()