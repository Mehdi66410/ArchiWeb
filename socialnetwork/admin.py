from django.contrib import admin
#test
# Register your models here.

from .models import Friend
from .models import PictureUser
from .models import Bar
from .models import Restaurant,Discotheque,starRestaurant,starDiscotheque,presentRestau,presentDisco
from .models import presentBar
from .models import InformationUser
from .models import SearchInformationUser
from .models import starBar
from .models import Chat



admin.site.register(Friend)
admin.site.register(PictureUser)
admin.site.register(Bar)
admin.site.register(Restaurant)
admin.site.register(presentBar)
admin.site.register(InformationUser)
admin.site.register(SearchInformationUser)
admin.site.register(starBar)
admin.site.register(Chat)
admin.site.register(Discotheque)
admin.site.register(starDiscotheque)
admin.site.register(starRestaurant)
admin.site.register(presentDisco)
admin.site.register(presentRestau)
