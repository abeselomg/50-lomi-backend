
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from users.models import Organization, User ,OrganizationUser
from users.serializers import LoggedInUserSerializer, OrganizationSerializer, OrganizationUserSerializer
from users.utils import CustomValidation, validate_phone
from rest_framework_simplejwt.tokens import RefreshToken
from events.models import Campaign, CampaignVolunteer, Donation, Event, EventOrganizers, EventsImage, EventsSchedule, EventsVolunteeringCategory, EventsVolunteers, EventsVolunteersCertification, EventsVolunteersHours
from rest_framework.validators import UniqueTogetherValidator
        
        
class EventSerializer(serializers.ModelSerializer):
    organizationId = serializers.CharField(write_only=True)
    organization = OrganizationSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    event_volunteering_categories=serializers.SerializerMethodField()

    def get_images(self, obj):
        imgs = EventsImage.objects.filter(event=obj)
        return SimpleEventsImageSerializer(imgs, many=True).data
    def get_event_volunteering_categories(self, obj):
        cat = EventsVolunteeringCategory.objects.filter(event=obj)
        return EventsVolunteeringCategorySerializer(cat, many=True).data
    
    class Meta:
        model = Event
        fields = ["id","title","description","organization","starting_date",
                  "ending_date","address","contact_phone","contact_email",
                  "status","organizationId","images","event_volunteering_categories"]

    def create(self, validated_data):
        organization_id = validated_data.get("organizationId")
        validated_data.pop("organizationId")
        event = Event.objects.create(
            **validated_data, organization=Organization.objects.get(id=organization_id)
        )
        return event
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
   
   
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
                "detail", "Invalid Event Id", status.HTTP_400_BAD_REQUEST
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
    
    
    
    

class EventsVolunteersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    status = serializers.CharField(required=False,write_only=True,allow_blank=True)
    eventId = serializers.UUIDField(write_only=True)
    event = SimpleEventSerializer(read_only=True)
    volunteer=LoggedInUserSerializer(read_only=True)
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
                                                           'role':'volunteer'})
        
        if created:                                               
            user.set_password('123456789')
            user.save()
        
        evnt_vol,created=EventsVolunteers.objects.get_or_create(event=evnt,volunteer=user,
                                                                defaults={"status":"registered"})
        
        
        return evnt_vol
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    

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
        hrs=EventsVolunteersHours.objects.create(events_volunteers=vol,**validated_data)
        return hrs
    
    

class EventsVolunteersCertificationSerializer(serializers.ModelSerializer):
    userId=serializers.CharField(write_only=True)
    eventId=serializers.CharField(write_only=True)
    events_volunteers = EventsVolunteersSerializer(read_only=True)
    
    class Meta:
        model = EventsVolunteersCertification
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
        hrs=EventsVolunteersCertification.objects.create(events_volunteers=vol,**validated_data)
        return hrs
    
    
    
    
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