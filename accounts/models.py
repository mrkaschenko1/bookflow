from PIL import Image
from django.contrib.auth import logout
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from bookflow.constants import DEFAULT_AVATAR
from book.models import Shelf, BookInfo
from django.db.models.signals import post_save
from django.dispatch import receiver

from middleware.middlewares import RequestMiddleware


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    books = models.ManyToManyField(BookInfo, related_name='profiles')
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, null=True)
    is_moderator = models.BooleanField(default=False)
    # avatar = models.ImageField(upload_to = 'avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Avatar(models.Model):
    image = models.ImageField(upload_to='avatars', default=DEFAULT_AVATAR)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(40, 40)],
                                     format='PNG',
                                     options={'quality': 60})
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='avatar')


    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return DEFAULT_AVATAR

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


class ModRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_requested')
    accepted = models.BooleanField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        user = instance
        if created:
            profile = Profile(user=user)
            # profile.avatar.image.set_image_to_default()
            profile.save()
            avatar = Avatar(image='default/default_avatar.png', profile=profile)
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


@receiver(post_save, sender=ModRequest)
def change_moderator_field(sender, instance, **kwargs):
    try:
        profile = User.objects.get(username=instance.user.username).profile
        if instance.accepted is not None:
            profile.is_moderator = instance.accepted
        else:
            profile.is_moderator = False
        profile.save()
    except Profile.DoesNotExist:
        print('foo')


@receiver(post_save, sender=User)
def logout_user_on_banned(sender, instance, **kwargs):
    try:
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        if not User.is_active:
            logout(request)
    except Exception as e:
        print(e.with_traceback())

# post_save.connect(create_user_profile, sender='User')