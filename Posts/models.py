from autoslug import AutoSlugField
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from location_field.models.plain import PlainLocationField
# from django.contrib.gis.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user',default= 'user')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    friends = models.ManyToManyField("Profile",related_name="prieteni",symmetrical=False,blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return f' {self.slug}'


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # if created: Maybe this way???
        #     user_profile = Profile(user=instance)
        #     user_profile.save()
        #     user_profile.friends.set([instance.profile.id])  # when logged in, the user has to follow himself also
        #     user_profile.save()
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=User)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.from_user.username} {self.to_user.username} '







class Location(models.Model):
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    def __str(self):
        return f' {self.city}'


class Event(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    nume = models.CharField(max_length=255)
    varsta = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now=True)
    location = PlainLocationField(based_fields=['city'], zoom=7, blank=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

# class EventLocation(models.Model):
#     event_location= models.ForeignKey(Location, on_delete=models.CASCADE)

