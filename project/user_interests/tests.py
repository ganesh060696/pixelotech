from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Images


BASE_URL = "http://127.0.0.1:8000"


class UserImageRatingTestCases(APITestCase):

    def setUp(self) -> None:
        user = User.fetch_user_with_phone_number(phone_no="+918125825876")
        if user is None:
            user = User.objects.create_user(username="Test User",
                                            hashed_phone_number="+918125825876",
                                            is_profile_complete=True)
        self.user = user
        self.user_token = self.user.auth_token.key
        self.headers = {
            "Authorization": f"Token {self.user_token}"
        }

        self.images_len = Images.objects.count()

    def test_list_images(self):
        """
        Ensure we can generate OTP for given Phone Number.
        """
        response = self.client.get(BASE_URL + "/api/images/", headers=self.headers, format='json')
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['total_count'], self.images_len)
        for image in response_data['data']:
            self.assertIn('id', image.keys())
            self.assertIn('name', image.keys())
            self.assertIn('image_url', image.keys())
            self.assertIn('created_at', image.keys())
            self.assertIn('modified_at', image.keys())

    def create_user_rating(self, image_id, selection_type):
        payload = {
            "image_id": image_id,
            "selection_type": selection_type
        }

        response = self.client.post(BASE_URL + f"/api/user_ratings/", payload,
                                    headers=self.headers, format='json')
        return response

    def test_user_reject_image_flow(self):
        """
        Ensure we can create a new account object.
        """
        image_obj = Images.objects.all().order_by('id').first()
        payload = {
            "image_id": image_obj.id,
            "selection_type": "rejected"
        }

        response = self.create_user_rating(**payload)
        response_json = response.json()
        response_data = response_json['data']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json['display_message'], f"{self.user.username}, you have rejected image {image_obj.name}.")
        self.assertEqual(response_data['image']['id'], image_obj.id)
        self.assertEqual(response_data['user']['id'], self.user.id)
        self.assertEqual(response_data['selection_type'], 'rejected')

    def test_user_reject_image_flow(self):
        """
        Ensure we can create a new account object.
        """
        image_obj = Images.objects.all().order_by('id').first()
        payload = {
            "image_id": image_obj.id,
            "selection_type": "interested"
        }

        response = self.create_user_rating(**payload)
        response_json = response.json()
        response_data = response_json['data']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json['display_message'], f"{self.user.username}, you have selected image {image_obj.name}.")
        self.assertEqual(response_data['image']['id'], image_obj.id)
        self.assertEqual(response_data['image']['id'], image_obj.id)
        self.assertEqual(response_data['user']['id'], self.user.id)
        self.assertEqual(response_data['selection_type'], 'interested')

    def test_update_image_rating_flow(self):
        """
        Ensure we can create a new account object.
        """
        image_obj = Images.objects.all().order_by('id').first()

        payload = {
            "image_id": image_obj.id,
            "selection_type": "rejected"
        }

        rejected_response = self.create_user_rating(**payload)

        rejected_response_json = rejected_response.json()
        rejected_response_data = rejected_response_json['data']
        self.assertEqual(rejected_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(rejected_response_json['display_message'], f"{self.user.username}, you have rejected image {image_obj.name}.")
        self.assertEqual(rejected_response_data['image']['id'], image_obj.id)
        self.assertEqual(rejected_response_data['user']['id'], self.user.id)
        self.assertEqual(rejected_response_data['selection_type'], 'rejected')

        payload = {
            "image_id": image_obj.id,
            "selection_type": "interested"
        }

        interested_response = self.create_user_rating(**payload)

        interested_response_json = interested_response.json()
        interested_response_data = interested_response_json['data']
        self.assertEqual(interested_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(interested_response_json['display_message'], f"{self.user.username}, you have selected image {image_obj.name}.")

        self.assertEqual(interested_response_data['image']['id'], image_obj.id)
        self.assertEqual(interested_response_data['user']['id'], self.user.id)
        self.assertEqual(interested_response_data['selection_type'], 'interested')

        self.assertEqual(interested_response_data['image']['id'],
                         rejected_response_data['image']['id'])
        self.assertEqual(interested_response_data['id'],
                         rejected_response_data['id'])

    def test_rate_last_image_flow(self):
        """
        Ensure we can create a new account object.
        """
        image_objs = Images.objects.all().order_by('id')

        for count, image in enumerate(image_objs):

            count += 1
            payload = {
                "image_id": image.id,
                "selection_type": "interested"
            }

            interested_response = self.create_user_rating(**payload)

            interested_response_json = interested_response.json()
            interested_response_data = interested_response_json['data']
            self.assertEqual(interested_response.status_code, status.HTTP_201_CREATED)

            if count < self.images_len:
                self.assertEqual(interested_response_json['display_message'], f"{self.user.username}, you have selected image {image.name}.")
            else:
                self.assertEqual(interested_response_json['display_message'], f"{self.user.username}, you have rated all the images. Thank You!")

            self.assertEqual(interested_response_data['image']['id'], image.id)
            self.assertEqual(interested_response_data['user']['id'], self.user.id)
            self.assertEqual(interested_response_data['selection_type'], 'interested')


