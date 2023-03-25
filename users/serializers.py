
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from .utils import CustomValidation, validate_phone
from .models import Organization, OrganizationUser, User
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
            "phone",
            "email",
            "password",
            "role"
        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        
        print(validated_data)
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
        fields = ("phone", "password", "first_name", "last_name","role","email")
        read_only_fields = ("first_name", "last_name","role","email")

    def validate(self, data):
        """Validate user data"""
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
            "email"
        )



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields = "__all__"
        
        extra_kwargs = {
            "id": {"read_only": True},
        }
        
        def update(self, instance, validated_data):
            instance.name = validated_data.get("name", instance.name)
            instance.description = validated_data.get("description", instance.description)
            instance.contact_phone = validated_data.get("contact_phone", instance.contact_phone)
            instance.contact_email = validated_data.get("contact_email", instance.contact_email)
            instance.legal_document = validated_data.get("legal_document", instance.legal_document)
            instance.regulation_body_account_id = validated_data.get("regulation_body_account_id", instance.regulation_body_account_id)
            instance.is_verified = validated_data.get("is_verified", instance.is_verified)
            instance.verification_notes = validated_data.get("verification_notes", instance.verification_notes)
            
            
            instance.save()
            return instance
        
        
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
        user = User.objects.create_user(**validated_data)
        admin = OrganizationUser.objects.create(
            user=user, organization=organization_value
        )
        return admin
    
    
