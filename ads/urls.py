from django.conf.urls.defaults import *

urlpatterns = patterns('apps.ads.views',
    (r'^$', 'index'),
    (r'^create_account/$', 'create_account'),
    (r'^create_advertiser/$', 'advertiser_create'),
    (r'^create_website/$', 'website_create'),

    (r'^advertiser/(?P<advertiser_id>\d+)/$', 'advertiser_home'),
    (r'^advertiser/(?P<advertiser_id>\d+)/create_ad/$', 'ad_create'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/$', 'ad_home'),
    
    (r'^website/(?P<website_id>\d+)/$', 'website_home'),
    (r'^website/(?P<website_id>\d+)/create_adbox/$', 'adbox_create'),
    (r'^website/(?P<website_id>\d+)/adbox/(?P<adbox_id>\d+)/$', 'adbox_home'),
)


