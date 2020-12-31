from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps
from .models import CustomUser

# Register your models here.

app = apps.get_app_config('graphql_auth')
for name, model in app.models.items():
    admin.site.register(model)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'get_full_name', 'email')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )
