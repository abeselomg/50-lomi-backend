from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q, Count
# Create your views here.
import datetime
from django.http import HttpResponse

# from elasticsearch_dsl import Q as ES_Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from utils.permissions import IsAdminPermission, IsSuperAdminPermission
from users.models import (Organization, OrganizationUser, User)
from users.serializers import ( OrganizationSerializer, OrganizationUserSerializer, UserSerializer,LoginSerializer)



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
    
class OrganizationAdminAdd(generics.CreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.IsAuthenticated,IsSuperAdminPermission)

    def post(self, request):
        serializer = OrganizationUserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrganizationEventOrganizerAdd(generics.CreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.IsAuthenticated,IsAdminPermission)

    def post(self, request):
        serializer = OrganizationUserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

