from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from forms import UserForm
from models import Profile

class UserAdmin(UserAdmin):
    add_form = UserForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password')}
        ),
    )

class ProfileAdmin(admin.ModelAdmin):
    exclude = ('activation_key',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
