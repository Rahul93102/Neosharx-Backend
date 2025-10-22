from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.verify_service_sid = settings.TWILIO_VERIFY_SERVICE_SID
    
    def send_verification_code(self, phone_number):
        """
        Send OTP verification code using Twilio Verify API
        """
        # Mock mode for testing
        if getattr(settings, 'USE_MOCK_OTP', False):
            logger.info(f"MOCK: Verification code sent to {phone_number}")
            return {
                'success': True,
                'message': 'Verification code sent successfully (MOCK MODE)',
                'verification_sid': 'mock_verification_sid'
            }
            
        try:
            # Ensure phone number has country code
            if not phone_number.startswith('+'):
                phone_number = '+1' + phone_number  # Default to US country code
            
            verification = self.client.verify.v2.services(
                self.verify_service_sid
            ).verifications.create(to=phone_number, channel='sms')
            
            logger.info(f"Verification sent to {phone_number}, SID: {verification.sid}")
            return {
                'success': True,
                'message': 'Verification code sent successfully',
                'verification_sid': verification.sid
            }
        except TwilioException as e:
            logger.error(f"Twilio error: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send verification code: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'success': False,
                'message': 'An unexpected error occurred'
            }
    
    def verify_code(self, phone_number, code):
        """
        Verify the OTP code using Twilio Verify API
        """
        # Mock mode for testing
        if getattr(settings, 'USE_MOCK_OTP', False):
            mock_code = getattr(settings, 'MOCK_OTP_CODE', '123456')
            if code == mock_code:
                logger.info(f"MOCK: Verification successful for {phone_number}")
                return {
                    'success': True,
                    'message': 'Phone number verified successfully (MOCK MODE)'
                }
            else:
                logger.info(f"MOCK: Verification failed for {phone_number} - invalid code")
                return {
                    'success': False,
                    'message': 'Invalid verification code'
                }
        
        try:
            # Ensure phone number has country code
            if not phone_number.startswith('+'):
                phone_number = '+1' + phone_number  # Default to US country code
                
            verification_check = self.client.verify.v2.services(
                self.verify_service_sid
            ).verification_checks.create(to=phone_number, code=code)
            
            logger.info(f"Verification check for {phone_number}: {verification_check.status}")
            
            if verification_check.status == 'approved':
                return {
                    'success': True,
                    'message': 'Phone number verified successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid verification code'
                }
        except TwilioException as e:
            logger.error(f"Twilio verification error: {str(e)}")
            return {
                'success': False,
                'message': f'Verification failed: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected verification error: {str(e)}")
            return {
                'success': False,
                'message': 'An unexpected error occurred during verification'
            }