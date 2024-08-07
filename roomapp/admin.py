from django.contrib import admin
from .models import City, User, Room, RoommateProfile, Accessory, Attachment
# Register your models here.
admin.site.register(City)
admin.site.register(Room)
admin.site.register(RoommateProfile)
admin.site.register(User)
admin.site.register(Accessory)
admin.site.register(Attachment)
