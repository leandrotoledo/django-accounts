import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from locations.models import Place, Municipality, Country

ACCOUNT_ACTIVATION_DAYS = 7

class ProfileManager(models.Manager):
    def activate_profile(self, activation_key):
        try:
            profile = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False

        if not profile.is_active:
            profile.is_active = True
            profile.save()

        return profile

    def create_profile(self, user):
        profile = Profile.objects.create(user=user)
        profile.activation_key = uuid.uuid4().hex
        profile.save()

        return profile

    def delete_inactive_profiles(self):
        for profile in self.filter(is_active=False):
            if profile.activation_key_expired:
                user = profile.user
                user.is_active = False
                user.save()

                profile.delete()

class Profile(models.Model):
    GENDER_CHOICES = (
        (u'F', _(u'Female')),
        (u'M', _(u'Male')),
    )
    user = models.OneToOneField(User, unique=True)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(
        _(u'Activation Key'), 
        max_length=32, 
        blank=True
    )
    gender = models.CharField(
        _(u'Gender'), 
        max_length=1, 
        choices=(GENDER_CHOICES), 
        blank=True
    )
    birth_date = models.DateField(_('Birthday'), blank=True, null=True)
    home_phone = models.CharField(max_length=10, blank=True)
    work_phone = models.CharField(max_length=10, blank=True)
    cell_phone = models.CharField(max_length=10, blank=True)
    nationality = models.ForeignKey(Country, blank=True, null=True)
    citizenship = models.ForeignKey(Municipality, blank=True, null=True)
    address = models.ForeignKey(Place)
    objects = ProfileManager()

    def __unicode__(self):
        return '{}: {} {}'.format(
            self.user.username, 
            self.user.first_name, 
            self.user.last_name
        )
    
    @property
    def email(self):
        return self.user.email
            
    @property
    def activation_key_expired(self):
        expiration_date = now().date() - self.user.date_joined.date()
        return self.is_active or (expiration_date.days >= ACCOUNT_ACTIVATION_DAYS)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create_profile(instance)
post_save.connect(create_user_profile, sender=User)
