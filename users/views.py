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
from users.models import (Organization, OrganizationUser, User, UserMessage)
from users.serializers import ( OrganizationSerializer, OrganizationUserSerializer, UserMessageSerializer, UserSerializer,LoginSerializer)



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
        if user.id!=id:
            raise CustomValidation(
                "detail", "Unauthorized Access", status.HTTP_401_UNAUTHORIZED
            )
        return self.update(request, id)

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
        # orgId = self.request.query_params.get('orgId',None)
        
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
        my_messages=UserMessage.objects.filter(reciver=user,is_read=False)
        serializer = UserMessageSerializer(my_messages, many=True)
        return Response(serializer.data)
    

