# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Parent(models.Model):
    pid = models.AutoField(db_column='PID', primary_key=True)
    password = models.CharField(db_column='PASSWORD', max_length=8)
    name = models.CharField(db_column='NAME', max_length=8)
    # reevaluate field type on info re: acct storage
    accounts = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'parent'


class Child(models.Model):
    pid = models.ForeignKey('Parent', on_delete=models.CASCADE)
    cname = models.CharField(max_length=10)
    # null=True for debug ONLY! Must be fixed for production!
    comp_level = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=8, blank=True, null=True)
    age = models.IntegerField()
    # get details on image storage from Samuel
    avatar = models.CharField(max_length=11)
    current_points = models.IntegerField(default=0)
    target_reward = models.ForeignKey('Reward', on_delete=models.PROTECT)
    # there's not a reason this is JSON; something else is likely better.
    owned_rewards = models.JSONField(blank=True, null=True)
    # Example list field that will hold the earned and not yet received rewards for each child
    # e.g. pizza night, movie night, skating... may be list of RIDs (1,4,3,2,2,3,4)
    #
    # owned_rewards = ListCharField(
    #         base_field=CharField(max_length=10),
    #     size=6,
    #     max_length=(6 * 11)  # 6 * 10 character nominals, plus commas

    class Meta:
        db_table = 'child'
        constraints = [
            # ensures a parent can't have multiple children with same name
            models.UniqueConstraint(fields=['pid', 'cname'], name='unique_sibling'),
            # ensures age of child is between 5-12, inclusive
            models.CheckConstraint(check=models.Q(age__range=(5, 12)), name='age_5_12')
        ]


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

    tid = models.IntegerField(primary_key=True)
    tname = models.CharField(max_length=12)
    tdesc = models.TextField()
    # const: "one or more" of "Child whose PID == Parent.pid"
    visible_to = models.CharField(max_length=8)
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    owner = models.ForeignKey('Child', on_delete=models.CASCADE)
    # get details on image storage from Samuel
    timage = models.CharField(max_length=12)
    # this setup doesn't really allow for recurring events-- alter? dupe?
    date = models.DateField()
    point_value = models.IntegerField(default=0)

    class Meta:
        db_table = 'task'


class Reward(models.Model):
    pid = models.IntegerField()
    rid = models.IntegerField(primary_key=True)
    rname = models.CharField(max_length=8)
    cost = models.IntegerField()
    rimage = models.CharField(max_length=8)
    # should we allow Null for this..?
    visible_to = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'reward'
