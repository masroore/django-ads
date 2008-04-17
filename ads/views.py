from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

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

@login_required
def advertiser_home(request, advertiser_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)

    return render_to_response(
            'ads/advertiser_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
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

@login_required
def ad_home(request, advertiser_id, ad_id):
    advertiser = get_object_or_404(Advertiser, id=advertiser_id)
    ad = get_object_or_404(Ad, id=ad_id)

    return render_to_response(
            'ads/ad_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

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

@login_required
def adbox_home(request, website_id, adbox_id):
    website = get_object_or_404(Website, id=website_id)
    adbox = get_object_or_404(AdBox, id=adbox_id)

    return render_to_response(
            'ads/adbox_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

