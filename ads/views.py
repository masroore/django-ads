from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from forms import FormAccount, FormAdvertiser, FormWebsite
from models import Website, Advertiser

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
def create_advertiser(request):
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
def create_website(request):
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
def advertiser_home(request, id):
    advertiser = get_object_or_404(Advertiser, id=id)

    return render_to_response(
            'ads/advertiser_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

@login_required
def website_home(request, id):
    website = get_object_or_404(Website, id=id)

    return render_to_response(
            'ads/website_home.html',
            locals(),
            context_instance=RequestContext(request),
            )

