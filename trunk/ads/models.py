from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

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

    def __unicode__(self):
        return "%dx%d" %(self.height, self.width)

class AdBox(models.Model):
    website = models.ForeignKey('Website', related_name='ad_boxes')
    ad_model = models.ForeignKey('AdModel', related_name='ad_boxes')
    since = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return unicode(self.ad_model)

    def get_absolute_url(self):
        return '%sadbox/%d/' %( self.website.get_absolute_url(), self.id )

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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '%sad/%d/' %( self.advertiser.get_absolute_url(), self.id )

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
        ordering = ('date',)

# SIGNALS AND LISTENERS
from django.db.models import signals
from django.dispatch import dispatcher

# Show
def show_pre_save(sender, instance, signal, *args, **kwargs):
    instance.slug = slugify(instance.name)
    instance.group = slugify(instance.group)

dispatcher.connect(show_pre_save, signal=signals.pre_save, sender=Show)

