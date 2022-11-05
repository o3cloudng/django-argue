
import jwt
from data_settings.models import *
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import filters, generics, status
from rest_framework.generics import (  # RetrieveUpdateAPIView, DestroyAPIView  #CreateAPIView, ListAPIView,
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts import serializers
from accounts.pagination import CustomPageNumberPagination

from accounts.models import User
from accounts.serializers import AddUserRoleSerializer, CustomTokenObtainPairSerializer  # UserRoleSerializer,
from accounts.serializers import (ChangePasswordSerializer, PasswordResetSerializer,
                          ReactivateSerializer, RegisterSerializer,
                          UserUpdateSerializer, LogoutSerializer,
                          RolePermissionSerializer, SetNewPasswordSerializer,)
from accounts.utils import Util
from aircraft_template_manager.models import AircraftTemplateManager
from occurrence_report.models import OccurrenceMetaData, ReportSection, ReportSubSection

from rest_framework.decorators import api_view, permission_classes
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.settings import SIMPLE_JWT

# Password Reset Utils
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext as _
# from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        default_error_message = {
            "error": "Incorrect password."
            # 'no_active_account': _('email or password is incorrect!')
        }
        
        # token["email"] = user.email
        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data = request.data)
    #     serializer.is_valid(raise_exception=True)

    #     return Response(serializer.data)

# User Creation and List of all Active Users
class RegisterListAPIView(ListCreateAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = RegisterSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("accounts.add_user"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email= user_data["email"])

        print(type(request.data["is_auto_generate_password"]))
        print(request.data["is_auto_generate_password"])

        if request.data["email"]:
            # if not user.is_verified:
            user.is_verified = True
            user.is_active = True
            user.save()

            email_body = (
            "Hello "
            + user.first_name + " "+user.last_name + 
            """
            Your account has been created on ARGUE with access to the dashboard, below

            is your login information to access your profile and generate report.

            """
            "Email: " + user.email + "\n\n"

            + "Password: "+ request.data["password"] +"\n\n\n\n"

            """
            Please change password when you’re logged in
            You have been assigned the following role(s)
            """
            + request.data["role"]+"\n\n"
        )
        else:
            token = RefreshToken.for_user(user).access_token
            user.is_verified = False
            user.is_active = False
            user.save()

            base_url = settings.ARGUEHOST + "verify-email/?token="+str(token)
            email_body = (
                "Hello "
                + user.first_name + " "+user.last_name + ",\n\n"
                """
                Your account has been created on ARGUE with access to the dashboard, below

                is your login information to access your profile and generate report.

                + "Email: " + user.email + "\n\n"
                """
                + base_url + "\n"
                """
                
                Please change password when you’re logged in
                You have been assigned the following role(s)
                """
                + request.data["role"]+"\n\n"
            )
            
        data = {
            "email_body": email_body,
            "to_email": user_data["email"],
            "email_subject": "New ARGUE Profile",
        }


        if not request.data["role"]:
            return Response({"error":"Role must be selected."}, status=status.HTTP_401_UNAUTHORIZED)

        role = Group.objects.get(name=request.data["role"])
        if not role:
            return Response({"error":"Role not found."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        role.user_set.add(serializer.data["id"])
        
        Util.send_email(data)
        return Response({"data":serializer.data, "role":role.name}, status=status.HTTP_201_CREATED)


#  Verify Email
class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        # password = request.GET.get("password")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print("##### Token Verify::")
            # print(payload)
            user = User.objects.get(id=payload["user_id"])

            # print(user)

            if not user.is_active:
                user.is_verified = True
                user.is_active = True
                # user.password = user.set_password(password)
                user.save()

            return Response({"message": "Successfully activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# Read, Update & Delete Users
class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("accounts.view_user"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm("accounts.change_user"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=kwargs['id'])
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("accounts.delete_user"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


# RAECTIVATD USER
class ReactivateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ReactivateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# User Creation and List of all Users including deactivated users
class AllUsersListAPIView(ListAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "username",
        "password",
        "is_deleted",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "username",
        "password",
    ]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return User.objects.all()


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        email = request.data["email"]
        if not User.objects.filter(email=email).exists():
            return Response({"error":"Error with the email, ensure you are enter the correct email address"})
        else:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relativeLink = reverse("confirm-password-reset", kwargs={"uidb64":uidb64, "token":token}) 
            base_url = "http://"+ current_site + relativeLink

            # base_url = settings.ARGUEHOST + "confirm-password-reset/?token="+str(token)

            email_body = (
                """
                
                Reset your password.
                
                You have received a request to reset the password for your ARGUE account

                """
                + base_url +
                
                """"
                If you didn't make this request just ignore it, and note this reset link will expire in 30 minutes.

                Best regards,
                AIB
                """
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "ARGUE: Password Reset",
            }

        Util.send_email(data)

        return Response({"message":"Your request for password reset has been sent, check you email to complete the process."}, status=status.HTTP_201_CREATED)

        
        

        # user_data = request.data

        # user = User.objects.get(email=user_data["email"])
        # token = RefreshToken.for_user(user).access_token

        # if not user:
        #     return Response({"error":"Email not found."}, status=status.HTTP_400_BAD_REQUEST)

        # base_url = settings.ARGUEHOST + "confirm-password-reset/?token="+str(token)

        # token = RefreshToken.for_user(user).access_token

        # email_body = (
        #     "Hello "
        #     + user.first_name + " "+user.last_name + ",\n\n"
        #     + "Your account password on ARGUE has been reset.\n\n"
        #     + "Below is your link to verify it is you.\n\n\n\n"

        #     # + "Email: " + user.email + "\n\n"
        #     + base_url
            
        #     +"\n\n\n\n"
        #     + "Please set new password after clicking the link.\n\n"
        # )
        # data = {
        #     "email_body": email_body,
        #     "to_email": user.email,
        #     "email_subject": "ARGUE: Password Reset",
        # }

        # Util.send_email(data)
        # return Response(user_data, status=status.HTTP_201_CREATED)


class ConfirmPasswordResetAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            # print(user)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is nolonger valid"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"message":"Credentials valid","success": True, "uidb64":uidb64,"token":token})

            
        except DjangoUnicodeDecodeError as identifier:
            # if not PasswordResetTokenGenerator():
            return Response({"error": "Token is nolonger valid"}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":True, "message":"Password reset successfully."}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        print("##### LOGOUT test")
        try:
            refresh_token = request.data["refresh"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "You are now logged out."},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )

    send_mail(
        # title:
        "Password Reset for {title}".format(title="ARGUE"),
        # message:
        email_plaintext_message,
        # from:
        "olumideo@synercomgroup.net",
        # to:
        [reset_password_token.user.email],
    )

class ProfileDetailsAPIView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        pk = request.user.id
        user = User.objects.get(id=pk)
        serializer = serializers.ProfileSerializer(user, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### Single End-Point for Role Creation and Assigning of Model Permissions
class RolePermissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = (IsAuthenticated,)


    def list(self, request):
        if not request.user.has_perm("auth.view_group"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset()
        serializer = RolePermissionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("auth.add_group"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        # print("### Role from Data")
        # print(request.data["role_name"])
        if request.data["role_name"]:
            if not Group.objects.filter(name=request.data["role_name"]).exists():
                Group.objects.create(name=request.data["role_name"])

            role= Group.objects.get(name=request.data["role_name"])
            print("### Role from Group")
            print(role)
            if not role:
                return Response({"error": "Role creation failed."})

            # print("######   MODULES HERE")
            for module in request.data["modules"]:
                # ReportManager
                # ContentManager  
                #         
                # UserRoleManager
                # UserProfileManager  
                #             
                # AircraftTemplateManager                
                # MediaLibrary                
                # WorkflowManager                
                # DataSettings

                print(module["module_name"])

                # OCCURRENCE REPORT MANAGER
                if module["module_name"] == "ReportManager":
                    ct = ContentType.objects.get_for_model(ReportSection)
                    module["module_name"] = "reportsection"
        
                    if str(module["can_view"]) == "False":
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_add"]) == "False":
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_edit"]) == "False":
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_delete"]) == "False":
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_import"]) == "False":
                        code_name = "import_"+ module["module_name"].str.lower()
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "import_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_print"]) == "False":
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                    print("Done")

                if module["module_name"] == "ContentManager":
                    ct = ContentType.objects.get_for_model(ReportSubSection)
                    module["module_name"] = "reportsubsection"
        
                    if str(module["can_view"]) == "False":
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_add"]) == "False":
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_edit"]) == "False":
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_delete"]) == "False":
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_import"]) == "False":
                        code_name = "import_"+ module["module_name"].str.lower()
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "import_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_print"]) == "False":
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                    print("Done")
                
                # USER MANAGER
                if module["module_name"] == "UserRoleManager":
                    ct = ContentType.objects.get_for_model(User)
                    module["module_name"] = "user"
        
                    if str(module["can_view"]) == "False":
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                        print("True")

                    if str(module["can_add"]) == "False":
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                        print("True")


                    if str(module["can_edit"]) == "False":
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                        print("True")


                    if str(module["can_delete"]) == "False":
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                        print("True")


                    if str(module["can_import"]) == "False":
                        code_name = "import_"+ module["module_name"].str.lower()
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "import_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_export"]) == "False":
                        code_name = "export_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "export_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_deactivate"]) == "False":
                        code_name = "deactivate_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "deactivate_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_print"]) == "False":
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                if module["module_name"] == "UserProfileManager":
                    ct = ContentType.objects.get_for_model(User)
                    module["module_name"] = "user"
        
                    if str(module["can_view"]) == "False":
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_add"]) == "False":
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_edit"]) == "False":
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                        print("True")


                    if str(module["can_delete"]) == "False":
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_import"]) == "False":
                        code_name = "import_"+ module["module_name"].str.lower()
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "import_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_export"]) == "False":
                        code_name = "export_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "export_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)


                    if str(module["can_deactivate"]) == "False":
                        code_name = "deactivate_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "deactivate_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_print"]) == "False":
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                
                # AIRCRAFT TEMPLATE MANAGER
                if module["module_name"] == "AircraftTemplateManager":
                    ct = ContentType.objects.get_for_model(AircraftTemplateManager)
                    module["module_name"] = "aircrafttemplatemanager"
        
                    if str(module["can_view"]) == "False":
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_add"]) == "False":
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_edit"]) == "False":
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_delete"]) == "False":
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)
                        print("True")

                    if str(module["can_import"]) == "False":
                        code_name = "import_"+ module["module_name"].str.lower()
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "import_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_print"]) == "False":
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                #  MEDIA LIBRARY

                # WORKFLOW MANAGER
                
                # DATA SETTINGS
                if module["module_name"] == "DataSettings":
                    ct = ContentType.objects.get_for_model(OccurrenceType)
                    module["module_name"] = "occurrencetype"
        
                    if str(module["can_view"]) == "False":
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "view_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_add"]) == "False":
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "add_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_edit"]) == "False":
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "change_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_delete"]) == "False":
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "delete_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_import"]) == "False":
                        code_name = "import_"+ module["module_name"].str.lower()
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "import_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

                    if str(module["can_print"]) == "False":
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.remove(permission)
                    else:
                        code_name = "print_"+ str.lower(module["module_name"])
                        permission = Permission.objects.get(
                            codename=code_name, content_type=ct
                            )
                        role.permissions.add(permission)

            
            return Response({"data":request.data})
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

class RoleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("auth.view_group"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     if not request.user.has_perm("auth.change_group"):
    #         return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
    #     queryset = Group.objects.filter(id=pk)
    #     queryset.name = request.data["role_name"]
    #     queryset.save()

    #     return super().put(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm("auth.view_group"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm("auth.delete_group"):
            return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


######  OLD ROLE VIEW
# class RoleListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Group.objects.all()
#     serializer_class = RoleSerializer
#     permission_classes = (IsAuthenticated,)

#     def list(self, request):
#         if not request.user.has_perm("auth.view_group"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)

#         queryset = self.get_queryset()
#         serializer = RoleSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         if not request.user.has_perm("auth.add_group"):
#             return Response({"error":"Permission denied."}, status=status.HTTP_401_UNAUTHORIZED)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)





#### Add User To Role
class AddUserRoleAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddUserRoleSerializer
    queryset = Group.objects.all()

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "No action here"}, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        if (str(request.data["user"]) == "") | (str(request.data["role"]) == ""):
            # print(str(request.data["user"]))
            return Response({"error": "Select role and user.", "status_code": 400})

        role = Group.objects.get(pk=request.data["role"])
        user = User.objects.get(pk=request.data["user"])

        urole = []
        print(user)
        for i in user.groups.all():
            urole.append(i.name)

        add_role = role.user_set.add(user)
        user = str(user)
        if add_role == False:
            return Response(
                ({"error": "Role assignment to user failed.", "status_code": "200"})
            )

        return Response(
            {
                "user": user,
                "roles": urole,
                "message": "Role assigned to user successfully",
                "status_code": 201,
            }
        )

    def delete(self, request, *args, **kwargs):
        if (str(request.data["user"]) == "") | (str(request.data["role"]) == ""):
            return Response({"error": "Select role and user.", "status_code": 400})

        role = Group.objects.get(pk=request.data["role"])
        user = User.objects.get(pk=request.data["user"])

        urole = []
        for i in user.groups.all():
            urole.append(i.name)

        if (role != "") & (user != ""):
            role.user_set.remove(user)

            user = str(user)
            return Response(
                {
                    "user": user,
                    "roles": urole,
                    "message": "User removed from role successfully",
                    "status_code": 204,
                }
            )

        else:
            return Response({"error": "User or role not found.", "status_code": 200})

        # import pdb
        # pdb.set_trace()
        # print(user)

        # return Response(role, user)


#### Permissions
class PermissionAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        # print(request.data)
        # role = Group.objects.get(name=role_name)
        # print(role)
        # if not role:
        #     return Response({"error": "Role not selected."})

        # print(role)
        role_name = request.data["role_name"]
        print(role_name)
        role_permissions = Group.objects.get(name=role_name).permissions.all().values()
        # role_perm = serializers.serializer("json", role_permissions)

        return Response(list(role_permissions))

    def post(self, request, *args, **kwargs):
        role = Group.objects.get(name=request.data["role_name"])
        if not role:
            return Response({"error": "Role not selected."})

        # Data Settings Permission
        if not request.data["module"]:
            return Response({"error": "Module not selected."})

        # print("#### MODULE")
        # print(request.data["module"])

        module = eval(request.data["module"])
        ct = ContentType.objects.get_for_model(module)
        
        if str(request.data["can_view"]) == "False":
            code_name = "view_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "view_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)
            

        if str(request.data["can_add"]) == "False":
            code_name = "add_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "add_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)


        if str(request.data["can_edit"]) == "False":
            code_name = "change_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "change_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)


        if str(request.data["can_delete"]) == "False":
            code_name = "delete_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "delete_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)


        if str(request.data["can_import"]) == "False":
            code_name = "import_"+ request.data["module"].str.lower()
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "import_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)


        if str(request.data["can_export"]) == "False":
            code_name = "export_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "export_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)


        if str(request.data["can_deactivate"]) == "False":
            code_name = "deactivate_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "deactivate_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)

        if str(request.data["can_print"]) == "False":
            code_name = "print_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.remove(permission)
        else:
            code_name = "print_"+ str.lower(request.data["module"])
            permission = Permission.objects.get(
                codename=code_name, content_type=ct
                )
            role.permissions.add(permission)
            
        role_name = request.data["role_name"]
        print(role_name)
        role_permissions = Group.objects.get(name=role_name).permissions.all().values()
        
        return Response({
            "message": "Permissions assigned to role successfully.",
            "permissions":request.data 
            })

