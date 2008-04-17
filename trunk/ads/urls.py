from django.conf.urls.defaults import *

urlpatterns = patterns('apps.ads.views',
    (r'^$', 'index'),
    (r'^create_account/$', 'create_account'),
    (r'^create_advertiser/$', 'create_advertiser'),
    (r'^create_website/$', 'create_website'),
    (r'^website/(?P<id>\d+)/$', 'website_home'),
    (r'^advertiser/(?P<id>\d+)/$', 'advertiser_home'),
)


