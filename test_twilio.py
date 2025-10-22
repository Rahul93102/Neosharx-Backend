"""
Simple test script to verify Twilio integration
Run this to test if your Twilio credentials are working
"""

import os
import sys

# Add the Django project to Python path
sys.path.append('/Users/vishaljha/neosharx/Backend flow')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from authentication.services import TwilioService

def test_twilio_connection():
    """Test Twilio connection and send a test OTP"""
    
    print("Testing Twilio Connection...")
    print("=" * 40)
    
    # Initialize Twilio service
    twilio_service = TwilioService()
    
    # Test phone number (replace with your own for testing)
    test_phone = input("Enter your phone number (with country code, e.g., +1234567890): ")
    
    if not test_phone:
        print("❌ No phone number provided")
        return
    
    # Send OTP
    print(f"📱 Sending OTP to {test_phone}...")
    result = twilio_service.send_verification_code(test_phone)
    
    if result['success']:
        print("✅ OTP sent successfully!")
        print(f"📝 Message: {result['message']}")
        
        # Ask for OTP verification
        otp_code = input("Enter the OTP you received: ")
        
        if otp_code:
            print(f"🔐 Verifying OTP: {otp_code}")
            verify_result = twilio_service.verify_code(test_phone, otp_code)
            
            if verify_result['success']:
                print("✅ OTP verified successfully!")
                print(f"📝 Message: {verify_result['message']}")
            else:
                print("❌ OTP verification failed!")
                print(f"📝 Error: {verify_result['message']}")
        else:
            print("⚠️  No OTP code provided for verification")
            
    else:
        print("❌ Failed to send OTP!")
        print(f"📝 Error: {result['message']}")

if __name__ == "__main__":
    try:
        test_twilio_connection()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 40)
    print("Test completed!")