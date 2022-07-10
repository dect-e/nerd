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

class DectHandset(models.Model):
    ipei = models.CharField(max_length=32)
    name = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} - {self.ipei}"

class ExtensionType(models.TextChoices):
    SIP = 'sip'
    DECT = 'dect'
    CALLGROUP = 'callgroup'
    STATIC = 'static'
    TEMP = 'temp'

class Extension(models.Model):
    event = models.ForeignKey(Event, related_name='extensions', on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    extension_type = models.CharField(
        max_length=255,
        choices=ExtensionType.choices,
        default=ExtensionType.SIP
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    public = models.BooleanField(default=True)
    dialout_allowed = models.BooleanField(default=True)
    trunk = models.BooleanField(default=False)
    outgoing_extension = models.CharField(max_length=15, blank=True)
    static_target = models.CharField(max_length=255, blank=True)
    dect_handset = models.ForeignKey(DectHandset, related_name='extensions', on_delete=models.CASCADE, blank=True, null=True)
    dect_claim_token = models.CharField(max_length=15, blank=True)
    sip_password = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f"{self.number} - {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'number'], name='unique_extension'),
            models.UniqueConstraint(fields=['event', 'dect_handset'], name='unique_handset')
        ]

class CallgroupMembership(models.Model):
    extension = models.ForeignKey(Extension, related_name='callgroups', on_delete=models.CASCADE)
    callgroup = models.ForeignKey(Extension, related_name='members', limit_choices_to={'extension_type': ExtensionType.CALLGROUP}, on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)

    def is_active(self):
        return not self.paused and self.accepted

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['extension', 'callgroup'], name='unique_callgroup_membership')
        ]
