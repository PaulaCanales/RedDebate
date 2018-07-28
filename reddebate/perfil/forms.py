# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from perfil.models import Perfil

class modificaAlias(forms.ModelForm):
    error_css_class = 'has-error'
    user = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'hidden',
        }))
    alias = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))
    class Meta:
        model = Perfil
        fields = ('user', 'alias')
