from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    UserManager,
)
from .utils import validate_phone
from uuid import uuid4


class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None, **extra_fields):
        """Creates and Save a new User"""
        if not phone:
            raise ValueError("User must have phone number")

        user = self.model(
            first_name=first_name, last_name=last_name, phone=phone, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, phone,role, password):
        """Creates and save a new superuser"""
        if not phone:
            raise ValueError("User must have phone number")
        user = self.model(first_name=first_name, last_name=last_name, phone=phone,role=role)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model using phone number insteadof email
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    phone = models.CharField(max_length=15, unique=True, validators=[validate_phone])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email=models.EmailField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(
        max_length=128, choices=(
    ("volunteer", "volunteer"),
    ("event_org", "event_org"),
    ("admin", "admin"),
    ("superadmin", "superadmin")
)
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
        "role"
    )

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


User = get_user_model()




class Organization(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name=models.CharField(max_length=255,blank=False,null=False)
    description=models.TextField(blank=True,default='')
    contact_phone=models.CharField(max_length=15, unique=True, validators=[validate_phone])
    contact_email=models.EmailField()
    legal_document=models.FileField()
    regulation_body_account_id=models.FileField()
    is_verified=models.BooleanField(default=False)
    verification_date=models.DateTimeField(auto_now=True)
    verification_notes=models.TextField(blank=True,default='')

    
    def __str__(self):
        return self.name



class OrganizationUser(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
