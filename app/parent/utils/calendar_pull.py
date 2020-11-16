from __future__ import print_function
from datetime import datetime, tzinfo
from pytz import timezone
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
from parent.models import Parent

# current_path = os.path.dirname(__file__)
# credential_path = os.path.join(current_path, 'credentials.json')




# # If modifying these scopes, delete the file token.pickle.
# SCOPES = [
#     'https://www.googleapis.com/auth/calendar.readonly',
#     'https://www.googleapis.com/auth/tasks.readonly']


'''
function: login_calendar()
        This function goes through google's login process.
    If it is the user's first time logging in, the user
    will be brought to sign into their account. Otherwise,
    credentials will be loaded from last log in. This function
    returns a calendar service.

    @return service
'''
def login_calendar(user):
    parent = Parent.objects.get(user = user)
    creds = google_apis_oauth.load_credentials(parent.account_creds)
    return build('calendar', 'v3', credentials=creds)

'''
function: get_list_of_events(service, n)
    This function accesses the specified amount of calendar events
and puts them into a list of strings to be stored into DB.

@parameter service - calendar service object
@paremeter n - desired amount of events
@return listOfEvents - array of strings
'''
def get_list_of_events(service, n):
    now = datetime.now(timezone(settings.TIME_ZONE)).isoformat()
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    listOfEvents = []

    for event in events:
        start_date = event['start']['datetime']
        end_date = event['end']['datetime']
        
        #formatted as "05:00PM on Friday, December 15"
        start_string = start_date.strftime("%I:%M%p on %A, %B %d")
        end_string = end_date.strftime("%I:%M%p on %A, %B %d")

        string = event['summary'] + ". " + event['description'] + ". Starts at " + start_string + ". Ends at " + end_string + "."
        listOfEvents.append(string)

    return listOfEvents
