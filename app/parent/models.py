from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse
from __future__ import print_function
from datetime import datetime
from pytz import timezone
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class User(AbstractUser):
    is_parent = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='parent')
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )
    # reevaluate field type on info re: acct storage
    # still need to work on things, not sure how this will work out
    # Will likely need changes when we get to it
    accounts = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'parent'

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

    def get_absolute_url(self):
        return reverse('parent', kwargs={'pk': self.pk})


'''
function: login_and_getCalendarService()
        This function goes through google's login process.
    If it is the user's first time logging in, the user
    will be brought to sign into their account. Otherwise,
    credentials will be loaded from last log in. This function
    returns a calendar service.

    @return service
'''
    def login_and_getCalendarService():
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
function: getListOfEvents()
        This function accesses the specified amount of calendar events
    and puts them into a list of strings to be stored into DB.

    @parameter service - calendar service object
    @paremeter n - desired amount of events
    @return listOfEvents - array of strings
'''
    def getListOfEvents(service, n):
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

class Reward(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    visible_to = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField("Reward Name", max_length=20)
    cost = models.IntegerField("Cost", )
    image = models.CharField("Reward Image", max_length=20, null=True)

    class Meta:
        db_table = 'reward'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('reward', kwargs={'pk': self.pk})



class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='child')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField("Child Name", max_length=20)
    target_reward = models.ForeignKey('Reward', on_delete=models.PROTECT, blank=True, null=True)
    age = models.IntegerField("Age")
    comp_level = models.IntegerField("Comprehension Level", blank=True, null=True)
    owned_rewards = models.JSONField(blank=True, null=True)
    avatar = models.ImageField("Avatar", max_length=20)
    current_points = models.IntegerField("Point Balance", default=0)
    class Meta:
        db_table = 'child'

        constraints = [
            # ensures a parent can't have multiple children with same name
            models.UniqueConstraint(fields=['parent', 'user'], name='unique_sibling'),

            # ensures age of child is between 5-12, inclusive
            models.CheckConstraint(check=models.Q(age__range=(5, 12)), name='age_5_12')
        ]

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('child', kwargs={'pk': self.pk})





# We will still need location added to Task model

class Task(models.Model):
    OPEN = "OPEN"
    PENDING = "PEND"
    COMPLETE = "COMP"
    STATUS_CHOICES = [
        (None, "NA"),
        (OPEN, "Open"),
        (PENDING, "Pending"),
        (COMPLETE, "Complete")
    ]

    original_task = models.ForeignKey('Original_Task', on_delete=models.CASCADE, null=True, default=None)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='creator')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='actioner')

    name = models.CharField("Task Name", max_length=20)
    description = models.TextField("Task Description", )
    status = models.CharField("Status",
        max_length=8,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    # get details on image storage from Samuel
    image = models.CharField("Task Image", max_length=20, default='default_img')

    # Will need to change to DateTimeField
    date = models.DateTimeField("Task Date", )
    point_value = models.IntegerField("Point Value", default=0)
    location = models.CharField("Location", max_length=40)

    class Meta:
        db_table = 'task'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})

class Original_Task(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    otask = models.CharField("Event / Task", max_length=500)

    class Meta:
        db_table = 'original_task'

    def __str__(self):
        """String for representing the Model object."""
        return self.otask

    def get_absolute_url(self):
        return reverse('original_task', kwargs={'pk': self.pk})

'''
function: putListIntoOriginalTasks()
    This function puts a list of strings into Original_Task table.

    @parameter listOfStrings
'''
    def putListIntoOriginalTasks(listOfStrings):
        #for each item in listOfStrings
            #t = Original_Task(user="current_user", task=item)
            #t.save()

'''
    This function takes checks which Original_Tasks need to be processed
then processes them. Stores the processed tasks into Task table.
'''
    def processOriginalTasks():
        #for each item in Original_Tasks table
            #if it has not been processed
                #process the task with spacy
                #HIGH- use that info to fill in appropriate task fields
                #save that into task table






