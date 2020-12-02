from django.db import models
from django.contrib.auth.models import User #, AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.urls import reverse
from parent.utils import entity_extraction, image_mapping


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
    )
    # reevaluate field type on info re: acct storage
    # still need to work on things, not sure how this will work out
    # Will likely need changes when we get to it
    account_creds = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'parent'

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

    def get_absolute_url(self):
        return reverse('parent', kwargs={'pk': self.pk})


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
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='child')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name ='parent')
    name = models.CharField("Child Name", max_length=20)
    is_authenticated = models.BooleanField(default=False)
    target_reward = models.ForeignKey('Reward', on_delete=models.SET_NULL, blank=True, null=True)
    age = models.IntegerField("Age")
    comp_level = models.IntegerField("Comprehension Level", blank=True, null=True)
    owned_rewards = models.JSONField(blank=True, null=True)
    avatar = models.ImageField("Avatar", upload_to = 'avatars', default='default.jpg')
    current_points = models.IntegerField("Point Balance", default=0)
    pin = models.CharField(max_length=6, default='123')

    class Meta:
        db_table = 'child'
        verbose_name_plural = 'children'

        constraints = [
            # ensures a parent can't have multiple children with same name
            models.UniqueConstraint(fields=['parent', 'name'], name='unique_sibling'),

            # ensures age of child is between 5-12, inclusive
            models.CheckConstraint(check=models.Q(age__range=(5, 12)), name='age_5_12')
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
    PENDING = "PEND"
    COMPLETE = "COMP"
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
    status = models.CharField("Status",
        max_length=8,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    # get details on image storage from Samuel
    image = models.CharField("Task Image", max_length=20, default='default_img')
    # image = image_mapping.get_task_image(description)

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
        task_details = entity_extraction.extract_entities(self.otask)
        for kid_name in task_details['people']:
            k = table_access.get_child(self.parent, kid_name)
            if k is not None:   #if the parent's kid exists
                #task_image, status is assigned to default
                t = Task(
                         original_task=self,
                         parent=self.parent,
                         child=k,
                         name=task_details['name'],
                         description=task_details['description'],
                         date=task_details['date'],
                         location=task_details['location'])
                t.save()



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

