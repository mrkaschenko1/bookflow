from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from book.models import Shelf, BookInfo
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # avatar = models.ImageField(upload_to = 'avatars/', null=True, blank=True)


class Avatar(models.Model):
    image = models.ImageField(upload_to='avatars', default='default/default_avatar.png')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(40, 40)],
                                     format='PNG',
                                     options={'quality': 60})
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='avatar')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.image.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        user = instance
        if created:
            profile = Profile(user=user)
            avatar = Avatar(image='default/default_avatar.png', profile=profile)
            # profile.avatar.image.set_image_to_default()
            profile.save()
            avatar.save()
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