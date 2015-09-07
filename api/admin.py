from django.contrib import admin

from .models import Key
# Register your models here.

class KeyAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'key']

    list_display = ('user', 'name', 'key', 'created_at')

admin.site.register(Key, KeyAdmin)
