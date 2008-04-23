# Admin registrations
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from models import Show, Advertiser, AdvertiserUser, Website, WebsiteUser, \
        AdModel, AdBox, Word, URL, Ad, Log, StyleSet

class ShowAdmin(ModelAdmin):
    list_display = ('group','name','slug','url_pattern',)
    list_display_links = ('name',)

class AdvertiserAdmin(ModelAdmin):
    pass

class AdvertiserUserAdmin(ModelAdmin):
    pass

class WebsiteAdmin(ModelAdmin):
    pass

class WebsiteUserAdmin(ModelAdmin):
    pass

class AdModelAdmin(ModelAdmin):
    pass

class AdModelAdmin(ModelAdmin):
    pass

class AdBoxAdmin(ModelAdmin):
    pass

class WordAdmin(ModelAdmin):
    pass

class URLAdmin(ModelAdmin):
    pass

class AdAdmin(ModelAdmin):
    list_display = ('title','advertiser','view_credits','click_credits','view_count','click_count','enabled','all_words','limited_by_credits')
    list_filter = ('enabled','all_words','limited_by_credits')

class LogAdmin(ModelAdmin):
    pass

class StyleSetAdmin(ModelAdmin):
    pass

admin.site.register(Show, ShowAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(AdvertiserUser, AdvertiserUserAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(WebsiteUser, WebsiteUserAdmin)
admin.site.register(AdModel, AdModelAdmin)
admin.site.register(AdBox, AdBoxAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(URL, URLAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(StyleSet, StyleSetAdmin)

