from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def is_active(self):
        return self.start <= timezone.now() < self.end

    def __str__(self):
        return self.name

class ExtensionType(models.TextChoices):
    SIP = 'sip'
    DECT = 'dect'
    CALLGROUP = 'callgroup'

class Extension(models.Model):
    event = models.ForeignKey(Event, related_name='extensions', on_delete=models.CASCADE)
    number = models.IntegerField()
    password = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    extension_type = models.CharField(
        max_length=255,
        choices=ExtensionType.choices,
        default=ExtensionType.SIP
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.number} - {self.name}"

class CallgroupMembership(models.Model):
    extension = models.ForeignKey(Extension, related_name='callgroups', on_delete=models.CASCADE)
    callgroup = models.ForeignKey(Extension, related_name='members', limit_choices_to={'extension_type': ExtensionType.CALLGROUP}, on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)

    def is_active(self):
        return not self.paused and self.accepted
