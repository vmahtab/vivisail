from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import DateRangeRequestSerializer

from google_calendar.google_calendar_util.google_calender_util import get_user_google_calendar_events_in_date_range

@api_view(["POST"])
def getGoogleCalendarEventsinDateRange(request):
    
    serializer = DateRangeRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(get_user_google_calendar_events_in_date_range(
        client_request_username = serializer.data["username"],
        start_date              = serializer.data["startDate"],
        end_date                = serializer.data["endDate"]))
    