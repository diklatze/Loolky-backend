from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['user_id', 'gender', 'country', 'city', 'height']

    user_id = models.AutoField(primary_key=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25, default="Israel")
    height = models.IntegerField()
    shirt_size = models.IntegerField()
    pents_size = models.IntegerField()
    bra_size = models.CharField(max_length=10)
    shoe_size = models.FloatField()
    picture = models.CharField(max_length=50)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
