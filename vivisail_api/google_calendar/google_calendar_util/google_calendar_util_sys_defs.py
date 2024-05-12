
import os

# TODO: this should be in the request
CURRENT_USER = "vivi-mahtab"

#   "google api event key": "desired json key"
GOOGLE_API_EVENT_KEY_JSON_FORMATTER = {
    "id": "id",
    "summary": "title",
#   "start": "startDateTime",
#   "end": "endDateTime",
    
} # (NOTE: startDate and endDate not included, needs additional parsing)

DATETIME_REGEX_PATTERN = "(\\d+)-(\\d+)-(\\d+)T(\\d+):(\\d+):.*"

GOOGLE_CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]  # the scope of GCal access

# TODO: make this safe
LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)) # ~/google_calendar/google_calendar_util/
PATH_TO_API_CREDS = f"{LOCAL_PATH}/_PROTECTED/_API_CREDENTIALS/GOOGLE_CALENDAR_CREDS.json"
PATH_TO_USER_CREDS = f"{LOCAL_PATH}/_PROTECTED/_USERS/{CURRENT_USER.lower()}"
PATH_TO_USER_TOKEN = f"{PATH_TO_USER_CREDS}/google_calendar_token.json"