from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

class Ad(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    group = models.SlugField(max_length=50, help_text=_('Type a keyword to make this ad part of a group'))
    template_body = models.TextField(null=True, blank=True)
    url_pattern = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('group','name')

# SIGNALS AND LISTENERS
from django.db.models import signals
from django.dispatch import dispatcher

# Ad
def ad_pre_save(sender, instance, signal, *args, **kwargs):
    instance.slug = slugify(instance.name)
    instance.group = slugify(instance.group)

dispatcher.connect(ad_pre_save, signal=signals.pre_save, sender=Ad)

