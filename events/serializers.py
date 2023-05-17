
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from users.models import Organization, User ,OrganizationUser
from users.serializers import LoggedInUserSerializer, OrganizationSerializer, OrganizationUserSerializer
from users.utils import CustomValidation, validate_phone
from rest_framework_simplejwt.tokens import RefreshToken
from events.models import (Campaign,SuperCategory, CampaignVolunteer, Donation, Event, EventOrganizers, EventsImage,
                           EventsSchedule, EventsVolunteeringCategory, EventsVolunteers,EventCertificate, EventsVolunteersCertification, EventsVolunteersHours)
from rest_framework.validators import UniqueTogetherValidator
from datetime import datetime
from django.db import IntegrityError
       
        
class SuperCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = SuperCategory
            fields="__all__"
    
    
    
class EventSerializer(serializers.ModelSerializer):
    organizationId = serializers.CharField(write_only=True)
    categoryId= serializers.CharField(write_only=True)
    organization = OrganizationSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    event_volunteering_categories=serializers.SerializerMethodField()
    general_category=SuperCategorySerializer(read_only=True)
    event_certificate=serializers.SerializerMethodField()

    def get_images(self, obj):
        imgs = EventsImage.objects.filter(event=obj)
        return SimpleEventsImageSerializer(imgs, many=True).data
    def get_event_volunteering_categories(self, obj):
        cat = EventsVolunteeringCategory.objects.filter(event=obj)
        return EventsVolunteeringCategorySerializer(cat, many=True).data
    def get_event_certificate(self, obj):
        return EventCertificate.objects.filter(event=obj).exists()
    
    class Meta:
        model = Event
        fields = ["id","title","description","organization","general_category","starting_date",
                  "ending_date","address","contact_phone","contact_email",
                  "status","organizationId","categoryId","images","event_volunteering_categories","event_certificate"]

    def create(self, validated_data):
        organization_id = validated_data.pop("organizationId")
        category_id=validated_data.pop("categoryId")
        category=SuperCategory.objects.get(id=category_id)
        event = Event.objects.create(
            **validated_data, organization=Organization.objects.get(id=organization_id),general_category=category
        )
        return event
    
    def update(self, instance, validated_data):
        cat_id = validated_data.pop("categoryId", None)
        event = super().update(instance, validated_data)
        if cat_id:
            category=SuperCategory.objects.get(id=cat_id)
            print(event)
            event.general_category=category
            event.save()

        return event

    
   
   
class SimpleOrganizationUserSerializer(serializers.ModelSerializer):
    user=LoggedInUserSerializer(read_only=True)
    class Meta:
        model = OrganizationUser
        fields = ["user"]


class SimpleEventSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        imgs = EventsImage.objects.filter(event=obj)
        return SimpleEventsImageSerializer(imgs, many=True).data
    
    class Meta:
        model = Event
        fields = ["id","title","starting_date",
                  "ending_date","status","images"]
            
    
class EventOrganizersSerializer(serializers.ModelSerializer):
    eventId = serializers.UUIDField(write_only=True)
    organizationId = serializers.UUIDField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    email = serializers.CharField(required=False,write_only=True,allow_blank=True)
    password = serializers.CharField(write_only=True) 
    
    event = EventSerializer(read_only=True)
    organizer=SimpleOrganizationUserSerializer(read_only=True)

    class Meta:
        model = EventOrganizers
        fields = "__all__"
        
    def create(self, validated_data):
        org_id=validated_data['organizationId']
        event_id=validated_data['eventId']
        
        if not Organization.objects.filter(id=org_id).exists():
            raise CustomValidation(
                "detail", "Invalid Organization Id", status.HTTP_400_BAD_REQUEST
            )
        if not Event.objects.filter(id=event_id).exists():
                raise CustomValidation(
                "detail","Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        organization_value=Organization.objects.get(id=org_id)
        validated_data.pop("organizationId")
        validated_data.pop("eventId")
  
        user,created=User.objects.get_or_create(phone=validated_data['phone'],
                                                defaults={'first_name':validated_data['first_name'],
                                                          'last_name':validated_data['last_name'],
                                                          'role':'event_org'})
        if created:                                               
            user.set_password(validated_data['password'])
            user.save()
            
        org_user,created=OrganizationUser.objects.get_or_create(user=user,organization=organization_value)
        
        
        event_org,created = EventOrganizers.objects.get_or_create(
            organizer=org_user,
            event=Event.objects.get(id=event_id)
        )
        return event_org
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class SimpleEventsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsImage
        fields = ["id","image"]

class EventsImageSerializer(serializers.ModelSerializer):
    eventId = serializers.UUIDField(write_only=True)

    upload_image = serializers.ListField( 
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False)
        ,write_only = True
    )
    event = EventSerializer(read_only=True)
    image=serializers.ImageField(read_only=True)
    
    class Meta:
        model = EventsImage
        fields = "__all__"
        
    def create(self, validated_data):
        
        event_id=validated_data['eventId']
        uploaded_data = validated_data.pop('upload_image')
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        validated_data.pop("eventId")
        evnt=Event.objects.get(id=event_id)
        for item in uploaded_data:
            photo=EventsImage.objects.create(image=item,event=evnt)
        
        return photo
                
        
        
        
class EventsVolunteeringCategorySerializer(serializers.ModelSerializer):
    eventId = serializers.UUIDField(write_only=True)

    class Meta:
        model = EventsVolunteeringCategory
        fields = ["category_name","id","eventId"]
        
    def create(self, validated_data):
        event_id=validated_data['eventId']
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        validated_data.pop("eventId")
        evnt=Event.objects.get(id=event_id)
        category=EventsVolunteeringCategory.objects.create(**validated_data,event=evnt)
        return category
    
    
class EventsVolunteeringCategoryBulkSerializer(serializers.ModelSerializer):
    eventId = serializers.UUIDField(write_only=True)

    category_name = serializers.ListField( 
        child = serializers.CharField()
        ,write_only = True
    )
    event = EventSerializer(read_only=True)
    image=serializers.CharField(read_only=True)
    
    class Meta:
        model = EventsVolunteeringCategory
        fields = "__all__"
        
    def create(self, validated_data):
        
        event_id=validated_data['eventId']
        uploaded_data = validated_data.pop('category_name')
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        validated_data.pop("eventId")
        evnt=Event.objects.get(id=event_id)
        for item in uploaded_data:
                category=EventsVolunteeringCategory.objects.create(category_name=item,event=evnt)
        
        return category

                
    
    
    
class EventsScheduleSerializer(serializers.ModelSerializer):
    eventId = serializers.UUIDField(write_only=True)
    class Meta:
        model = EventsSchedule
        fields =["id","date","session_name","starting_time","ending_time","venue","eventId"]
        
    def create(self, validated_data):
        event_id=validated_data['eventId']
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        validated_data.pop("eventId")
        evnt=Event.objects.get(id=event_id)
        schedule=EventsSchedule.objects.create(**validated_data,event=evnt)
        return schedule
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class VolunteerHistorySerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    volunteer=LoggedInUserSerializer(read_only=True)
    volunteer_hrs=serializers.SerializerMethodField()
    # volunteer_Certification=serializers.SerializerMethodField()
    achievment=serializers.SerializerMethodField()
    certificate=serializers.SerializerMethodField()
    
    
    
    def get_volunteer_hrs(self, obj):
        def days_between(d1, d2):
            return abs((d2 - d1).days)
        
            
        event=obj.event
        if event.status=='finished':
            total_days=days_between(event.starting_date, event.ending_date)
            absent_days=EventsVolunteersHours.objects.filter(events_volunteers=obj).count()
            return 8*(total_days-absent_days)
        elif event.status=='ongoing':
            today=datetime.today().date()
            total_days=days_between(event.starting_date, today)
            absent_days=EventsVolunteersHours.objects.filter(events_volunteers=obj).count()
            return 8*(total_days-absent_days)
        else:
            return 0
    
    def get_achievment(self, obj):
        absent_days=EventsVolunteersHours.objects.filter(events_volunteers=obj).count()
        tag="Perfect Streak" if absent_days==0 else "Decent Streak" if absent_days<3 else "Poor Streak"
        return tag
    
    def get_certificate(self,obj):
        event=obj.event 
        if EventCertificate.objects.filter(event=event).exists():
            event_certeficate=EventCertificate.objects.get(event=event)
            if EventsVolunteersCertification.objects.filter(events_volunteers=obj,event_certeficate=event_certeficate).exists():
                return True
        return False
        
    
    

    class Meta:
        model = EventsVolunteers
        fields =["id","event","volunteer",
                 "events_volunteering_category",
                 "volunteer_hrs","achievment","certificate"]
        
        
class EventsVolunteersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True,required=False,allow_blank=True)
    status = serializers.CharField(required=False,write_only=True,allow_blank=True)
    eventId = serializers.UUIDField(write_only=True)
    event = SimpleEventSerializer(read_only=True)
    volunteer=LoggedInUserSerializer(read_only=True)
    volunteer_hrs=serializers.SerializerMethodField()
    volunteer_history=serializers.SerializerMethodField()
    

    def get_volunteer_hrs(self, obj):
        hrs = EventsVolunteersHours.objects.filter(events_volunteers=obj,date=datetime.now().date())
        return SimpleEventsVolunteersHoursSerializer(hrs, many=True).data
    
    def get_volunteer_history(self, obj):
        org=obj.event.organization
        history_count=EventsVolunteers.objects.filter(event__organization=org,volunteer=obj.volunteer).count()
        return history_count
    # EventsVolunteersHoursSerializer
    class Meta:
        model = EventsVolunteers
        fields ="__all__"
 
    def create(self, validated_data):
        event_id=validated_data['eventId']
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
        validated_data.pop("eventId")
        evnt=Event.objects.get(id=event_id)
        user,created=User.objects.get_or_create(phone=validated_data['phone'],
                                                defaults={'first_name':validated_data['first_name'],
                                                          'last_name':validated_data['last_name'],
                                                          'email':validated_data.get('email',''),
                                                           'role':'volunteer'})
        
        if created:                                               
            user.set_password('123456789')
            user.save()
        
        evnt_vol,created=EventsVolunteers.objects.get_or_create(event=evnt,volunteer=user,
                                                                defaults={"status":"registered"})
        return evnt_vol
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class SimpleEventsVolunteersHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsVolunteersHours
        fields =["id","date","attended"]
class EventsVolunteersHoursSerializer(serializers.ModelSerializer):
    userId=serializers.CharField(write_only=True)
    eventId=serializers.CharField(write_only=True)
    events_volunteers = EventsVolunteersSerializer(read_only=True)
    
    class Meta:
        model = EventsVolunteersHours
        fields ="__all__"
        
    def create(self, validated_data):
        event_id=validated_data.pop('eventId')
        user_id=validated_data.pop('userId')
        
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
            
        if not User.objects.filter(id=user_id).exists():
            raise CustomValidation(
            "detail", "Invalid User Id", status.HTTP_400_BAD_REQUEST
        )
            
        user=User.objects.get(id=user_id)
        event=Event.objects.get(id=event_id)
        vol=EventsVolunteers.objects.get(event=event,volunteer=user) 
        hrs,created=EventsVolunteersHours.objects.get_or_create(events_volunteers=vol,date=validated_data['date'],
                                                defaults={'attended':validated_data['attended']})
        # hrs=EventsVolunteersHours.objects.create(events_volunteers=vol,**validated_data)
        return hrs
    
    
class EventCertificateSerializer(serializers.ModelSerializer):
    eventId=serializers.CharField(write_only=True)
    
    class Meta:
        model = EventCertificate
        fields ="__all__"
        
        
    def create(self, validated_data):
        event_id=validated_data.pop('eventId')
        
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
            
        event=Event.objects.get(id=event_id)
        certificate=EventCertificate.objects.create(event=event,**validated_data)
        return certificate
        
class EventsVolunteersCertificationSerializer(serializers.ModelSerializer):
    # minHour=serializers.FloatField(write_only=True)
    eventId=serializers.CharField(write_only=True)
    events_volunteers = EventsVolunteersSerializer(read_only=True)
    event_certeficate= EventsVolunteersSerializer(read_only=True)
    
    class Meta:
        model = EventsVolunteersCertification
        fields ="__all__"
        
    def create(self, validated_data):
        event_id=validated_data.pop('eventId')
        # min_hour=validated_data.pop('minHour')
        
        if not Event.objects.filter(id=event_id).exists():
            raise CustomValidation(
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
            )
            
        event=Event.objects.get(id=event_id)
        
        if not EventCertificate.objects.filter(event=event).exists():
                raise CustomValidation(
                "detail", "No Certificate has been created under this event", status.HTTP_400_BAD_REQUEST
            )
                
        try:
            event_certeficate=EventCertificate.objects.get(event=event)
            vols=EventsVolunteers.objects.filter(event=event)
            obj=[EventsVolunteersCertification(events_volunteers=vol,event_certeficate=event_certeficate) for vol in vols]
            
            EventsVolunteersCertification.objects.bulk_create(obj) 
            
            return {"success":True}
        except IntegrityError as e: 
            raise CustomValidation(
                "detail", "Certificate for volunteers has already been created.", status.HTTP_400_BAD_REQUEST
            )

    
    
    
    
class CampaignSerializer(serializers.ModelSerializer):
    organizationId = serializers.UUIDField(write_only=True)
    organization = OrganizationSerializer(read_only=True)
    campaign_manager = LoggedInUserSerializer(read_only=True)
    class Meta:
        model = Campaign
        fields ="__all__"
        
    def create(self, validated_data):
        organization_id=validated_data.pop("organizationId")
        if not Organization.objects.filter(id=organization_id).exists():
                raise CustomValidation(
                "detail", "Invalid Organization Id", status.HTTP_400_BAD_REQUEST
            )
        
        org=Organization.objects.get(id=organization_id)
        camp=Campaign.objects.create(**validated_data,organization=org)
        return camp
    
    
class CampaignManagerSerializer(serializers.ModelSerializer):
    managerId = serializers.UUIDField(write_only=True)
    campaign_manager = LoggedInUserSerializer(read_only=True)
    
    class Meta:
        model = Campaign
        fields ="__all__"
        
    def update(self, instance, validated_data):
        managerId=validated_data.pop("managerId")
        if not User.objects.filter(id=managerId).exists():
                raise CustomValidation(
                "detail", "Invalid Organization Id", status.HTTP_400_BAD_REQUEST
            )
        
        usr=User.objects.get(id=managerId)
        instance.campaign_manager = usr
            
        instance.save()
        return instance
    
    
    
class CampaignVolunteersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    campaignId = serializers.UUIDField(write_only=True)
    volunteer=LoggedInUserSerializer(read_only=True)
    class Meta:
        model = CampaignVolunteer
        fields ="__all__"
 
    def create(self, validated_data):
        campaign_id=validated_data.pop("campaignId")
        if not Campaign.objects.filter(id=campaign_id).exists():
            raise CustomValidation(
                "detail", "Invalid Campaign Id", status.HTTP_400_BAD_REQUEST
            )
        
        camp=Campaign.objects.get(id=campaign_id)
        user,created=User.objects.get_or_create(phone=validated_data['phone'],
                                                defaults={'first_name':validated_data['first_name'],
                                                          'last_name':validated_data['last_name'],
                                                           'role':'volunteer'})
        
        if created:                                               
            user.set_password('123456789')
            user.save()
        
        camp_vol,created=CampaignVolunteer.objects.get_or_create(campaign=camp,volunteer=user)
        
        return camp_vol
    
    
    
class DonationSerializer(serializers.ModelSerializer):
    campaignId = serializers.UUIDField(write_only=True)
    organization = OrganizationSerializer(read_only=True)
    campaign=CampaignSerializer(read_only=True)
    
    class Meta:
        model = Donation
        fields ="__all__"
        
    def create(self, validated_data):
        campaign_id=validated_data.pop("campaignId")
        if not Campaign.objects.filter(id=campaign_id).exists():
                raise CustomValidation(
                "detail", "Invalid Campaign Id", status.HTTP_400_BAD_REQUEST
            )
         
        camp=Campaign.objects.get(id=campaign_id)
        don=Donation.objects.create(**validated_data,campaign=camp)
        return don