from django.contrib import admin
from events.models import EventsVolunteers

from users.models import OrganizationUser, User,Organization

# Register your models here.

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(OrganizationUser)
admin.site.register(EventsVolunteers)

