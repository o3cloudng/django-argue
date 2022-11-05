from rest_framework import permissions
from accounts.models import User, Permission  # Role, UserRole,


class IsVerified(permissions.BasePermission):

    message = "Your email has not been verified. Kindly check your email for confirmation link."

    def has_permission(self, request, view):
        # print("######## IS VERIFIED #######")
        # print(request.user.is_verified)
        # user = User.objects.filter(email=request.user)
        return request.user.is_verified


class IsNotDeactivated(permissions.BasePermission):

    message = "User has been deactivated"

    def has_permission(self, request, view):

        return request.user.is_deleted == False


# class CanViewAllUser(permissions.BasePermission):

#     message = "You are not authourized to perform this action."
#     def has_permission(self, request, view):
#         role = Role.objects.filter(user=request.user)
#         if role != "":
#             print("### Role ID")
#             for r in role:
#                 print(r.id)
#                 perm = Permission.objects.filter(role=r.id, model="UserModule")
#             # can_view = perm.can_view
#                 print("######## ROLE can_view #######")
#                 for i in perm:
#                     print(i.can_view == True)
#                     if i.can_view == True:
#                         print(i.can_view == True)
#                         return True
#         else:
#             return False


# class CanViewOwnUser(permissions.BasePermission):

#     message = "You are not authourized to perform this action."
#     def has_permission(self, request, view):
#         role = Role.objects.filter(user=request.user)
#         if role != "":
#             print("### Role ID")
#             for r in role:
#                 print(r.id)
#                 perm = Permission.objects.filter(role=r.id, model="UserModule")
#             # can_view = perm.can_view
#                 print("######## ROLE can_view #######")
#                 for i in perm:
#                     print(i.can_view == True)
#                     if i.can_view == True:
#                         print(i.can_view == True)
#                         return True
#         else:
#             return False


# class IsAdministrator(permissions.BasePermission):

#     message = "You are not an Administrator"
#     def has_permission(self, request, view):

#         return request.user == "ADMINISTRATOR"

# class IsOccurrenceOwner(permissions.BasePermission):

#     message = "You are not an Occurrence Owner"
#     def has_permission(self, request, view):

#         return request.user == "OCCURRENCEOWNER"

# class IsOccurenceManager(permissions.BasePermission):

#     message = "You are not an Occurrence Manager"
#     def has_permission(self, request, view):

#         return request.user == "OCCURRENCEMANAGER"

# class IsStakeholder(permissions.BasePermission):

#     message = "You are not a Stakeholder"
#     def has_permission(self, request, view):

#         return request.user == "STAKEHOLDER"

# class IsCommittee(permissions.BasePermission):

#     message = "You are not a Committee member"
#     def has_permission(self, request, view):

#         return request.user == "COMMITTEE"
