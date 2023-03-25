
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from users.models import Organization, User ,OrganizationUser
from users.serializers import LoggedInUserSerializer, OrganizationSerializer, OrganizationUserSerializer
from users.utils import CustomValidation, validate_phone
from rest_framework_simplejwt.tokens import RefreshToken
from events.models import Event, EventOrganizers, EventsImage

        
        
class EventSerializer(serializers.ModelSerializer):
    organizationId = serializers.CharField(write_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

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
        
        org_user,created=OrganizationUser.objects.get_or_create(user=user,organization=organization_value)
        print('org user created',created)
        
        event_org,created = EventOrganizers.objects.get_or_create(
            organizer=org_user,
            event=Event.objects.get(id=event_id)
        )
        return event_org
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    


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
                
        