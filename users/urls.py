from django.urls import path,include

from users.views import LoginAPIView, OrganizationAdd, OrganizationAdminAdd, OrganizationApproval, OrganizationEventOrganizerAdd, OrganizationList, SignupUserView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path("auth/signup/", SignupUserView.as_view(), name="signup"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-org',OrganizationList.as_view(),name="organiaztions-get"),
    path('create-org',OrganizationAdd.as_view(),name="organiaztions-add"),
    path('approve-org/<str:id>',OrganizationApproval.as_view(),name="OrganizationApproval"),
    path('create-admins',OrganizationAdminAdd.as_view(),name="create-admin"),
    path('create-event-org',OrganizationEventOrganizerAdd.as_view(),name="create-event-org")
]
