import simplejson, re
from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib.djangoplus.shortcuts import render_to_json
from django.conf import settings
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache
from django.utils.dates import MONTHS

from forms import FormAdvertiser, FormWebsite, FormAd, FormAdBox
from models import Website, Advertiser, Ad, AdBox
from openflashchart import graph as OpenFlashChartGraph, graph_object as OpenFlashChartObject
import app_settings

def index(request):
    return render_to_response(
            'ads/index.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def advertiser_create(request):
    if request.POST:
        form_advertiser = FormAdvertiser(request.POST)

        if form_advertiser.is_valid():
            advertiser = form_advertiser.save()
            if advertiser:
                advertiser.set_owner(request.user)
                request.user.message_set.create(message=_('Advertiser account created!'))
                return HttpResponseRedirect('/ads/')
    else:
        form_advertiser = FormAdvertiser()

    return render_to_response(
            'ads/advertiser_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def website_create(request):
    if request.POST:
        form_website = FormWebsite(request.POST)

        if form_website.is_valid():
            website = form_website.save()
            if website:
                website.set_owner(request.user)
                request.user.message_set.create(message=_('Website account created!'))
                return HttpResponseRedirect('/ads/')
    else:
        form_website = FormWebsite()

    return render_to_response(
            'ads/website_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

def advertiser_home(request, advertiser_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)

    return render_to_response(
            'ads/advertiser_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def advertiser_edit(request, advertiser_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)

    if not advertiser.advertiser_users.filter(type='o', user=request.user).count():
        raise Http404

    if request.POST:
        form_advertiser = FormAdvertiser(request.POST, instance=advertiser)

        if form_advertiser.is_valid():
            if form_advertiser.save():
                return HttpResponseRedirect(advertiser.get_absolute_url())
    else:
        form_advertiser = FormAdvertiser(instance=advertiser)

    return render_to_response(
            'ads/advertiser_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

def website_home(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    return render_to_response(
            'ads/website_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def website_edit(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    if not website.website_users.filter(type='o', user=request.user).count():
        raise Http404

    if request.POST:
        form_website = FormWebsite(request.POST, instance=website)

        if form_website.is_valid():
            if form_website.save():
                return HttpResponseRedirect(website.get_absolute_url())
    else:
        form_website = FormWebsite(instance=website)

    return render_to_response(
            'ads/website_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def ad_edit(request, advertiser_id, ad_id=None):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = ad_id and get_object_or_404(Ad, id=ad_id) or None

    if request.POST:
        form_ad = FormAd(request.POST, instance=ad)

        if form_ad.is_valid():
            ad = form_ad.save(advertiser)
            if ad:
                request.user.message_set.create(message=_('Ad saved!'))
                return HttpResponseRedirect(advertiser.get_absolute_url())
    else:
        form_ad = FormAd(instance=ad)

    return render_to_response(
            'ads/ad_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def ad_delete(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    ad.delete()

    request.user.message_set.create(message=_('Ad Deleted!'))
    return HttpResponseRedirect('/ads/')

def ad_home(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    w = app_settings.ADS_CHARTS_WIDTH
    h = app_settings.ADS_CHARTS_HEIGHT
    
    chart_latest30days = OpenFlashChartObject().render(w, h, '%scd/latest30days/'%ad.get_absolute_url(), '/media/ads/')
    chart_days_of_month = OpenFlashChartObject().render(w, h, '%scd/days_of_month/'%ad.get_absolute_url(), '/media/ads/')
    chart_days_of_week = OpenFlashChartObject().render(w, h, '%scd/days_of_week/'%ad.get_absolute_url(), '/media/ads/')
    chart_months = OpenFlashChartObject().render(w, h, '%scd/months/'%ad.get_absolute_url(), '/media/ads/')
    chart_hours = OpenFlashChartObject().render(w, h, '%scd/hours/'%ad.get_absolute_url(), '/media/ads/')

    return render_to_response(
            'ads/ad_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

def ad_chart_data_last30days(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    final_date = datetime(*datetime.today().timetuple()[:3])
    start_date = final_date - timedelta(days=30)

    dates = []
    cur_date = start_date
    while cur_date <= final_date:
        log_entries = ad.log_entries.filter(date__year=cur_date.year, date__month=cur_date.month, date__day=cur_date.day)
        dates.append({
            'date': cur_date,
            'views': log_entries.filter(type='v').count(),
            'clicks': log_entries.filter(type='c').count(),
            })
        cur_date = cur_date + timedelta(days=1)

    views_data = [d['views'] for d in dates]
    clicks_data = [d['clicks'] for d in dates]

    g = OpenFlashChartGraph()

    g.line( 2, '0x9933CC', _('Views'), 10 )
    g.set_data( views_data )

    g.line_dot( 3, 5, '0xCC3399', _('Clicks'), 10)
    g.set_data( clicks_data )
    
    g.set_x_labels( [d['date'].day for d in dates] )
    g.set_x_label_style( 10, '0x000000', 0, 2 )
    
    g.set_y_max( max( [d['views'] for d in dates] + [d['clicks'] for d in dates] ) )
    g.y_label_steps( 4 )

    return HttpResponse(g.render())

def ad_chart_data_bar(dates, labels=[]):
    views_data = [d['views'] for d in dates]
    clicks_data = [d['clicks'] for d in dates]

    g = OpenFlashChartGraph()

    g.bar_3d( 75, '#D54C78', _('Views'), 10 )
    g.set_data(views_data)
    
    g.bar_3d( 75, '#3334AD', _('Clicks'), 10 )
    g.set_data(clicks_data)
    
    g.set_x_axis_3d( 12 )
    g.x_axis_colour = '#909090'
    g.x_grid_colour = '#ADB5C7'
    g.y_axis_colour = '#909090'
    g.y_grid_colour = '#ADB5C7'
    
    g.set_x_labels( labels or [d['date'] for d in dates] )
    g.set_y_max( max( [d['views'] for d in dates] + [d['clicks'] for d in dates] ) )
    g.y_label_steps( 5 )

    return HttpResponse(g.render())

def ad_chart_data_days_of_month(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    dates = []
    for day in range(1,32):
        log_entries = ad.log_entries.filter(date__day=day)
        dates.append({
            'date': day,
            'views': log_entries.filter(type='v').count(),
            'clicks': log_entries.filter(type='c').count(),
            })

    return ad_chart_data_bar(dates)

def ad_chart_data_days_of_week(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    dates = []
    for day in range(7):
        if settings.DATABASE_ENGINE == 'sqlite3':
            log_entries = ad.log_entries.extra(where=["strftime('%%w', date) = %s"], params=[str(day)])
        else:
            log_entries = ad.log_entries.extra(where=["extract(dow from date) = %s"], params=[str(day)])
        dates.append({
            'date': day,
            'views': log_entries.filter(type='v').count(),
            'clicks': log_entries.filter(type='c').count(),
            })

    return ad_chart_data_bar(dates)

def ad_chart_data_months(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    dates = []
    for month in range(1,13):
        log_entries = ad.log_entries.filter(date__month=month)
        dates.append({
            'date': month,
            'views': log_entries.filter(type='v').count(),
            'clicks': log_entries.filter(type='c').count(),
            })

    return ad_chart_data_bar(dates)

def ad_chart_data_hours(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    dates = []
    for hour in range(24):
        if settings.DATABASE_ENGINE == 'sqlite3':
            log_entries = ad.log_entries.extra(where=["strftime('%%H', date) = %s"], params=["%02d"%hour])
        else:
            log_entries = ad.log_entries.extra(where=["extract(hour from date) = %s"], params=["%02d"%hour])
        dates.append({
            'date': hour,
            'views': log_entries.filter(type='v').count(),
            'clicks': log_entries.filter(type='c').count(),
            })

    return ad_chart_data_bar(dates)

@never_cache
def ad_hit(request, advertiser_id, ad_id):
    try:
        #advertiser = get_object_or_404(Advertiser, id=advertiser_id)
        ad = Ad.objects.get(id=ad_id)
        ad.hit_click(request.GET['referer'])

        return HttpResponseRedirect(ad.url)
    except Ad.DoesNotExist, e:
        return HttpResponseRedirect(settings.PROJECT_ROOT_URL)

@login_required
def adbox_edit(request, website_id, adbox_id=None):
    website = get_object_or_404(Website, id=website_id)
    adbox = adbox_id and get_object_or_404(AdBox, id=adbox_id) or None

    if request.POST:
        form_adbox = FormAdBox(request.POST, instance=adbox)

        if form_adbox.is_valid():
            adbox = form_adbox.save(False)
            
            if adbox:
                adbox.website = website
                adbox.save()
                request.user.message_set.create(message=_('AdBox saved!'))
                return HttpResponseRedirect(website.get_absolute_url())
    else:
        form_adbox = FormAdBox(instance=adbox)

    return render_to_response(
            'ads/adbox_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def adbox_delete(request, website_id, adbox_id):
    website = get_object_or_404(Website, id=website_id)
    adbox = get_object_or_404(AdBox, id=adbox_id)

    adbox.delete()

    request.user.message_set.create(message=_('AdBox Deleted!'))
    return HttpResponseRedirect('/ads/')

def adbox_home(request, website_id, adbox_id):
    website = get_object_or_404(Website, id=website_id)
    adbox = get_object_or_404(AdBox, id=adbox_id)

    return render_to_response(
            'ads/adbox_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

@never_cache
def adbox_get_ads(request, website_id, adbox_id):
    """View function that returs the ads html for be shown in the iframe"""
    #website = get_object_or_404(Website, id=website_id)
    adbox = get_object_or_404(AdBox, id=adbox_id)

    # Get referer to use as origin URL when user clicks
    referer = request.GET.get('referer', '')

    # Get 'words' argument with relevant words in the page body
    words = [slugify(w) for w in request.GET.get('words', '').split(',') if w]

    tomorrow = datetime.today() + timedelta(days=1)

    # Filters enabled and by words
    ads = Ad.objects.with_credits().filter(
            words__slug__in=words,  # only with request words
            ).exclude(
                all_words=True,
                )

    # only when next view is before than tomorrow
    ads = ads.filter(next_view__lt='%04d-%02d-%02d 00:00:00'%(tomorrow.year, tomorrow.month, tomorrow.day)) |\
          ads.filter(next_view__isnull=True)

    # Orders by next view
    ads = ads.order_by('next_view')

    # Evite duplicated ads and limited by quantity
    ads = ads.distinct()[:adbox.ad_model.ads_quantity]

    # If limit was not reached, complement with "all words" ads
    if ads.count() < adbox.ad_model.ads_quantity:
        extra_ads = Ad.objects.with_credits().filter(
                all_words=True,     # only with request words
                ).exclude(
                    id__in=[ad.id for ad in ads]
                    ).distinct()
    else:
        extra_ads = []

    # Evite duplicated ads and limited by quantity
    ads = [a for a in ads] + [a for a in extra_ads]
    ads = ads[:adbox.ad_model.ads_quantity]

    # Stores the view hit in each of selected ads
    for ad in ads: ad.hit_view(referer)

    return render_to_response(
            'ads/adbox_ads.html',
            locals(),
            context_instance=RequestContext(request),
            )

