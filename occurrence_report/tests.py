import email
from rest_framework.test import APITestCase
from accounts.models import User
from django.urls import reverse, resolve
from accounts.views import RegisterListAPIView

# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from django.test import SimpleTestCase


class ApiUrlTest(SimpleTestCase):
    def test_get_user_is_resolved(self):
        url = reverse("occurrence-report")
        # print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, RegisterListAPIView)


class UserAPIViewTest(APITestCase):

    user_url = reverse("occurrence-report")
    login_url = reverse("token_obtain_pair")
    occurrence_report_url = reverse("occurrence-report")

    def setUp(self):
        self.email = "o3cloudng@gmail.com"
        self.password = "@Password"
        self.data = {"email": self.email, "password": self.password}

        self.user = User.objects.create_user(
            email="o3cloudng@gmail.com", password="@Password", username="o3cloud"
        )
        self.assertEqual(self.user.is_active, 1, "Active User")
        resp = self.client.post(self.login_url, self.data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {resp.data["access"]}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.content)
        # self.refresh = RefreshToken.for_user(self.user)
        # print(self.resp)
        # self.assertEqual(self.resp.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        pass

    def test_get_user_authenticated(self):
        response = self.client.get(self.all_users_url)
        # print(response.data[0]["type"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.all_users_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
