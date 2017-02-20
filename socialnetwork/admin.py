from django.contrib import admin
#test
# Register your models here.

from .models import Friend
from .models import PictureUser

admin.site.register(Friend)
admin.site.register(PictureUser)
