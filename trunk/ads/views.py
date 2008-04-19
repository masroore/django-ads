import simplejson, re
from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib.djangoplus.shortcuts import render_to_json
from django.conf import settings
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache

from forms import FormAccount, FormAdvertiser, FormWebsite, FormAd, FormAdBox
from models import Website, Advertiser, Ad, AdBox

def index(request):
    form_account = FormAccount()

    return render_to_response(
            'ads/index.html',
            locals(),
            context_instance=RequestContext(request),
            )

def create_account(request):
    if request.POST:
        form_account = FormAccount(request.POST)

        if form_account.is_valid():
            user = form_account.save()
            if user:
                user = authenticate(
                        username=user.username,
                        password=form_account.cleaned_data['password']
                        )
                login(request, user)
                return HttpResponseRedirect('/ads/')
    else:
        form_account = FormAccount()

    return render_to_response(
            'ads/create_account.html',
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

def website_home(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    return render_to_response(
            'ads/website_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def ad_create(request, advertiser_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)

    if request.POST:
        form_ad = FormAd(request.POST)

        if form_ad.is_valid():
            ad = form_ad.save(advertiser)
            if ad:
                request.user.message_set.create(message=_('Ad created!'))
                return HttpResponseRedirect(advertiser.get_absolute_url())
    else:
        form_ad = FormAd()

    return render_to_response(
            'ads/ad_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

def ad_home(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    return render_to_response(
            'ads/ad_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

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
def adbox_create(request, website_id):
    website = get_object_or_404(Website, id=website_id)

    if request.POST:
        form_adbox = FormAdBox(request.POST)

        if form_adbox.is_valid():
            adbox = form_adbox.save(False)
            
            if adbox:
                adbox.website = website
                adbox.save()
                request.user.message_set.create(message=_('AdBox created!'))
                return HttpResponseRedirect(website.get_absolute_url())
    else:
        form_adbox = FormAdBox()

    return render_to_response(
            'ads/adbox_edit.html',
            locals(),
            context_instance=RequestContext(request),
            )

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
            next_view__lt='%04d-%02d-%02d 00:00:00'%(tomorrow.year, tomorrow.month, tomorrow.day), # only when next view is before than tomorrow
            )
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

