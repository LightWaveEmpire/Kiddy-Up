from __future__ import print_function
from datetime import datetime
from pytz import timezone
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


current_path = os.path.dirname(__file__)
credential_path = os.path.join(current_path, 'credentials.json')




# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/tasks.readonly']


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
    creds = None
    try:
        token_path = os.path.join(current_path, user_tokens, f'{user.username}.pickle')
        raise Exception('TEST 1')
    except Exception as e:
        print('Caught error: ' + repr(e))


    if os.path.exists('token.pickle'):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

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
    now = datetime.now(tz).isoformat()
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    listOfEvents = []

    for event in events:
        string = "testing" #event.summary, description, start, end
        listOfEvents.append(string)

    return listOfEvents
