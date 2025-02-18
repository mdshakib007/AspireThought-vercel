from django.contrib import admin
from users.models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',)

admin.site.register(CustomUser, UserAdmin)