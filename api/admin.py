from django.contrib import admin

from .models import Key
# Register your models here.

class KeyAdmin(admin.ModelAdmin):
    fields = ['name']

    list_display = ('user', 'name', 'key', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(KeyAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

admin.site.register(Key, KeyAdmin)
