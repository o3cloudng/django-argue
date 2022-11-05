from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response


def assign_group_permissions(request, act, action_type, code_name, ct, module, role):  # data = request.user, module = OccurrenceType, role
    # if not module:
    #     return Response({"error": "Module not selected."})
    print("######  DATA in Method.py")
    ct = ContentType.objects.get_for_model(module)
            
    if str(request.data[act]) == "False":
        permission = Permission.objects.get(
            codename=code_name, content_type=ct
            )
        print(request.data[act])
        role.permissions.remove(permission)
    else:
        permission = Permission.objects.get(
            codename=code_name, content_type=ct
            )
        print(request.data[act])
        role.permissions.add(permission)
