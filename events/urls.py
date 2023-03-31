from django.urls import path,include

from events.views import AddCampaignManager, CampaignAdd, CampaignList, CampaignVolunteerAdd, DonationAdd, EventImageDelete, EventOrganizerDelete, EventOrganizersAdd, EventOrganizersOnEvent, EventRUD, EventsAdd, EventsImageAdd, EventsList, EventsScheduleAdd, EventsScheduleList, EventsScheduleRUD, EventsVolunteeringCategoryAdd, EventsVolunteeringCategoryRUD, EventsVolunteersAdd, EventsVolunteersCertificationAdd, EventsVolunteersHoursAdd


urlpatterns = [
    path("event-add", EventsAdd.as_view(), name="event-add"),
    path("events-get", EventsList.as_view(), name="events-get"),
    path('event-detail/<str:id>',EventRUD.as_view(),name="event-detail"),
    path('events-edit/<str:id>',EventRUD.as_view(),name="events-edit"),
    path('events-delete/<str:id>',EventRUD.as_view(),name="events-delete"),
    path('event-orgs-add',EventOrganizersAdd.as_view(),name="event-orgs-add"),
    path('event-orgs-get',EventOrganizersOnEvent.as_view(),name="event-orgs-get"),
    path('events-org-remove/<str:id>',EventOrganizerDelete.as_view(),name="events-org-remove-from-event"),
    path('events-image-add',EventsImageAdd.as_view(),name="events-image-add"),
    path('events-image-delete/<str:id>',EventImageDelete.as_view(),name="events-image-delete"),
    path("event-category-add", EventsVolunteeringCategoryAdd.as_view(), name="event-category-add"),
    path('events-category-edit/<str:id>',EventsVolunteeringCategoryRUD.as_view(),name="events-category-edit"),
    path('events-category-delete/<str:id>',EventsVolunteeringCategoryRUD.as_view(),name="events-category-delete"),
    
    path("event-schedule-add", EventsScheduleAdd.as_view(), name="event-schedule-add"),
    path("event-schedule-get", EventsScheduleList.as_view(), name="event-schedule-get"),
    path('event-schedule-edit/<str:id>',EventsScheduleRUD.as_view(),name="event-schedule-edit"),
    path('event-schedule-delete/<str:id>',EventsScheduleRUD.as_view(),name="event-schedule-delete"),
    
    path('register-for-event',EventsVolunteersAdd.as_view(),name="register-for-event"),
    path('add-hours-for-volunteer',EventsVolunteersHoursAdd.as_view(),name="add-hours-for-volunteer"),
    path('certificate-volunteer',EventsVolunteersCertificationAdd.as_view(),name="certificate-volunteer"),
    
    path('get-campaigns',CampaignList.as_view(),name='get-campaigns'),
    path('add-campaign',CampaignAdd.as_view(),name='add-campaign'),
    path('add-campaign-manager/<str:id>',AddCampaignManager.as_view(),name='add-campaign'),
    
    path('register-for-campaign',CampaignVolunteerAdd.as_view(),name='register-for-campaign'),
    path('add-donations',DonationAdd.as_view(),name='add-donations'),
    
]