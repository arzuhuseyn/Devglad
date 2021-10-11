from django.contrib import admin

from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass