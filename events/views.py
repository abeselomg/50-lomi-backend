import json
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q, Count,Sum
# Create your views here.
from users.utils import status_updater
from datetime import datetime
from django.forms.models import model_to_dict
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from users.utils import CustomValidation
from utils.pagination import CustomPagination

from utils.permissions import IsAdminPermission, IsEventOrgPermission, IsSuperAdminPermission
from users.models import (Organization, OrganizationUser, User)
from users.serializers import ( OrganizationSerializer, OrganizationUserSerializer, UserSerializer,LoginSerializer)

from events.serializers import SuperCategorySerializer,EventCertificateSerializer, CampaignManagerSerializer,EventsVolunteeringCategoryBulkSerializer, CampaignSerializer, CampaignVolunteersSerializer, DonationSerializer, EventOrganizersSerializer, EventSerializer, EventsImageSerializer, EventsScheduleSerializer, EventsVolunteeringCategorySerializer, EventsVolunteersCertificationSerializer, EventsVolunteersHoursSerializer, EventsVolunteersSerializer, VolunteerHistorySerializer
from .models import Campaign,SuperCategory,EventCertificate, CampaignVolunteer, Donation, Event, EventOrganizers,EventsImage, EventsSchedule, EventsVolunteeringCategory, EventsVolunteers, EventsVolunteersCertification, EventsVolunteersHours
# Create your views here.

class SuperCategoryList(generics.ListAPIView):
    queryset=SuperCategory.objects.all()
    serializer_class=SuperCategorySerializer


class EventsList(generics.ListAPIView):
   
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class=CustomPagination
    
    def get_queryset(self):
        queryset = Event.objects.all().order_by('-created_date')
        orgID = self.request.query_params.get('orgId',None)
        categoryID = self.request.query_params.get('categoryID',None)
        
        if orgID!=None:
            if not Organization.objects.filter(id=orgID).exists():
                    raise CustomValidation(
                "detail", "Invalid Organization Id", status.HTTP_400_BAD_REQUEST
            )
            return queryset.filter(organization=Organization.objects.get(id=orgID))
           
           
        if categoryID!=None:
            if not SuperCategory.objects.filter(id=categoryID).exists():
                    raise CustomValidation(
                "detail", "Invalid Category Id", status.HTTP_400_BAD_REQUEST
            )
            return queryset.filter(status='upcoming',general_category=SuperCategory.objects.get(id=categoryID))
        else:
            return queryset.filter(status='upcoming')
        
        
        
class EventsAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request):
        serializer = EventSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        


class EventDetail(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = "id"
    
    def get(self, request, id=None):
        st=['ongoing','upcoming']
        if Event.objects.get(id=id).status in st:
            obj=Event.objects.get(id=id)
            status=status_updater(obj.starting_date,obj.ending_date)
            if status is not None:
                Event.objects.filter(id=id).update(status=status)
                
        return self.retrieve(request, id)
    

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

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# EventsVolunteeringCategoryBulkSerializer


class EventImageDelete(generics.DestroyAPIView):
    permission_classes = [IsEventOrgPermission]
    queryset = EventsImage.objects.all()
    lookup_field = "id"
    
    def delete(self, request, id=None):
        return self.destroy(request, id)
    


class EventsVolunteeringCategoryBulkAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsVolunteeringCategory.objects.all()
    serializer_class = EventsVolunteeringCategoryBulkSerializer

    def post(self, request):
        serializer = EventsVolunteeringCategoryBulkSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    
    queryset = EventsVolunteers.objects.all()
    serializer_class = EventsVolunteersSerializer

    def post(self, request):
        serializer = EventsVolunteersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class EventsVolunteersList(generics.ListAPIView):
       
    queryset = EventsVolunteers.objects.all()
    serializer_class = EventsVolunteersSerializer
    pagination_class=CustomPagination
    
    
    def get_queryset(self):
        eventID = self.request.query_params.get('eventId',None)
    
        if not Event.objects.filter(id=eventID).exists:
                raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        if eventID==None:
            return EventsVolunteers.objects.all()
        else:
            return EventsVolunteers.objects.filter(event=Event.objects.get(id=eventID))
            

    


    
class EventsVolunteersHoursAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsVolunteersHours.objects.all()
    serializer_class = EventsVolunteersHoursSerializer

    def post(self, request):
        serializer = EventsVolunteersHoursSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
 
class EventCertificateAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventCertificate.objects.all()
    serializer_class = EventCertificateSerializer   
    
    
    def post(self, request):
        serializer = EventCertificateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)         
        
class EventsVolunteersCertificationAdd(generics.CreateAPIView):
    permission_classes= (permissions.IsAuthenticated,IsEventOrgPermission)
    queryset = EventsVolunteersCertification.objects.all()
    serializer_class = EventsVolunteersCertificationSerializer

    def post(self, request):
        serializer = EventsVolunteersCertificationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success":True}, status=status.HTTP_201_CREATED)
             
   
   
class CampaignList(generics.ListAPIView):
       
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer 
    pagination_class=CustomPagination
    def get_queryset(self):
        orgId = self.request.query_params.get('orgId',None)
        queryset = Campaign.objects.all()
        if orgId!=None:
            return queryset.filter(organization=Organization.objects.get(id=orgId))
        return queryset
    
    
class CampaignAdd(generics.CreateAPIView):
    permission_classes= [permissions.IsAuthenticated]
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def post(self, request):
        serializer = CampaignSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
             
        
    
class AddCampaignManager(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CampaignManagerSerializer
    queryset = Campaign.objects.all()
    lookup_field = "id"
    

    def put(self, request, id=None):
        return self.partial_update(request, id)

    
class CampaignVolunteerAdd(generics.CreateAPIView):
    queryset = CampaignVolunteer.objects.all()
    serializer_class = CampaignVolunteersSerializer

    def post(self, request):
        serializer = CampaignVolunteersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
             
        
class DonationAdd(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsAdminPermission]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    pagination_class=CustomPagination


    def post(self, request):
        serializer = DonationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)





####################################################  Volunteer Related Queries  ################################################################

class VolunteerHistory(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EventsVolunteers.objects.all()
    serializer_class = VolunteerHistorySerializer
    pagination_class=CustomPagination
      
    def list(self, request):
        user=request.user
        volunteer=EventsVolunteers.objects.exclude(event__status='upcoming').filter(volunteer=user)
        
        serializer = VolunteerHistorySerializer(volunteer, many=True)
        return Response(serializer.data)
    
    
    
class VolunteerDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user=request.user
        allevents=EventsVolunteers.objects.filter(volunteer=user)
        ongoing_events=allevents.filter(event__status="ongoing")
        total_hrs=0
        my_participations=[]
        for e in allevents:
            event=e.event
    
            if event.status=='finished':
                total_days=abs((event.starting_date - event.ending_date).days)
                absent_days=EventsVolunteersHours.objects.filter(events_volunteers=e).count()
                hr=8*(total_days-absent_days)
            elif event.status=='ongoing':
                today=datetime.today().date()
                total_days=abs((event.starting_date - today).days)
                absent_days=EventsVolunteersHours.objects.filter(events_volunteers=e).count()
                hr=8*(total_days-absent_days)
            else:
                hr=0
            
            participant={"hours":hr, "value":model_to_dict(event)}
            my_participations.append(participant)
            total_hrs+=hr


 
        return Response({
            "total_events":allevents.count(),
            "ongoing_events":ongoing_events.count(),
            "total_hours":total_hrs,
            "total_certifications":0,
            "sorted_events_per_hours":sorted(my_participations, key=lambda d: d['hours'],reverse=True)   ,
            
        })
           
    
    
    
    
    
####################################################   ################################################################
    
    
    

        
class EventDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated,IsEventOrgPermission]

    def get(self, request, format=None):
        user=request.user
        
        listofparticipants=[]
        
        org=OrganizationUser.objects.get(user=user).organization
        allevents=Event.objects.filter(organization=org)

        total_participants=0
        for event in allevents:
            participant={"count":EventsVolunteers.objects.filter(event=event).count(), "value":model_to_dict(event)}
            listofparticipants.append(participant)
            total_participants+=EventsVolunteers.objects.filter(event=event).count()


 
        return Response({
            "allevents":allevents.count(),
            "ongoing_events":allevents.filter(status="ongoing").count(),
            "total_participants":total_participants,
            "sorted_events_per_participants":sorted(listofparticipants, key=lambda d: d['count'],reverse=True)   ,
        })
        
        
class AdminDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated,IsAdminPermission]


    def get(self, request, format=None):
        user=request.user
        
        listofparticipants=[]
        
        org=OrganizationUser.objects.get(user=user).organization
        allcampaigns=Campaign.objects.filter(organization=org)
        allevents=Event.objects.filter(organization=org)

        total_donations=Donation.objects.filter(campaign__organization=org).aggregate(Sum('amount'))
        total_participants=0
        for camp in allcampaigns:
            participant={"count":CampaignVolunteer.objects.filter(campaign=camp).count(), "value":model_to_dict(camp)}
            listofparticipants.append(participant)
            total_participants+=CampaignVolunteer.objects.filter(campaign=camp).count()
            


 
        return Response({
            "allevents":allevents.count(),
            "allcampaigns":allcampaigns.count(),
            "total_donations":total_donations['amount__sum'],
            "total_participants":total_participants,
            "sorted_campaigns_per_participants":sorted(listofparticipants, key=lambda d: d['count'],reverse=True) ,
        })
        
        
