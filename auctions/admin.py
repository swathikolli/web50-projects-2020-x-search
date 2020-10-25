from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import List, Comments, WatchList, Bid
# Register your models here.
admin.site.register(List)
admin.site.register(Comments)
admin.site.register(WatchList)
admin.site.register(Bid)

