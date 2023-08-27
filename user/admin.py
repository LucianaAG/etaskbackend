from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


class UserAdmin(UserAdmin):
    list_display=('id', 'email', 'is_admin', 'is_active', 'date_joined', 'last_login')

admin.site.register(User, UserAdmin)




