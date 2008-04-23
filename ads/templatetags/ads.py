import re

from django import template
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.conf import settings

from apps.ads.models import Show

ADS_USE_DJANGOPLUS = getattr(settings, 'ADS_USE_DJANGOPLUS', False)

register = template.Library()

def test_conditions(ad, context):
    if not ad.conditions:
        return True

    tpl = "{% if "+ad.conditions+" %}1{% endif %}"

    if ADS_USE_DJANGOPLUS:
        tpl = "{% load djangoplus %}" + tpl

    res = template.Template(tpl).render(context)

    return res == '1'

# ---
# Template tag {% ad "slug-identifier" %}
# ---

def do_ad(parser, token):
    try:
        tag_name, slug = token.split_contents()
    except ValueError, e:
        raise template.TemplateSyntaxError, "%s requires a single argument" \
                % token.contents.split()[0]

    return AdRender(slugify(slug))

class AdRender(template.Node):
    slug = None

    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        try:
            ad = Show.objects.get(slug=self.slug, enabled=True)

            return ad.template_body
        except template.VariableDoesNotExist, e:
            return ''

register.tag('ad', do_ad)

# ---
# Template tag {% ad_by_group "group-identifier" %}
# ---

def do_ad_by_group(parser, token):
    try:
        tag_name, group = token.split_contents()
    except ValueError, e:
        raise template.TemplateSyntaxError, "%s requires a single argument" \
                % token.contents.split()[0]

    return AdGroupRender(slugify(group))

class AdGroupRender(template.Node):
    group = None

    def __init__(self, group):
        self.group = group

    def render(self, context):
        ads = Show.objects.filter(group=self.group, enabled=True).order_by('-url_pattern','-conditions','id')

        template_body = ''

        if ads.count() == 1 and not ads[0].url_pattern and test_conditions(ads[0], context):
            template_body = ads[0].template_body
        elif ads.count() and 'request' in context:
            url = context['request'].get_full_path()

            for ad in ads.filter(url_pattern__isnull=False):
                if re.match(ad.url_pattern, url, re.I) and test_conditions(ad, context):
                    template_body = ad.template_body
                    break

            if not template_body and ads.filter(url_pattern__isnull=True).count():
                template_body = ads.filter(url_pattern__isnull=True)[0].template_body

        return template.Template(template_body).render(context)

register.tag('ad_by_group', do_ad_by_group)

