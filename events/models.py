from uuid import uuid4
from django.db import models
from users.models import Organization,User,OrganizationUser
from users.utils import validate_phone
# Create your models here.



    

class Event(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title=models.CharField(max_length=255,blank=False,null=False)
    description=models.TextField()
    organization=models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True)
    starting_date=models.DateField()
    ending_date=models.DateField()
    address=models.CharField(max_length=255)
    contact_phone=models.CharField(max_length=255,validators=[validate_phone],default='')
    contact_email=models.EmailField(default='')
    status=models.CharField(max_length=255,default="upcoming",choices=(
    ("upcoming", "upcoming"),
    ("ongoing", "ongoing"),
    ("canceled", "canceled"),
    ("postponed", "postponed"),
    ("finished", "finished")
))
    
    

class EventOrganizers(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    organizer=models.ForeignKey(OrganizationUser,on_delete=models.CASCADE) 
    
    class Meta:
        unique_together = ('event', 'organizer')

class EventsImage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    image=models.ImageField()



class EventsSchedule(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    date=models.DateField()
    session_name=models.CharField(max_length=255)
    starting_time=models.TimeField()
    ending_time=models.TimeField()
    venue=models.CharField(max_length=255,blank=True,default='')



class EventsVolunteeringCategory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    category_name=models.CharField(max_length=255)



class EventsVolunteers(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    volunteer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    events_volunteering_category=models.ForeignKey(EventsVolunteeringCategory,on_delete=models.SET_NULL,null=True)
    status=models.CharField(max_length=255,choices=(
    ("registered", "registered"),
    ("unregistered", "unregistered")
))
    registery_date=models.DateTimeField(auto_now_add=True)
    # add reward feature
    
    class Meta:
        unique_together = ('event', 'volunteer')


class EventsVolunteersHours(models.Model):
    events_volunteers=models.ForeignKey(EventsVolunteers,on_delete=models.CASCADE)
    date=models.DateField()
    attended=models.BooleanField()
    daily_total_hours=models.FloatField()

