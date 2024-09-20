from django.contrib import admin
from .models import (
    FriendRequest, 
    UserBlock, 
    Cooldown
    )
# Register your models here.

admin.site.register(FriendRequest)
admin.site.register(UserBlock)
admin.site.register(Cooldown)
