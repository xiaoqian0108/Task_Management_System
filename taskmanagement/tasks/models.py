from django.db import models

# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True) #this is the primary key to identify the event
    name = models.CharField(max_length=100) #this is the name of the event
    label = models.CharField(max_length=100) #this is the label of the event, it is used to categorize the event
    date = models.DateField() #this is the date of the event
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
