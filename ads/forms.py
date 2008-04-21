from django import newforms as forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import AuthenticationForm

from models import Advertiser, Website, Ad, Word, AdBox

class FormLogin(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

class FormAdvertiser(forms.ModelForm):
    class Meta:
        model = Advertiser
        exclude = ('since',)

class FormWebsite(forms.ModelForm):
    class Meta:
        model = Website
        exclude = ('since',)

class FormAd(forms.ModelForm):
    words = forms.CharField(max_length=100, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.base_fields['description'].widget = forms.Textarea()

        super(FormAd, self).__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            self.initial['words'] = ' '.join([w.slug for w in self.instance.words.all()])

    def save(self, advertiser):
        words = [s.strip() for s in self.cleaned_data['words'].split(' ')]
        words_objs = []

        for word in words:
            w, new = Word.objects.get_or_create(slug=slugify(word))
            words_objs.append(unicode(w.id))

        ad = super(FormAd, self).save(False)
        ad.advertiser = advertiser
        ad.save()

        ad.words.clear()

        for word in words_objs:
            ad.words.add(word)

        return ad

    class Meta:
        model = Ad
        fields = ('title','description','url','all_words','enabled',
                'click_limit_per_day',)

class FormAdBox(forms.ModelForm):
    class Meta:
        model = AdBox
        fields = ('ad_model','styleset',)

