from django.contrib import admin

from accounts.models import User
from django.contrib.auth.models import Permission, ContentType

# Register your models here.
admin.site.register(User)
# admin.site.register(Group)
admin.site.register(Permission)
admin.site.register(ContentType)
