from django.conf.urls.defaults import *

urlpatterns = patterns('apps.ads.views',
    (r'^$', 'index'),
    (r'^create_account/$', 'create_account'),
    (r'^create_advertiser/$', 'advertiser_create'),
    (r'^create_website/$', 'website_create'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),

    (r'^advertiser/(?P<advertiser_id>\d+)/$', 'advertiser_home'),
    (r'^advertiser/(?P<advertiser_id>\d+)/create_ad/$', 'ad_edit'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/$', 'ad_home'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/edit/$', 'ad_edit'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/delete/$', 'ad_delete'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/hit/$', 'ad_hit'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/cd/latest30days/$', 'ad_chart_data_last30days'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/cd/days_of_month/$', 'ad_chart_data_days_of_month'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/cd/days_of_week/$', 'ad_chart_data_days_of_week'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/cd/months/$', 'ad_chart_data_months'),
    (r'^advertiser/(?P<advertiser_id>\d+)/ad/(?P<ad_id>\d+)/cd/hours/$', 'ad_chart_data_hours'),
    
    (r'^website/(?P<website_id>\d+)/$', 'website_home'),
    (r'^website/(?P<website_id>\d+)/create_adbox/$', 'adbox_edit'),
    (r'^website/(?P<website_id>\d+)/adbox/(?P<adbox_id>\d+)/$', 'adbox_home'),
    (r'^website/(?P<website_id>\d+)/adbox/(?P<adbox_id>\d+)/edit/$', 'adbox_edit'),
    (r'^website/(?P<website_id>\d+)/adbox/(?P<adbox_id>\d+)/delete/$', 'adbox_delete'),
    (r'^website/(?P<website_id>\d+)/adbox/(?P<adbox_id>\d+)/get_ads/$', 'adbox_get_ads'),
)


