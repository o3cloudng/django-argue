from accounts.models import User

# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class OccurrenceTypeTest(APITestCase):

    occurrence_type_url = reverse("occurrence-type")
    login_url = reverse("token_obtain_pair")
    all_users_url = reverse("all-users")

    def setUp(self):
        self.email = "admin@example.com"
        self.password = "@Password"
        self.data = {"email": self.email, "password": self.password}

        self.user = User.objects.create_user(
            email=self.email, password=self.password, username="example"
        )
        self.assertEqual(self.user.is_active, 1, "Active User")
        response = self.client.post(self.login_url, self.data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def tearDown(self):
        pass

    def test_authenticated_can_view_content_type(self):
        response = self.client.get(self.occurrence_type_url)
        print("Authenticated user can view page url")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.all_users_url)
        print("Failed authentication")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_add_data(self):
        self.data = {
            "name": "New Content Type",
            "description": "This a new content type",
        }
        response = self.client.post(self.occurrence_type_url, self.data)
        print("Authenticated user can add content type")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

    def test_wrong_values_in_content_type(self):
        self.data = {
            "name": "",
            "description": "",
        }
        response = self.client.post(self.occurrence_type_url, self.data)
        print("Bad request cannot be added to content type")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_view_content_type(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.occurrence_type_url)
        print("Unauthorized user cannot view content type")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_add_content_type(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.occurrence_type_url)
        # print(response.data)
        print("Unauthorized user cannot add content type")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_put_content_type(self):
        self.data = {
            "name": "johnson",
            "description": "johnson is great",
        }
        resp = self.client.post(self.occurrence_type_url, self.data)

        self.ndata = {
            "name": "johnson",
            "description": "johnson is great",
        }
        # request.POST.get("")
        if resp:
            response = self.client.put(
                reverse("occurrence-type-details"), kwargs={"pk": 1}, data=self.ndata
            )

            print("Authorized user can update content type")
            print(response.status_code)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
