from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (  # DeactivatedUserDetailAPIView,; UserRoleCreateAPIView,; UserRoleDetailAPIView, LogoutAPIView
    AddUserRoleAPIView, AllUsersListAPIView, ChangePasswordAPIView,
    ConfirmPasswordResetAPIView, MyTokenObtainPairView,
    PasswordResetAPIView, PermissionAPIView, ProfileDetailsAPIView,
    ReactivateAPIView, RegisterListAPIView, 
    UserDetailAPIView, VerifyEmail, LogoutAPIView, RolePermissionListCreateAPIView, 
    RoleDetailAPIView, SetNewPasswordAPIView,
    # role_permission 
    )


urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("allusers/", AllUsersListAPIView.as_view(), name="all-users"),
    # path(
    #     "deactivated-users/"
    #     DeactivatedUserDetailAPIView.as_view(),
    #     name="deactivated-user-list",
    # ),
    path("", RegisterListAPIView.as_view(), name="register"),
    path("<int:id>/", UserDetailAPIView.as_view(), name="users"),
    path(
        "reactivate-user/<int:id>/",
        ReactivateAPIView.as_view(),
        name="reactivate-user",
    ),
    # path('delete/<int:id>', UserSoftDelete, name="delete"),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
    # path(
    #     "password-reset-otp/",
    #     PasswordResetAPIView.as_view(),
    #     name="password-reset-otp",
    # ),
    # path(
    #     "password_reset/",
    #     include("django_rest_passwordreset.urls", namespace="password_reset"),
    # ),
    path(
        "password-reset/",
        PasswordResetAPIView.as_view(),
        name="confirm-password-reset",
    ),
    path(
        "confirm-password-reset/<uidb64>/<token>/",
        ConfirmPasswordResetAPIView.as_view(),
        name="confirm-password-reset",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    # path("role-permission/", role_permission, name="role-permission-create"),
    path("role-permission/", RolePermissionListCreateAPIView.as_view(), name="role-permission-create"),
    path("role-permission/<int:id>/", RoleDetailAPIView.as_view(), name="role-permission-detail"),
    # path("role/", RoleListCreateAPIView.as_view(), name="role-list-create"),
    path(
        "add_roles_permissions/",
        PermissionAPIView.as_view(),
        name="add_roles_permission",
    ),
    path("add_user_role/", AddUserRoleAPIView.as_view(), name="add-user-role"),
    # path('role/', RoleListCreateAPIView.as_view(), name='role'),
    # path('role/<int:id>/', RoleDetailAPIView.as_view(), name='role-detail'),
    # path('user_role/', UserRoleCreateAPIView.as_view(), name='user-role'),
    # path('user_role/<int:id>/', UserRoleDetailAPIView.as_view(), name='user-role-detail'),
    path("profile/", ProfileDetailsAPIView.as_view(), name="profile"),
    path("profile/<int:id>", ProfileDetailsAPIView.as_view(), name="profile-edit"),
]
