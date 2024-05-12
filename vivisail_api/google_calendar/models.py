from django.db import models

class DateRangeRequestModel(models.Model):
    username  = models.TextField()
    startDate = models.DateTimeField()
    endDate   = models.DateTimeField()
    
class GoogleCalendarEventModel(models.Model):
    id            = models.TextField(primary_key=True)
    title         = models.TextField()
    startDateTime = models.DateTimeField()
    endDateTime   = models.DateTimeField()
