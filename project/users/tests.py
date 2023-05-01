from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


BASE_URL = "http://127.0.0.1:8000"


class UserLoginAndSingupTestCases(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="Test User",
                                             hashed_phone_number="+918125825876",
                                             is_profile_complete=True)

    def call_generate_otp(self, phone_number):
        payload = {
            "phone_number": phone_number
        }
        response = self.client.post(BASE_URL+"/api/users/generate_otp/", payload, format='json')
        return response

    def verify_otp(self, phone_number):
        self.call_generate_otp(phone_number)
        payload = {
            "phone_number": phone_number,
            "otp_received": "00000"
        }
        response = self.client.post(BASE_URL + "/api/users/verify_otp/", payload, format='json')

        return response

    def test_generate_otp(self):
        """
        Ensure we can generate OTP for given Phone Number.
        """
        phone_number = "+918125825877"
        response = self.call_generate_otp(phone_number)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'], 'OTP Sent Successfully')
        self.assertEqual(response_data['phone_number'], phone_number)

    def test_verify_otp_new_user_flow(self):
        """
        Ensure we can create a new account object.
        """
        phone_number = "+918125825877"

        response = self.verify_otp(phone_number)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response_data['display_message'], 'OTP Verified Successfully')
        self.assertEqual(response_data['phone_number'], phone_number)
        self.assertEqual(response_data['user']['username'], phone_number)
        self.assertEqual(response_data['user']['phone_number'], phone_number)
        self.assertIs(response_data['user']['is_profile_complete'], False)
        self.assertIn('token', response_data['user'].keys())
        self.assertIn('created_at', response_data['user'].keys())
        self.assertIn('modified_at', response_data['user'].keys())

    def test_update_new_user_name_flow(self):
        """
        Ensure we can create a new account object.
        """
        phone_number = "+918125825878"
        response = self.verify_otp(phone_number)
        response_data = response.data

        user_id = response_data['user']['id']
        user_token = response_data['user']['token']
        new_username = "Test User 123"
        payload = {
            "username": new_username,
        }

        headers = {
            "Authorization": f"Token {user_token}"
        }

        response = self.client.patch(BASE_URL + f"/api/users/{user_id}/", payload,
                                     headers=headers, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['username'], new_username)
        self.assertEqual(response_data['phone_number'], phone_number)
        self.assertIs(response_data['is_profile_complete'], True)
        self.assertIn('token', response_data.keys())
        self.assertIn('created_at', response_data.keys())
        self.assertIn('modified_at', response_data.keys())

    def test_verify_otp_login_user_flow(self):
        """
        Ensure we can create a new account object.
        """
        phone_number = self.user.phone_number

        response = self.verify_otp(phone_number)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['display_message'], 'Welcome Test User')
        self.assertEqual(response_data['phone_number'], phone_number)
        self.assertEqual(response_data['user']['username'], self.user.username)
        self.assertEqual(response_data['user']['phone_number'], phone_number)
        self.assertIs(response_data['user']['is_profile_complete'], True)
        self.assertIn('token', response_data['user'].keys())
        self.assertIn('created_at', response_data['user'].keys())
        self.assertIn('modified_at', response_data['user'].keys())