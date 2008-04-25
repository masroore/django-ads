# Admin registrations
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from models import Show, Advertiser, AdvertiserUser, Website, WebsiteUser, \
        AdModel, AdBox, Word, URL, Ad, Log, StyleSet, CreditsLog

class ShowAdmin(ModelAdmin):
    list_display = ('group','name','slug','url_pattern',)
    list_display_links = ('name',)

class AdvertiserAdmin(ModelAdmin):
    pass

class AdvertiserUserAdmin(ModelAdmin):
    list_display = ('advertiser','user','type',)
    raw_id_fields = ('user','advertiser',)

class WebsiteAdmin(ModelAdmin):
    pass

class WebsiteUserAdmin(ModelAdmin):
    list_display = ('website','user','type',)
    raw_id_fields = ('user','website',)

class AdModelAdmin(ModelAdmin):
    pass

class AdModelAdmin(ModelAdmin):
    pass

class AdBoxAdmin(ModelAdmin):
    raw_id_fields = ('website',)

class WordAdmin(ModelAdmin):
    pass

class URLAdmin(ModelAdmin):
    raw_id_fields = ('website',)

class AdAdmin(ModelAdmin):
    list_display = ('title','advertiser','view_credits','click_credits','view_count','click_count','enabled','all_words','limited_by_credits')
    list_filter = ('enabled','all_words','limited_by_credits')
    raw_id_fields = ('advertiser','words',)

class LogAdmin(ModelAdmin):
    raw_id_fields = ('ad','website_url',)

class StyleSetAdmin(ModelAdmin):
    pass

class CreditsLogAdmin(ModelAdmin):
    raw_id_fields = ('ad',)

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
admin.site.register(CreditsLog, CreditsLogAdmin)

