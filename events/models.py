from django.db import models
from users.models import Organization,User
# Create your models here.


class Location(models.Model):
    city=models.CharField(max_length=255)
    sub_city=models.CharField(max_length=255)
    

class Event(models.Model):
    title=models.CharField(max_length=255,blank=False,null=False)
    description=models.TextField()
    organization=models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True)
    starting_date=models.DateField()
    ending_date=models.DateField()
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=255)
    status=models.CharField(max_length=255,choices=(
    ("upcoming", "upcoming"),
    ("ongoing", "ongoing"),
    ("canceled", "canceled"),
    ("postponed", "postponed"),
    ("finished", "finished")
))
    
    

class EventOrganizers(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    organizer=models.ForeignKey(User,on_delete=models.CASCADE)



class EventsImage(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    image=models.ImageField()



class EventsSchedule(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    date=models.DateField()
    session_name=models.CharField(max_length=255)
    starting_time=models.TimeField()
    ending_time=models.TimeField()
    venue=models.CharField(max_length=255,blank=True,default='')



class EventsVolunteeringCategory(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    category_name=models.CharField(max_length=255)



class EventsVolunteers(models.Model):
    events=models.ForeignKey(Event,on_delete=models.CASCADE)
    volunteers=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    events_volunteering_category=models.ForeignKey(EventsVolunteeringCategory,on_delete=models.SET_NULL,null=True)
    status=models.CharField(max_length=255,choices=(
    ("active", "active"),
    ("unregistered", "unregistered")
))
    Registery_date=models.DateTimeField(auto_now_add=True)
    # add reward feature


# class EventsVolunteersHours(models.Model):
#     events_volunteers=models.ForeignKey(EventsVolunteers,on_delete=models.CASCADE)
#     date=models.DateField()
#     daily_total_hours=models.FloatField()

