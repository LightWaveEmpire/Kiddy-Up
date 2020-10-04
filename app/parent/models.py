from django.db import models

# Create your models here.


class Child(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    grade = models.IntegerField()
# ...

class Task(models.Model):
    STATUS =(
            ('Pending', 'Pending'),
            ('Inprogress', 'Inprogress'),
            ('Completed', 'Completed'),
            ('Missed', 'Missed'),
    )
    task_name = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS)
# ...

class Event (models.Model):
    event_name = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    date = models.DateField()
# ...


class Reward(models.Model):
    name = models.CharField(max_length=30)
    point_value = models.IntegerField()
# ...
