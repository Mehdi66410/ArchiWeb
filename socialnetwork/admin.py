from django.contrib import admin

# Register your models here.
from .models import Affinite, Bar, Chat, Discotheque, InformationUser, PictureUser, presentBar, presentDisco, presentRestau, Restaurant, SearchInformationUser, starBar, starDiscotheque, starRestaurant

admin.site.register(Affinite)
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
