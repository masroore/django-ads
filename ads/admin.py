# Admin registrations
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from models import Ad

class AdAdmin(ModelAdmin):
    list_display = ('group','name','slug','url_pattern',)

admin.site.register(Ad, AdAdmin)

