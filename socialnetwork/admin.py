from django.contrib import admin
#test
# Register your models here.

from .models import Friend
from .models import PictureUser
from .models import Bar
from .models import Restaurant
from .models import jaimeBar
from .models import presentBar

admin.site.register(Friend)
admin.site.register(PictureUser)
admin.site.register(Bar)
admin.site.register(Restaurant)
admin.site.register(jaimeBar)
admin.site.register(presentBar)