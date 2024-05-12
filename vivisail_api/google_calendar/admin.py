
from django.contrib import admin
from .models import DateRangeRequestModel, GoogleCalendarEventModel

admin.site.register(DateRangeRequestModel)
admin.site.register(GoogleCalendarEventModel)