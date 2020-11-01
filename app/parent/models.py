from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



## Proposed Changes (Original_Task) ##

#! New table for raw tasks
# All naming can be changed
class Original_Task(models.Model):
    # link tasks to the logged in user (the parent)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # This may need to change based on how the google syncing works... I haven't looked into that yet
    otask = models.CharField(max_length=500)

    class Meta:
        db_table = 'original_task'

    def __str__(self):
        """String for representing the Model object."""
        return self.task

    def get_absolute_url(self):
        return reverse('original_task', kwargs={'pk': self.pk})

## End Proposed Changes (Original_Task) ##


class Parent(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(db_column='NAME', max_length=20, default="")

    # reevaluate field type on info re: acct storage
    # still need to work on things, not sure how this will work out
    # Will likely need changes when we get to it
    accounts = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'parent'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('parent', kwargs={'pk': self.pk})


class Child(models.Model):

    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, null=True, default=None)

    #! This user will link to the child logged in user
    #! We still need to figure out how once we build out the child django users (auth.user)
    #! user = ??

    target_reward = models.ForeignKey('Reward', on_delete=models.PROTECT, blank=True, null=True)

    # there's not a reason this is JSON; something else is likely better.
    #! We need to understand how we are going to manage "purchased" rewards
    #! e.g. pizza night, movie night, skating... may be list of RIDs (1,4,3,2,2,3,4)?

    #! Example list field that will hold the earned and not yet received rewards for each child
    #!    owned_rewards = ListCharField(
    #!        base_field=CharField(max_length=10),
    #!        size=6,
    #!        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas

    owned_rewards = models.JSONField(blank=True, null=True)

    cname = models.CharField(max_length=20)

    comp_level = models.IntegerField(blank=True, null=True)

    age = models.IntegerField()

    # get details on image storage from Samuel
    avatar = models.CharField(max_length=20)

    current_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'child'

        constraints = [
            # ensures a parent can't have multiple children with same name
            models.UniqueConstraint(fields=['parent', 'cname'], name='unique_sibling'),

            # ensures age of child is between 5-12, inclusive
            models.CheckConstraint(check=models.Q(age__range=(5, 12)), name='age_5_12')
        ]

    def __str__(self):
        """String for representing the Model object."""
        return self.cname

    def get_absolute_url(self):
        return reverse('child', kwargs={'pk': self.pk})


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

    ## Proposed Changes (Tasks) ##

    #! Link the child's task to the "master" or original task that is synced with google or other external source.
    #! Many tasks can be linked to the single original task (two kids going to same soccer match)
    #! If original is deleted, the child task is deleted
    original_task = models.ForeignKey('Original_Task', on_delete=models.CASCADE, null=True, default=None)

    # const: "one or more" of "Child whose PID == Parent.pid"
    #! I don't think this is needed anymore
    #! Each task will be linked to a child (which is linked to a parent)
    #! Each task will be linked to an original_task which is linked to a parent
    #!visible_to = models.CharField(max_length=20)

    #! Linking each task to a child allows the child to
    child = models.ForeignKey('Child', on_delete=models.CASCADE)

    #! I don't think this is necessary as we are linking tasks to the parent in other ways (original_task.parent and child.parent)
    #!created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    ## End Proposed Changes (Tasks) ##

    tname = models.CharField(max_length=20)
    tdesc = models.TextField()
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    # get details on image storage from Samuel
    timage = models.CharField(max_length=20, default='default_img')
    # this setup doesn't really allow for recurring events-- alter? dupe?
    date = models.DateField()
    point_value = models.IntegerField(default=0)

    class Meta:
        db_table = 'task'

    def __str__(self):
        """String for representing the Model object."""
        return self.tname

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})


class Reward(models.Model):

    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, null=True, default=None)

    # review field type-- may need foreign key?
    # const: "one or more" of "Child whose PID == Parent.pid"
    visible_to = models.CharField(max_length=20, blank=True, null=True)

    rname = models.CharField(max_length=20)
    cost = models.IntegerField()
    rimage = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'reward'

    def __str__(self):
        """String for representing the Model object."""
        return self.rname

    def get_absolute_url(self):
        return reverse('reward', kwargs={'pk': self.pk})
