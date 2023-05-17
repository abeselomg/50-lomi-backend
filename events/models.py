from uuid import uuid4
from django.db import models
from users.models import Organization,User,OrganizationUser
from users.utils import validate_phone
from django.utils import timezone
# Create your models here.


class SuperCategory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title=models.CharField(max_length=255,blank=False,null=False)
    description=models.TextField()
    
    def __str__(self):
        return self.title
        
    

class Event(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title=models.CharField(max_length=255,blank=False,null=False)
    description=models.TextField()
    organization=models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True)
    general_category=models.ForeignKey(SuperCategory,on_delete=models.SET_NULL,null=True)
    starting_date=models.DateField()
    ending_date=models.DateField()
    address=models.CharField(max_length=255)
    contact_phone=models.CharField(max_length=255,validators=[validate_phone],default='')
    contact_email=models.EmailField(default='')
    created_date = models.DateTimeField('date created', default=timezone.now)
    status=models.CharField(max_length=255,default="upcoming",choices=(
    ("upcoming", "upcoming"),
    ("ongoing", "ongoing"),
    ("canceled", "canceled"),
    ("postponed", "postponed"),
    ("finished", "finished")
))
    
    def __str__(self):
        return self.title
    

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
    volunteer=models.ForeignKey(User,on_delete=models.CASCADE)
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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    events_volunteers=models.ForeignKey(EventsVolunteers,on_delete=models.CASCADE)
    date=models.DateField()
    attended=models.BooleanField()
    daily_total_hours=models.FloatField(default=0)

class EventCertificate(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title=models.CharField(max_length=255)
    description=models.TextField() 
    event=models.ForeignKey(Event,on_delete=models.CASCADE,null=True)
    

class EventsVolunteersCertification(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    events_volunteers=models.ForeignKey(EventsVolunteers,on_delete=models.CASCADE)
    event_certeficate=models.ForeignKey(EventCertificate,on_delete=models.CASCADE)
    issue_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('events_volunteers', 'event_certeficate')
            

class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title=models.CharField(max_length=255)
    description=models.TextField()
    organization=models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True)
    starting_date=models.DateField()
    ending_date=models.DateField()
    campaign_manager=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    

class CampaignVolunteer(models.Model):
    campaign=models.ForeignKey(Campaign,on_delete=models.SET_NULL,null=True)
    volunteer=models.ForeignKey(User,on_delete=models.CASCADE)
    registery_date=models.DateTimeField(auto_now_add=True)

class Donation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    donor_name=models.CharField(max_length=255,default='')
    amount=models.FloatField()
    campaign=models.ForeignKey(Campaign,on_delete=models.SET_NULL,null=True)
    donation_date=models.DateField(auto_now_add=True)

