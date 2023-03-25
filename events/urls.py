from django.urls import path,include

from events.views import EventOrganizerDelete, EventOrganizersAdd, EventOrganizersOnEvent, EventRUD, EventsAdd, EventsList


urlpatterns = [
    path("event-add", EventsAdd.as_view(), name="event-add"),
    path("events-get", EventsList.as_view(), name="events-get"),
    path('events-edit/<str:id>',EventRUD.as_view(),name="events-edit"),
    path('events-delete/<str:id>',EventRUD.as_view(),name="events-delete"),
    path('event-orgs-add',EventOrganizersAdd.as_view(),name="event-orgs-add"),
    path('event-orgs-get',EventOrganizersOnEvent.as_view(),name="event-orgs-get"),
    path('events-org-remove/<str:id>',EventOrganizerDelete.as_view(),name="events-org-remove-from-event"),
    
    
    
    
    
    
]