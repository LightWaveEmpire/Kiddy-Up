from __future__ import print_function
from datetime import datetime
from pytz import timezone
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


'''
function: login_calendar()
        This function goes through google's login process.
    If it is the user's first time logging in, the user
    will be brought to sign into their account. Otherwise,
    credentials will be loaded from last log in. This function
    returns a calendar service.

    @return service
'''
    def login_calendar():
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
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

        for event in events
            string = #event.summary, description, start, end
            listOfEvents.append(string)

        return listOfEvents
