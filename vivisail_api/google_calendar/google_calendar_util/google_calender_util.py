
import datetime
import json
import typing
import re

from .google_calendar_util_sys_defs import *

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# :param username: the user we are making new credentials for
#
# :modifies creates a new _USER directory for the user and creates a new token for them
#
# :returns the generated user's credentials
#
def initialize_google_calendar_user_credentials(username: str):

    # TODO: this should be on new user not first grab of GCAL credentials
    if not os.path.exists(PATH_TO_USER_CREDS):
        os.makedirs(PATH_TO_USER_CREDS)

    google_flow = InstalledAppFlow.from_client_secrets_file(PATH_TO_API_CREDS, GOOGLE_CALENDAR_SCOPES)
    user_credentials = google_flow.run_local_server()

    # cache the new user's credentials
    with open(PATH_TO_USER_TOKEN, "w") as token:
        token.write(user_credentials.to_json())

    return user_credentials

# :param username: the user we are fetching credentials for
#
# :modifies iff the user does not previously have credentials, creates a new Google API token
#
# :returns the user's credentials
#
def get_google_calendar_user_credentials(username: str): # TODO: make this secure

    try:
        user_credentials = Credentials.from_authorized_user_file(PATH_TO_USER_TOKEN, GOOGLE_CALENDAR_SCOPES)

        if not user_credentials.valid and user_credentials.expired and user_credentials.refresh_token:
            user_credentials.refresh(Request())

        return user_credentials

    # user credentials path does not exist
    except FileNotFoundError:
        return initialize_google_calendar_user_credentials(username)

    # user credentials was None type
    except AttributeError or ValueError:
        return initialize_google_calendar_user_credentials(username)

    # user credentials could not be refreshed, initialize new ones
    except RefreshError:
        return initialize_google_calendar_user_credentials(username)

# :param google_api_event: a single Google Calendar API event
#
# :returns a subset map of google_api_event using keys from GOOGLE_API_EVENT_KEY_JSON_FORMATTER from sys_defs
#
def parse_google_event(google_api_event) -> dict[str: typing.Any]:

    parsed_event = {json_key: google_api_event[event_key] for event_key, json_key in GOOGLE_API_EVENT_KEY_JSON_FORMATTER.items()}
    
    # START DATETIME
    startComponents = re.search(pattern=DATETIME_REGEX_PATTERN, string=google_api_event["start"]["dateTime"]).groups()
    parsed_event["startDateTime"] = {
        "Date": {
            "year"  : int(startComponents[0]),
            "month" : int(startComponents[1]),
            "day"   : int(startComponents[2]),
        },
        "Time": {
            "hour"  : int(startComponents[3]),
            "minute": int(startComponents[4]),
        }
    }
    
    # END DATETIME 
    endComponents = re.search(pattern=DATETIME_REGEX_PATTERN, string=google_api_event["end"]["dateTime"]).groups()
    parsed_event["endDateTime"] = {
        "Date": {
            "year"  : int(endComponents[0]),
            "month" : int(endComponents[1]),
            "day"   : int(endComponents[2]),
        },
        "Time": {
            "hour"  : int(endComponents[3]),
            "minute": int(endComponents[4]),
        }
    }
    
    return parsed_event


#   :param google_api_events: event_results["items"] where event_results is a return from a call
#                             to the Google Calendar API (a list of Google Calendar API Events)
#
#   :returns a json formatted using the google_calendar_utils_sys_defs.GOOGLE_API_EVENT_KEY_JSON_FORMATTER
#
def parse_json_from_google_events(google_api_events) -> json:
    return [parse_google_event(event) for event in google_api_events]


def get_user_google_calendar_events_in_date_range(client_request_username: str, start_date: str, end_date: str) -> json:

    try:
        
        user_credentials = get_google_calendar_user_credentials(username=client_request_username)
        google_calendar_servicer = build("calendar", "v3", credentials=user_credentials)

        events_result = (
            google_calendar_servicer.events().list(
                calendarId="primary",
                singleEvents=True,
                maxResults=9999,
                orderBy="startTime",
                timeMin=start_date,
                timeMax=end_date)
            .execute()
        )
        
        return parse_json_from_google_events(events_result.get("items", []))

    except HttpError as error:
        print(f"An error occurred: {error}")


# def prefilled_handler():

#     april_start = datetime.datetime(2025, 4, 1)
#     april_end = datetime.datetime(2025, 4, 30)
#     return get_user_google_calendar_events_in_date_range(CURRENT_USER, april_start, april_end)
