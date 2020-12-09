from django.db import models
from django.contrib.auth.models import User #, AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.urls import reverse
from parent.utils import entity_extraction, image_mapping

from collections import defaultdict

import os
import sys
from array import *
import fnmatch

import json


# This list will be read into the parent.entities json structure for RACT on first call

# User = settings.AUTH_USER_MODEL

# class User(AbstractUser):
#     is_parent = models.BooleanField(default=False)
#     is_child = models.BooleanField(default=False)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    active_child = models.ForeignKey('Child', on_delete=models.SET_NULL, blank=True, null=True, related_name='logged_in_child')
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
        default=23505
    )
    # reevaluate field type on info re: acct storage
    # still need to work on things, not sure how this will work out
    # Will likely need changes when we get to it
    account_creds = models.JSONField(blank=True, null=True)
    entities = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'parent'

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.entities = {
                "CHILD": [],
                "SCHOOL": [],
                "WORK": [],
                "RACT": []
            }
        super(Parent, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

    def get_absolute_url(self):
        return reverse('parent', kwargs={'pk': self.pk})

    def update_entities(self, children, locations, tasks):
        default_entities = {
            "CHILD": [],
            "SCHOOL": [],
            "WORK": [],
            "RACT": []
        }
        temp_entities = {
            "CHILD": [],
            "SCHOOL": [],
            "WORK": [],
            "RACT": []
        }
        if self.entities is None:
            self.entities = json.dumps(default_entities)
        else:

            entities_from_parent = json.loads(self.entities)
            print(f'\n\nDEBUG: {entities_from_parent}\n\n', file=sys.stderr)

            for key, value_as_list in entities_from_parent.items():
                for item in value_as_list:
                    temp_entities[key].append(item)

        for child in children:
            temp_entities['CHILD'].append(child.name)

        temp_entities['CHILD'] = list(set(temp_entities['CHILD']))

        # build list of schools, offices,
        # and other locations

        for location in locations:
            if location.location_type == "School":
                temp_entities['SCHOOL'].append(location.name)
            if location.location_type == "Work":
                temp_entities['WORK'].append(location.name)
        temp_entities['SCHOOL'] = list(set(temp_entities['SCHOOL']))

        # build list of task names
#
#        for task in tasks:
#            temp_entities['RACT'].append(task.name)

        temp_entities['RACT'] = list(set(temp_entities['RACT']))

        self.entities = json.dumps(temp_entities)
        self.save()

        print(f'\n\nDEBUG: {self.entities}\n\n', file=sys.stderr)
        return self.entities


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


class Location(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField("Location Name", max_length=50)

    SCHOOL = "School"
    WORK = "Work"
    CHURCH = "Church"
    SPORT = "Sport"
    OTHER = "Other"

    LOCATION_CHOICES = [
        (SCHOOL, "School"),
        (WORK, "Work"),
        (CHURCH, "Church"),
        (SPORT, "Sport"),
        (OTHER, "Other")
    ]

    location_type = models.CharField(
        "Type",
        max_length=6,
        choices=LOCATION_CHOICES,
        default=OTHER
    )

    address = models.CharField("Location Address", max_length=75)

    class Meta:
        db_table = 'location'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('location', kwargs={'pk': self.pk})


class Child(models.Model):
    ONE = 1
    TWO = 2
    COMP_CHOICES = [
        (ONE, "Younger Child"),
        (TWO, "Older Child")
    ]


    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='child')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField("Child Name", max_length=20)
    is_authenticated = models.BooleanField(default=False)
    target_reward = models.ForeignKey('Reward', on_delete=models.SET_NULL, blank=True, null=True)
    age = models.IntegerField("Age")
    comp_level = models.IntegerField(
        "Comprehension Level",
        choices=COMP_CHOICES,
        default=ONE
    )
    owned_rewards = models.JSONField(blank=True, null=True)
    avatar = models.ImageField("Avatar", upload_to='avatars', default='default.jpg')
    current_points = models.IntegerField("Point Balance", default=0)
    pin = models.CharField(max_length=6, default='123')

    class Meta:
        db_table = 'child'
        verbose_name_plural = 'children'

        constraints = [
            # ensures a parent can't have multiple children with same name
            models.UniqueConstraint(fields=['parent', 'name'], name='unique_sibling')#,

            # ensures age of child is between 5-12, inclusive
            #models.CheckConstraint(check=models.Q(age__range=(5, 12)), name='age_5_12')
        ]

    def authenticate(self, pin):
        # We'll need to do logic to test if pin is correct and then authenticate
        if pin == self.pin:
            self.is_authenticated = True
        return self.is_authenticated

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('child', kwargs={'pk': self.pk})


# We will still need location added to Task model

class Task(models.Model):
    OPEN = "OPEN"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    STATUS_CHOICES = [
        (None, "NA"),
        (OPEN, "Open"),
        (PENDING, "Pending"),
        (COMPLETE, "Complete")
    ]

    original_task = models.ForeignKey('Original_Task', on_delete=models.SET_NULL, null=True, default=None)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    name = models.CharField("Task Name", max_length=20)
    description = models.TextField("Task Description", )
    status = models.CharField(
        "Status",
        max_length=8,
        choices=STATUS_CHOICES,
        default=OPEN
    )

    # get details on image storage from Samuel
    image = models.TextField("Task Image", default='task_images/default_task_image.jpg')

    # Will need to change to DateTimeField
    date = models.DateTimeField("Task Date", )
    point_value = models.IntegerField("Point Value", default=1)
    location = models.CharField("Location", max_length=40)

    class Meta:
        db_table = 'task'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})

    def get_task_image(self):
        task_name = self.name
        curr_user = self.child
        comp_level = str(curr_user.comp_level)
        newlist = []
        file_name = []
        file_list = {}

        # on my machine this line made the child task images work right
        print("loading child-friendly images...", file=sys.stderr)

        newlist = (task_name.lower().split())

        for root, dirs, files in os.walk(r'static/task_images/'):
            for file in files:
                if file.startswith(comp_level):
                    file_name = (file.split('_'))
                    res = len(set(newlist) & set(file_name))
                    file_list[f"{file}"] = res

        res_file = max(file_list, key=file_list.get)

        return "task_images/" + str(res_file)


class Original_Task(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    otask = models.TextField("Event / Task", blank=True, null=True)
    raw_otask = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'original_task'

    def __str__(self):
        """String for representing the Model object."""
        return self.otask

    def get_absolute_url(self):
        return reverse('original_task', kwargs={'pk': self.pk})

    def has_created_task(self):
        return Task.objects.filter(original_task=self).exists()

    def turn_into_child_task(self):
        # May need to call with self.raw_otask

        # prevents duplicate imports
        if not self.has_created_task():
        # if True:
            task_details = entity_extraction.extract_entities(self.otask, self.parent.entities)
            # print(f'\n\nDEBUG Task Creation: {task_details}\n\n', file=sys.stderr)
            for kid_name in task_details['people']:
                parent = self.parent
                try:
                    k = Child.objects.get(parent=parent, name=kid_name)
                    if k is not None:   #if the parent's kid exists
                        #task_image, status is assigned to default
                        # print(f'\n\nDEBUG: {k} - If Block', file=sys.stderr)
                        t = Task(
                            original_task=self,
                            parent=self.parent,
                            child=k,
                            name=task_details['name'],
                            description=task_details['description'],
                            date=task_details['date'],
                            location=task_details['location'],
                            image=''
                        )
                        t.image = image_mapping.get_task_image(t)
                        t.save()

                except Exception as e:
                    print(f'\n\nDEBUG: Task not created. \n\nError: {e}', file=sys.stderr)


class Earned_Reward(models.Model):
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    class Meta:
        db_table = 'earned_reward'

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.child} earned {self.reward}"

    def get_absolute_url(self):
        return reverse('earned_reward', kwargs={'pk': self.pk})
