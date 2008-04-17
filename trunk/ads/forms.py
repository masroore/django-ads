from django import newforms as forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from models import Advertiser, Website

class FormAccount(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=30, widget=forms.PasswordInput)
    
    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).count():
            raise forms.ValidationError(_('Username already exists!'))

        return self.cleaned_data['username']
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError(_('E-mail already exists!'))

        return self.cleaned_data['email']
    
    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise forms.ValidationError(_('Confirm password correctly!'))

        return self.cleaned_data['confirm']

class FormAdvertiser(forms.ModelForm):
    class Meta:
        model = Advertiser
        exclude = ('since',)

class FormWebsite(forms.ModelForm):
    class Meta:
        model = Website
        exclude = ('since',)

