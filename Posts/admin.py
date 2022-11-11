from django.contrib import admin
from .models import Profile, FriendRequest, Event, Location
# from django.contrib.gis.admin import OSMGeoAdmin


admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Event)
admin.site.register(Location)
# class EventLocation(OSMGeoAdmin):
#     list_display = ('name', 'location')


# Register your models here.
