from django.contrib import admin
from .models import Event,Donation,EventsVolunteersCertification, EventOrganizers, EventsImage, EventsVolunteersHours,SuperCategory
# Register your models here.


admin.site.register(Event)
admin.site.register(EventOrganizers)
admin.site.register(EventsImage)
admin.site.register(EventsVolunteersHours)
admin.site.register(SuperCategory)
admin.site.register(Donation)
admin.site.register(EventsVolunteersCertification)