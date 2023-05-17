
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response

from events.models import Event, EventsVolunteers
from .utils import CustomValidation, validate_phone
from .models import Organization, OrganizationUser, User, UserMessage,UserNotification
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserSerializer(serializers.ModelSerializer):
    """serializer for the users objects"""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "profile_pic",
            "phone",
            "email",
            "changed_password",
            "password",
            "role"
        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        if validated_data['role']!='volunteer':
            raise CustomValidation(
                "detail", "You are not authorized to register with this role.", status.HTTP_401_UNAUTHORIZED
            )
        user = User.objects.create_user(**validated_data)
        
        token=get_tokens_for_user(user=user)
        
        data = LoggedInUserSerializer(user)
        
        return {
            "user_data": data.data,
            "token":token
        }

    def update(self, instance, validated_data):
        """Update a user"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    """serializer for user login"""

    phone = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    class Meta:
        model = get_user_model()
            
        fields = ("phone", "password", "first_name", "last_name","role","email","changed_password","profile_pic")
            
        read_only_fields = ("first_name", "last_name","role","email","changed_password","profile_pic")

    def validate(self, data):
        """Validate user data"""
        validate_phone(data.get("phone", None))
        
        user = authenticate(
            phone=data.get("phone", None), password=data.get("password", None)
        )

        if not user:
            raise CustomValidation(
                "detail", "Invalid Credentials", status.HTTP_401_UNAUTHORIZED
            )

        token=get_tokens_for_user(user=user)
        
        data = LoggedInUserSerializer(user)
        
        if user.role=='admin' or user.role=='event_org':
            try:
                org=OrganizationUser.objects.get(user=user).organization
                org_data=Organization.objects.filter(id=org.id).values()
                return Response(
                {
                    "user": data.data,
                    "token":token,
                    "org":org_data
                },
                status=status.HTTP_200_OK,
            )
            except Exception as e:
                raise CustomValidation(
                "detail", e, status.HTTP_401_UNAUTHORIZED
            )
            
        
       
        return Response(
            {
                "user": data.data,
                 "token":token
            },
            status=status.HTTP_200_OK,
        )


class LoggedInUserSerializer(serializers.ModelSerializer):
    """
    return the logged in user info
    """

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "role",
            "first_name",
            "last_name",
            "email",
            "changed_password",
            "profile_pic"
            
        )



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields = "__all__"
        
        extra_kwargs = {
            "id": {"read_only": True},
        }
        
    def update(self, instance, validated_data):
            return super().update(instance, validated_data)
        
        
class OrganizationUserSerializer(serializers.ModelSerializer):
    organizationId = serializers.UUIDField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    email = serializers.CharField(required=False,write_only=True,allow_blank=True)
    role = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)    

    organization = OrganizationSerializer(read_only=True)
    user=LoggedInUserSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = "__all__"

    def create(self, validated_data):
        valid_roles=['admin','event_org']
        org_id=validated_data['organizationId']
        if not Organization.objects.get(id=org_id):
            raise CustomValidation(
                "detail", "Invalid Organization Id", status.HTTP_400_BAD_REQUEST
            )
        organization_value=Organization.objects.get(id=org_id)
        validated_data.pop("organizationId")
        validate_phone(validated_data['phone'])
        if validated_data['role'] not in valid_roles:
            raise CustomValidation(
                "detail", "Incorrect role. Only admin or event organizer role can be created.", status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(phone=validated_data['phone']).exists():
            raise CustomValidation(
                "detail", "Phone number already exists.", status.HTTP_400_BAD_REQUEST
            )
        try:
            password=validated_data.pop('password')
            user = User.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()
            
            admin = OrganizationUser.objects.create(
                user=user, organization=organization_value
            )
            return admin
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )
        
    
    
    
class UserMessageSerializer(serializers.ModelSerializer):
    reciverId = serializers.UUIDField(write_only=True)
    sender=LoggedInUserSerializer(read_only=True)
    reciver=LoggedInUserSerializer(read_only=True)

    
    class Meta:
        model = UserMessage
        fields = "__all__"

    def create(self, validated_data):
        sender_user =  self.context['request'].user
        try:
            reciver_user=User.objects.get(id=validated_data.pop("reciverId")) 
            user_mes=UserMessage.objects.create(sender=sender_user,reciver=reciver_user,**validated_data)
            return user_mes
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )
            
        #    raise Exception(e)

        
        
    

class UserNotificationSerializer(serializers.ModelSerializer):
    reciverId = serializers.UUIDField(write_only=True)
    sender=LoggedInUserSerializer(read_only=True)
    reciver=LoggedInUserSerializer(read_only=True)

    
    class Meta:
        model = UserNotification
        fields = "__all__"

    def create(self, validated_data):
        sender_user =  self.context['request'].user
        try:
            reciver_user=User.objects.get(id=validated_data.pop("reciverId")) 
            user_noti=UserNotification.objects.create(sender=sender_user,reciver=reciver_user,**validated_data)
            return user_noti
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )

    
    
class MassNotificationSerializer(serializers.ModelSerializer):
    eventId = serializers.UUIDField(write_only=True)
    sender=LoggedInUserSerializer(read_only=True)
    reciver=LoggedInUserSerializer(read_only=True)

    
    class Meta:
        model = UserNotification
        fields = "__all__"

    def create(self, validated_data):
        
        sender_user =  self.context['request'].user
        event=Event.objects.get(id=validated_data.pop("eventId"))
        try:
            event_vols=EventsVolunteers.objects.filter(event=event)
            obj=[UserNotification(sender=sender_user,
                                                reciver=vol.volunteer,
                                                title=validated_data["title"],message=validated_data["message"]) for vol in event_vols]
            noti=UserNotification.objects.bulk_create(obj)
            return noti
        except Exception as e:
            raise CustomValidation(
                "detail", e, status.HTTP_400_BAD_REQUEST
            )
