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

from events.serializers import EventOrganizersSerializer, EventSerializer, EventsImageSerializer, EventsScheduleSerializer, EventsVolunteeringCategorySerializer, EventsVolunteersSerializer
from .models import Event, EventOrganizers,EventsImage, EventsSchedule, EventsVolunteeringCategory, EventsVolunteers
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
    
    
    

class EventsImageAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsImage.objects.all()
    serializer_class = EventsImageSerializer

    def post(self, request):
        serializer = EventsImageSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            new_data= serializer.data
            del new_data['image']
            images=EventsImage.objects.filter(event=Event.objects.get(id=request.data['eventId']))
            image_urls = [p.image.url for p in images]
            new_data["images"]=image_urls
            return Response(new_data, status=status.HTTP_201_CREATED)
        


class EventImageDelete(generics.DestroyAPIView):
    permission_classes = [IsEventOrgPermission]
    queryset = EventsImage.objects.all()
    lookup_field = "id"
    
    def delete(self, request, id=None):
        return self.destroy(request, id)
    
    

class EventsVolunteeringCategoryRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsEventOrgPermission)
    serializer_class = EventsVolunteeringCategorySerializer
    queryset = EventsVolunteeringCategory.objects.all()
    lookup_field = "id"
    
    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)
    
class EventsVolunteeringCategoryAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsVolunteeringCategory.objects.all()
    serializer_class = EventsVolunteeringCategorySerializer

    def post(self, request):
        serializer = EventsVolunteeringCategorySerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventsScheduleList(generics.ListAPIView):
       
    queryset = EventsSchedule.objects.all()
    serializer_class = EventsScheduleSerializer
    
    
    def get_queryset(self):
        eventID = self.request.query_params.get('eventId',None)
    
        if not Event.objects.filter(id=eventID).exists:
                raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        if eventID==None:
            return EventsSchedule.objects.all()
        else:
            return EventsSchedule.objects.filter(event=Event.objects.get(id=eventID))
            

    
    
class EventsScheduleAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsSchedule.objects.all()
    serializer_class = EventsScheduleSerializer

    def post(self, request):
        serializer = EventsScheduleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class EventsScheduleRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsEventOrgPermission)
    serializer_class = EventsScheduleSerializer
    queryset = EventsSchedule.objects.all()
    lookup_field = "id"
    
    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)
    



class EventsVolunteersAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsVolunteers.objects.all()
    serializer_class = EventsVolunteersSerializer

    def post(self, request):
        serializer = EventsVolunteersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        