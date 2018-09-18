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

class modificaImagen(forms.Form):
    img = forms.FileField(label='Añadir imagen', required=False,
        widget=forms.FileInput(
            attrs={'id': 'debImgForm'}
            ))

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

class seleccionaUsuarios(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.usuarios = kwargs.pop('usuarios')
        self.lista = kwargs.pop('lista')
        super(seleccionaUsuarios,self).__init__(*args,**kwargs)
        if self.usuarios:
            self.fields['usuario'].choices = [(x.id, x) for x in self.usuarios]
        if self.lista:
            self.fields['lista_id'].widget=forms.TextInput(
                attrs={
                    'value': self.lista,
                    'type': 'hidden',
                })
    lista_id = forms.CharField(widget=forms.TextInput())
    usuario = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'usuarioListadoForm'}
        ),
        label="Usuarios")
    class Meta:
        model = UsuarioListado
        fields = ('id', 'usuario', 'lista_id')

class seleccionaListados(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.listas = kwargs.pop('listas')
        self.usuario = kwargs.pop('usuario')
        super(seleccionaListados,self).__init__(*args,**kwargs)
        if self.listas:
            self.fields['lista_id'].choices = [(x['id'], x['nombre']) for x in self.listas]
        if self.usuario:
            self.fields['usuario'].widget=forms.TextInput(
                attrs={
                    'value': self.usuario,
                    'type': 'hidden',
                })
    usuario = forms.CharField(widget=forms.TextInput())
    lista_id = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'ListadoForm'}
        ),
        label="Listas")
    nueva = forms.CharField(required=False, widget=forms.TextInput(
    attrs={
        'class': 'form-control',
        'placeholder': 'Escribe un nombre...',
        'maxlength': 100,
    }))
    class Meta:
        model = UsuarioListado
        fields = ('id', 'usuario', 'lista_id')
