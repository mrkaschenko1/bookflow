from django.db import models
from django.contrib.auth.models import User
from book.models import Shelf, BookInfo
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to = 'avatars/', null=True, blank=True)
    # avatar = AvatarField(upload_to='profile_images', width=100, height=100)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        user = instance
        if created:
            profile = Profile(user=user)
            profile.save()
            Shelf.objects.create(name="To read", profile=profile, is_custom=False)
            Shelf.objects.create(name="In progress", profile=profile, is_custom=False)
            Shelf.objects.create(name="Have read", profile=profile, is_custom=False)

    except Profile.DoesNotExist:
        print('foo')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        print('foo')

# post_save.connect(create_user_profile, sender='User')