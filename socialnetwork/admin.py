from django.contrib import admin
#test
# Register your models here.

from .models import Friend
from .models import PictureUser
from .models import Bar
from .models import Restaurant

admin.site.register(Friend)
admin.site.register(PictureUser)
admin.site.register(Bar)
admin.site.register(Restaurant)