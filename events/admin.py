from django.contrib import admin
from .models import Event, EventOrganizers, EventsImage, EventsVolunteersHours
# Register your models here.


admin.site.register(Event)
admin.site.register(EventOrganizers)
admin.site.register(EventsImage)
admin.site.register(EventsVolunteersHours)