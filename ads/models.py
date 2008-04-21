import re
from datetime import datetime, timedelta

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

USER_TYPES = (
    ('o', _('Owner')),
    ('g', _('Guest')),
)

LOG_TYPES = (
    ('v', _('View')),
    ('c', _('Click')),
)

class Show(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    group = models.SlugField(max_length=50, help_text=_('Type a keyword to make this ad part of a group'))
    template_body = models.TextField(null=True, blank=True)
    url_pattern = models.CharField(max_length=500, null=True, blank=True)
    enabled = models.BooleanField(blank=True, default=True)
    rotative = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('group','name')

class Advertiser(models.Model):
    name = models.CharField(max_length=50)
    enabled = models.BooleanField(blank=True, default=True)
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return self.name

    def set_owner(self, user):
        aduser, new = AdvertiserUser.objects.get_or_create(
                advertiser=self,
                user=user,
                defaults={'type': 'o'},
                )

        if not new and aduser.type != 'o':
            aduser.type = 'o'
            aduser.save()

        return aduser

    def get_absolute_url(self):
        return '/ads/advertiser/%d/' % self.id

    class Meta:
        ordering = ('name',)

class AdvertiserUser(models.Model):
    user = models.ForeignKey(User, related_name='advertiser_users')
    advertiser = models.ForeignKey('Advertiser', related_name='advertiser_users')
    type = models.CharField(max_length=1, blank=True, default='o', choices=USER_TYPES)
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('since',)
        unique_together = (('user','advertiser'),)

class Website(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(null=True, blank=True)
    enabled = models.BooleanField(blank=True, default=True)
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return self.name

    def set_owner(self, user):
        webuser, new = WebsiteUser.objects.get_or_create(
                website=self,
                user=user,
                defaults={'type': 'o'},
                )

        if not new and webuser.type != 'o':
            webuser.type = 'o'
            webuser.save()

        return webuser

    def get_absolute_url(self):
        return '/ads/website/%d/' % self.id

    class Meta:
        ordering = ('name',)

class WebsiteUser(models.Model):
    user = models.ForeignKey(User, related_name='website_users')
    website = models.ForeignKey('Website', related_name='website_users')
    type = models.CharField(max_length=1, blank=True, default='o', choices=USER_TYPES)
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('since',)
        unique_together = (('user','website'),)

class AdModel(models.Model):
    height = models.SmallIntegerField()
    width = models.SmallIntegerField()
    since = models.DateTimeField(blank=True, default=datetime.now)
    css = models.FileField(upload_to=settings.ADS_UPLOAD_CSS_PATH)
    ads_quantity = models.SmallIntegerField()

    def __unicode__(self):
        return "%dx%d" %(self.width, self.height)

class AdBox(models.Model):
    website = models.ForeignKey('Website', related_name='ad_boxes')
    ad_model = models.ForeignKey('AdModel', related_name='ad_boxes')
    styleset = models.ForeignKey('StyleSet', related_name='ad_boxes', null=True, blank=True)
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return unicode(self.ad_model)

    def get_absolute_url(self):
        return '%sadbox/%d/' %( self.website.get_absolute_url(), self.id )

    def generate_code(self):
        return """<div id="adbox_%(id)d"/>\n<script type="text/javascript">cont_id='adbox_%(id)d';website_id=%(w_id)d;adbox_id=%(id)d;adbox_height=%(h)d;adbox_width=%(w)d</script>\n<script type="text/javascript" src="%(url)s/media/ads/ads_client.js"></script>""" %{
                'url': settings.PROJECT_ROOT_URL[:-1],
                'id': self.id,
                'w_id': self.website.id,
                'h': self.ad_model.height,
                'w': self.ad_model.width,
                }

    class Meta:
        ordering = ('since',)

class Word(models.Model):
    slug = models.SlugField()
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return self.slug

    class Meta:
        ordering = ('slug',)

class URL(models.Model):
    url = models.URLField(verify_exists=False)
    website = models.ForeignKey('Website', related_name='urls', null=True, blank=True)
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ('url',)

class Ad(models.Model):
    advertiser = models.ForeignKey('Advertiser', related_name='ads')
    words = models.ManyToManyField('Word', null=True, blank=True)
    title = models.CharField(max_length=40)
    url = models.URLField(verify_exists=False)
    description = models.CharField(max_length=200) # Check if better limite CharField or unlimited TextField
    view_credits = models.IntegerField(blank=True, default=0)
    click_credits = models.IntegerField(blank=True, default=0)
    view_count = models.IntegerField(blank=True, default=0)
    click_count = models.IntegerField(blank=True, default=0)
    credits_amount = models.IntegerField(blank=True, default=0)
    enabled = models.BooleanField(blank=True, default=False)
    all_words = models.BooleanField(blank=True, default=False)
    next_view = models.DateTimeField(null=True, blank=True)
    last_view = models.DateTimeField(null=True, blank=True)
    click_limit_per_day = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '%sad/%d/' %( self.advertiser.get_absolute_url(), self.id )

    def get_hit_url(self):
        return '%s%shit/' %( settings.PROJECT_ROOT_URL[:-1], self.get_absolute_url() )

    def get_short_url(self):
        m = re.match('(http://|)([^/\?]*)', self.url, re.I | re.M)
        return m and m.group(2) or ''

    def __store_hit(self, url, type):
        # Get URL from database
        website_url, new = URL.objects.get_or_create(url=url)

        # Returns the log created
        return Log.objects.create(
                ad=self,
                type=type,
                url=url,
                website_url=website_url,
                )

    def hit_view(self, url):
        # Increment count
        self.view_count = self.view_count + 1
        
        # Decrement credits
        self.view_credits = self.view_credits - 1

        # Save the Ad (self)
        self.last_view = datetime.now()
        self.save()

        return self.__store_hit(url, 'v')

    def hit_click(self, url):
        # Increment count
        self.click_count = self.click_count + 1
        
        # Decrement credits
        self.click_credits = self.click_credits - 1

        # Calculating next view
        now = datetime.now()

        tomorrow = now.today() + timedelta(days=1)
        self.click_limit_per_day = self.click_limit_per_day or 1
        clicks_today = Log.objects.filter(
                ad=self,
                type='c',
                date__startswith="%04d-%02d-%02d"%(now.year, now.month, now.day),
                ).count()
        delta_click = timedelta(seconds=86400 / self.click_limit_per_day) # Click each seconds number

        # Next view is tomorrow if limit was reached
        if clicks_today >= self.click_limit_per_day:
            self.next_view = datetime.today() + timedelta(days=1)

        # Next view is last moment of today if sum of delta is tomorrow
        elif now + delta_click > tomorrow:
            self.next_view = tomorrow - timedelta(seconds=1)

        # Next view is now + delta else
        else:
            self.next_view = now + delta_click

        # Save the Ad (self)
        self.save()

        return self.__store_hit(url, 'c')

    class Meta:
        ordering = ('title',)

class Log(models.Model):
    ad = models.ForeignKey('Ad', related_name='log_entries')
    date = models.DateTimeField(blank=True, default=datetime.now)
    type = models.CharField(max_length=1, choices=LOG_TYPES)
    url = models.URLField(verify_exists=False)
    website_url = models.ForeignKey('URL', related_name='log_entries', null=True, blank=True)

    def __unicode__(self):
        return self.date

    class Meta:
        ordering = ('-date',)

class StyleSet(models.Model):
    name = models.CharField(max_length=20)
    since = models.DateTimeField(blank=True, default=datetime.now)
    css = models.FileField(upload_to=settings.ADS_UPLOAD_CSS_PATH, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

# SIGNALS AND LISTENERS
from django.db.models import signals
from django.dispatch import dispatcher

# Show
def show_pre_save(sender, instance, signal, *args, **kwargs):
    instance.slug = slugify(instance.name)
    instance.group = slugify(instance.group)

dispatcher.connect(show_pre_save, signal=signals.pre_save, sender=Show)

