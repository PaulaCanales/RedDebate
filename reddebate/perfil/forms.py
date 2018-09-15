# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from perfil.models import Perfil, Listado, UsuarioListado

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

class creaListado(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe un nombre...',
            'maxlength': 100,
        }))
    class Meta:
        model = Listado
        fields = ('id','nombre')

class agregaUsuarioListado(forms.ModelForm):
    class Meta:
        model = UsuarioListado
        fields = ('id', 'lista', 'usuario')
