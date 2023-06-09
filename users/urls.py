from django.urls import path,include

from users.views import (DeleteOrgUserView,AllUsersList,AllUsersUpdateDelete, LoginAPIView, MassEventNotifications, MyMessagesDetail,OrganizationProfileEdit, MyNotificationCount,
                         MessageAdd, MyMessages,UpdateDeleteUserView, OrganizationAdd, OrganizationAdminAdd,
                         OrganizationApproval, OrganizationEventOrganizerAdd, OrganizationList, OrganizationUserList, SignupUserView,MyNotifications, UserNotificationDetail,
                         MassNotificationsUser,MassNotificationsOrganizationAdmins,MassNotificationsOrganizationEventOrgs)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path("auth/signup/", SignupUserView.as_view(), name="signup"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("update-user/<str:id>",UpdateDeleteUserView.as_view(),name='update-user'),
    path("delete-org-user/<str:id>",DeleteOrgUserView.as_view(),name='delete-org-user'),
    
    path('all-users-get',AllUsersList.as_view(),name='all-users-get'),
    path("all-users-update-delete/<str:id>",AllUsersUpdateDelete.as_view(),name='all-users-update-delete'),
    

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-org',OrganizationList.as_view(),name="organiaztions-get"),
    path('create-org',OrganizationAdd.as_view(),name="organiaztions-add"),
    path('approve-org/<str:id>',OrganizationApproval.as_view(),name="OrganizationApproval"),
    path('create-admins',OrganizationAdminAdd.as_view(),name="create-admin"),
    path('create-event-org',OrganizationEventOrganizerAdd.as_view(),name="create-event-org"),
    path('get-org-users',OrganizationUserList.as_view(),name="get-org-users"),
    path('get-org-eventorg-users',OrganizationUserList.as_view(),name="get-org-eventorg-users"),
    path('update-org-profile/<str:id>',OrganizationProfileEdit.as_view(),name="update-org-profile"),
    
    #Messages
    path('send-message',MessageAdd.as_view(),name="send-message"),
    path('my-messages-list',MyMessages.as_view(),name="my-messages-list"),
    path('my-messages-detail',MyMessagesDetail.as_view(),name="my-messages-detail"),
    
    
    #Notification
    path('send-notification',MyNotifications.as_view(),name="send-notification"),
    path('my-notifications',MyNotifications.as_view(),name="my-notifications"),
    path('notification-count',MyNotificationCount.as_view(),name='notification-count'),
    path('send-mass-notification',MassEventNotifications.as_view(),name="send-mass-notification"),
    path('notification-detail/<str:id>',UserNotificationDetail.as_view(),name="notification-detail"),
    path('mass-notification-allusers',MassNotificationsUser.as_view(),name="mass-notification-allusers"),
    path('mass-notification-orgadmins',MassNotificationsOrganizationAdmins.as_view(),name="mass-notification-orgadmins"),
    path('mass-notification-evnt-orgs',MassNotificationsOrganizationEventOrgs.as_view(),name="mass-notification-evnt-orgs"),
    
    
]
