from django.contrib import admin
#test
# Register your models here.

from .models import Friend
from .models import PictureUser
from .models import Bar
from .models import Restaurant
from .models import LikeBar
from .models import DislikeBar
from .models import presentBar
from .models import InformationUser
from .models import SearchInformationUser


admin.site.register(Friend)
admin.site.register(PictureUser)
admin.site.register(Bar)
admin.site.register(Restaurant)
admin.site.register(LikeBar)
admin.site.register(DislikeBar)
admin.site.register(presentBar)
admin.site.register(InformationUser)
admin.site.register(SearchInformationUser)