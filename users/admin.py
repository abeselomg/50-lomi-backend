from django.contrib import admin

from users.models import OrganizationUser, User,Organization

# Register your models here.

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(OrganizationUser)


