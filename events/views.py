from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q, Count
# Create your views here.
import datetime

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from users.utils import CustomValidation

from utils.permissions import IsAdminPermission, IsEventOrgPermission, IsSuperAdminPermission
from users.models import (Organization, OrganizationUser, User)
from users.serializers import ( OrganizationSerializer, OrganizationUserSerializer, UserSerializer,LoginSerializer)

from events.serializers import EventOrganizersSerializer, EventSerializer
from .models import Event, EventOrganizers
# Create your views here.

class EventsList(generics.ListAPIView):
   
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    
class EventsAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request):
        serializer = EventSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class EventRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsEventOrgPermission)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = "id"
    
    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)
    
class EventOrganizersAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsAdminPermission)
    queryset = EventOrganizers.objects.all()
    serializer_class = EventOrganizersSerializer

    def post(self, request):
        serializer = EventOrganizersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class EventOrganizersOnEvent(generics.ListAPIView):
    permission_classes = [IsAdminPermission]
    serializer_class = EventOrganizersSerializer
    

    def get_queryset(self):
        eventID = self.request.query_params.get('eventId',None)
        
        if not Event.objects.filter(id=eventID).exists:
                raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        if eventID==None:
            return EventOrganizers.objects.all()
        else:
            return EventOrganizers.objects.filter(event=Event.objects.get(id=eventID))
            
    


class EventOrganizerDelete(generics.DestroyAPIView):
    permission_classes = [IsAdminPermission]
    queryset = EventOrganizers.objects.all()
    lookup_field = "id"
    
    def delete(self, request, id=None):
        return self.destroy(request, id)