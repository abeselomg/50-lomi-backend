from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q, Count
# Create your views here.
import datetime
from django.http import HttpResponse
from users.utils import CustomValidation

# from elasticsearch_dsl import Q as ES_Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from utils.pagination import CustomPagination

from utils.permissions import IsAdminPermission, IsSuperAdminPermission
from users.models import (UserNotification, Organization, OrganizationUser, User, UserMessage)
from users.serializers import ( MassNotificationSerializer,UserNotificationSerializer, OrganizationSerializer,
                               OrganizationUserSerializer, UserMessageSerializer, UserSerializer,LoginSerializer)




class SignupUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(user)


class UpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update, Delete signup user info"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def put(self, request, id=None):
        user=request.user
        if str(user.id)!=id:
            raise CustomValidation(
                "detail", "Unauthorized Access", status.HTTP_401_UNAUTHORIZED
            )
        return self.partial_update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class LoginAPIView(generics.CreateAPIView):
    """Login users with valid credintials"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data



class AllUsersList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,IsSuperAdminPermission)
    queryset = get_user_model().objects.all()
    serializer_class=UserSerializer
    pagination_class=CustomPagination
    
class AllUsersUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,IsSuperAdminPermission)
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def put(self, request, id=None):
        return self.update(request, id)
    
    def delete(self, request, id=None):
        return self.destroy(request, id)


class OrganizationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,IsSuperAdminPermission)
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class=CustomPagination


class OrganizationAdd(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class OrganizationApproval(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsSuperAdminPermission)
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "id"
    
    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id=None):
        # send custom deletion success message
        return self.destroy(request, id)
    
    
class OrganizationProfileEdit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdminPermission)
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "id"
    
    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        # org=OrganizationUser.objects.get(user=request.user).organization
        # if org.id!=id:
        #         raise CustomValidation(
        #         "detail", "Unauthorized Access", status.HTTP_401_UNAUTHORIZED
        #     )
        return self.partial_update(request, id)
 

class OrganizationAdminAdd(generics.CreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.IsAuthenticated,IsSuperAdminPermission)

    def post(self, request):
        serializer = OrganizationUserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrganizationUserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,IsAdminPermission)
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer   
    pagination_class=CustomPagination
    
      
    def get_queryset(self):
        org=OrganizationUser.objects.get(user=self.request.user).organization
        query_set=OrganizationUser.objects.filter(organization=org)
        role = self.request.query_params.get('role',None)
        print(role)
        if role!=None:
            return query_set.filter(user__role=role)
        else:
            return query_set
            


class OrganizationEventOrganizerAdd(generics.CreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.IsAuthenticated,IsAdminPermission)

    def post(self, request):
        serializer = OrganizationUserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteOrgUserView(generics.DestroyAPIView):
    """Update, Delete signup user info"""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,IsAdminPermission)
    queryset = OrganizationUser.objects.all()
    lookup_field = "id"

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)
    
    
class MessageAdd(generics.CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserMessageSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyMessages(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
      
    def list(self, request):
        user=request.user
        list_of_users=[]
        my_messages_list=[]
        
        try:
            queryset = UserMessage.objects.filter(
                Q(reciver=user) | Q(sender=user)
            ).order_by('is_read','-created_date')

            for q in queryset:
                user_to_list = None
                if (q.reciver.id != user.id):
                    user_to_list=q.reciver
                if (q.sender.id != user.id):
                    user_to_list=q.sender 

                if user_to_list not in list_of_users:
                    list_of_users.append(user_to_list)
                    my_messages_list.append(q)
                
            serializer = UserMessageSerializer(my_messages_list, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )



class MyMessagesDetail(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    
    def get_queryset(self):
        user=self.request.user
        try:
            user_id = self.request.query_params.get('userId',None)
            otheruser=User.objects.get(id=user_id)
            
            queryset = UserMessage.objects.filter(
                    Q(reciver=user) | Q(sender=user)
                ).filter(Q(reciver=otheruser) | Q(sender=otheruser)).order_by('is_read','-created_date')
            return queryset
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )

    
    
    
########################################################  NOTIFICATION VIEWS  #######################################################################

class MyNotifications(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
      
    def list(self, request):
        user=request.user
        my_messages=UserNotification.objects.filter(reciver=user).order_by('is_read','-created_date') 
        serializer = UserNotificationSerializer(my_messages, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = UserNotificationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserNotificationDetail(generics.RetrieveAPIView):
    queryset = UserNotification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserNotificationSerializer
    lookup_field = "id"
    
    def get(self, request, id=None):
        UserNotification.objects.filter(id=id).update(is_read=True)
        return self.retrieve(request, id)
class MyNotificationCount(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user=request.user
        my_nots=UserNotification.objects.filter(reciver=user,is_read=False).count()
        return  Response(my_nots, status=status.HTTP_200_OK)
        
class MassEventNotifications(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserNotification.objects.all()
    serializer_class = MassNotificationSerializer
      
    def list(self, request):
        user=request.user
        my_messages=UserNotification.objects.filter(reciver=user,is_read=False).order_by('-created_date') 
        serializer = MassNotificationSerializer(my_messages, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = MassNotificationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                {"success":True,"title": request.data["title"],
                 "message":request.data["message"]}, 
                status=status.HTTP_201_CREATED)

class MassNotificationsUser(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSuperAdminPermission]
    queryset = UserNotification.objects.all()
    serializer_class = MassNotificationSerializer

    def post(self, request):
        data=request.data
        try:
            all_users=get_user_model().objects.all().exclude(phone=request.user.phone)
            obj=[UserNotification(sender=request.user,
                                                reciver=user,
                                                title=data["title"],message=data["message"]) for user in all_users]
            UserNotification.objects.bulk_create(obj)
            return Response({"success":True,"title":data["title"],"message":data["message"]},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )

        
class MassNotificationsOrganizationAdmins(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSuperAdminPermission]
    queryset = UserNotification.objects.all()

    def post(self, request):
        try:
            data=request.data
            org=Organization.objects.get(id=data["orgId"])
            org_admins=OrganizationUser.objects.filter(organization=org,user__role='admin')
            obj=[UserNotification(sender=request.user,reciver=org_admin.user,
                                                title=data["title"],message=data["message"]) for org_admin in org_admins]
            UserNotification.objects.bulk_create(obj)
            
            return Response({"success":True,"title":data["title"],"message":data["message"]},
                            status=status.HTTP_201_CREATED)     
        except Exception as e:
            print(e)
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )

                



class MassNotificationsOrganizationEventOrgs(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsAdminPermission]
    queryset = UserNotification.objects.all()

    def post(self, request):
        data=request.data
        try:
            org=OrganizationUser.objects.get(user=request.user).organization
            org_evnt=OrganizationUser.objects.filter(organization=org,user__role='event_org')
            obj=[UserNotification(sender=request.user,reciver=evt.user,
                                                title=data["title"],message=data["message"]) for evt in org_evnt]
            UserNotification.objects.bulk_create(obj)   
            return Response({"success":True,"title":data["title"],"message":data["message"]},
                            status=status.HTTP_201_CREATED)  
        except Exception as e:
            
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )
