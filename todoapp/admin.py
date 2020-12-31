from django.contrib import admin
from .models import Todo

# Register your models here.


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_important',
                    'is_completed', 'owner')
    list_filter = ('is_completed', 'is_important')
    search_fields = ('title',)
