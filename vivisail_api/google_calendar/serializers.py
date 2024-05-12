
from rest_framework import serializers

from .models import DateRangeRequestModel, GoogleCalendarEventModel

class DateRangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateRangeRequestModel
        fields = ['username', 'startDate', 'endDate']

class GoogleCalendarEventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GoogleCalendarEventModel
        fields = ['id', 'title', 'startDateTime', 'endDateTime']