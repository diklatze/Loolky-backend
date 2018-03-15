from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    ########################## TODO: change USERNAME_FIELD to id ##########################
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gender', 'country', 'city', 'height']

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=25, default='Tel Aviv')
    country = models.CharField(max_length=25, default="Israel")
    height = models.PositiveSmallIntegerField(default=0)
    shirt_size = models.PositiveSmallIntegerField(default=0)
    pents_size = models.PositiveSmallIntegerField(default=0)
    bra_size = models.CharField(max_length=10, default='0')
    shoe_size = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    picture = models.CharField(max_length=50)

    is_valid_account = models.BooleanField(default=False)
    temporary_password = models.CharField(max_length=128, null=True)
    temporary_password_date = models.DateTimeField(null=True, blank=True)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
