from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import User  # Or your custom user model

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')  # Add 'id' here

admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, UserAdmin)  # Register it again with the custom admin class

