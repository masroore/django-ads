import simplejson, re
from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib.djangoplus.shortcuts import render_to_json
from django.conf import settings
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import UserCreationForm

from forms import FormAdvertiser, FormWebsite, FormAd, FormAdBox, FormLogin
from models import Website, Advertiser, Ad, AdBox
from openflashchart import graph as OpenFlashChartGraph, graph_object as OpenFlashChartObject

def index(request):
    return render_to_response(
            'ads/index.html',
            locals(),
            context_instance=RequestContext(request),
            )

def create_account(request):
    if request.POST:
        form_account = UserCreationForm(request.POST)

        if form_account.is_valid():
            user = form_account.save()
            if user:
                user = authenticate(
                        username=form_account.cleaned_data['username'],
                        password=form_account.cleaned_data['password1']
                        )
                auth_login(request, user)
                return HttpResponseRedirect('/ads/')
    else:
        form_account = UserCreationForm()

    return render_to_response(
            'ads/create_account.html',
            locals(),
            context_instance=RequestContext(request),
            )

def login(request):
    if request.POST:
        form_login = FormLogin(request.POST)

        if form_login.is_valid():
            user = authenticate(
                        username=form_login.cleaned_data['username'],
                        password=form_login.cleaned_data['password']
                        )
            auth_login(request, user)
            return HttpResponseRedirect('/ads/')
    else:
        form_login = FormLogin()

    return render_to_response(
            'ads/login.html',
            locals(),
            context_instance=RequestContext(request),
            )

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/ads/')

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

def website_home(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    return render_to_response(
            'ads/website_home.html',
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
    chart = OpenFlashChartObject().render("80%", 200, '%schart_data/'%ad.get_absolute_url(), '/media/ads/')

    return render_to_response(
            'ads/ad_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

def ad_chart_data(request, advertiser_id, ad_id):
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

    g = OpenFlashChartGraph()

    g.title(_('Views and Clicks'), '{font-size: 20px; color: #333}')

    views_data = [d['views'] for d in dates]
    clicks_data = [d['clicks'] for d in dates]

    g.set_data( views_data )
    g.set_data( clicks_data )

    g.line( 2, '0x9933CC', 'Views', 10 )
    g.line_dot( 3, 5, '0xCC3399', 'Clicks', 10)
    #g.line_hollow( 2, 4, '0x80a033', 'Bounces', 10 )
    
    g.set_x_labels( [d['date'].day for d in dates] )
    g.set_x_label_style( 10, '0x000000', 0, 2 )
    
    g.set_y_max( max( [d['views'] for d in dates] + [d['clicks'] for d in dates] ) )
    g.y_label_steps( 4 )
    #g.set_y_legend( 'Open Flash Chart', 12, '#736AFF' )

    return HttpResponse(g.render())

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
    ads = Ad.objects.filter(
            enabled=True,           # only enabled Ads
            words__slug__in=words,  # only with request words
            ).exclude(
                all_words=True,
                )

    # only when next view is before than tomorrow
    ads = ads.filter(next_view__lt='%04d-%02d-%02d 00:00:00'%(tomorrow.year, tomorrow.month, tomorrow.day)) |\
          ads.filter(next_view__isnull=True)
    #.filter(view_credits__gt=0).filter(click_credits__gt=0)

    # Orders by next view
    ads = ads.order_by('next_view')

    # Evite duplicated ads and limited by quantity
    ads = ads.distinct()[:adbox.ad_model.ads_quantity]

    # If limit was not reached, complement with "all words" ads
    if ads.count() < adbox.ad_model.ads_quantity:
        extra_ads = Ad.objects.filter(
                enabled=True,       # only enabled Ads
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

