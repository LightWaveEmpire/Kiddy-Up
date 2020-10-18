# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Parent(models.Model):
## This information will be stored in the django user management system that is built-in
## may need to use this to have multiple parents for same account?
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#    password = models.CharField(db_column='PASSWORD', max_length=20)
    name = models.CharField(db_column='NAME', max_length=20, default="")

# reevaluate field type on info re: acct storage
    accounts = models.JSONField(blank=True, null=True)
#    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'parent'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('parent', kwargs={'pk': self.pk})




class Child(models.Model):
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE)
    cname = models.CharField(max_length=20)
    # null=True for debug ONLY! Must be fixed for production!
    comp_level = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField()
    # get details on image storage from Samuel
    avatar = models.CharField(max_length=20)
    current_points = models.IntegerField(default=0)
    target_reward = models.ForeignKey('Reward', on_delete=models.PROTECT)
    # there's not a reason this is JSON; something else is likely better.
    owned_rewards = models.JSONField(blank=True, null=True)
    # Example list field that will hold the earned and not yet received rewards for each child
    # e.g. pizza night, movie night, skating... may be list of RIDs (1,4,3,2,2,3,4)
    #
#    owned_rewards = ListCharField(
#        base_field=CharField(max_length=10),
#        size=6,
#        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

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

#    tid = models.IntegerField(primary_key=True)
    tname = models.CharField(max_length=20)
    tdesc = models.TextField()
    # const: "one or more" of "Child whose PID == Parent.pid"
    visible_to = models.CharField(max_length=20)
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    owner = models.ForeignKey('Child', on_delete=models.CASCADE)
    # get details on image storage from Samuel
    timage = models.CharField(max_length=20, default='default_img')
    # this setup doesn't really allow for recurring events-- alter? dupe?
    date = models.DateField()
    point_value = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'

    def __str__(self):
        """String for representing the Model object."""
        return self.tname

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})


class Reward(models.Model):
    rname = models.CharField(max_length=20)
    cost = models.IntegerField()
    rimage = models.CharField(max_length=20, null=True)
    # should we allow Null for this..?
    visible_to = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reward'

    def __str__(self):
        """String for representing the Model object."""
        return self.rname

    def get_absolute_url(self):
        return reverse('reward', kwargs={'pk': self.pk})
