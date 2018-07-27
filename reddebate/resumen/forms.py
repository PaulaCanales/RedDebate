# -*- coding: utf-8 -*-

from django import forms
from resumen.models import Debate

caracteres = [('300', '300'),
                ('200','200'),
                ('140','140')]
creador=[('username','Nombre Real'),
         ('alias','Alias')]

class creaDebateForm(forms.ModelForm):
    titulo = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe un título...'
        }))
    descripcion = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe una descripción...',
            'rows': 8
        }))
    date_fin = forms.DateField(
        required=False,
        label='Fecha fin',
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker',
            }))
    alias_c = forms.CharField(
        label='Publicar debate con',
        widget=forms.Select(
            choices=creador,
            attrs={'class': 'form-control'}
            ))
    largo = forms.CharField(
        label='Largo máximo de los argumentos',
        widget=forms.Select(
            choices=caracteres,
            attrs={'class': 'form-control'}
            ))
    img = forms.FileField(label='Añadir imagen', required=False)
    class Meta:
        model = Debate
        fields = ('id_debate', 'titulo', 'descripcion', 'date_fin', 'alias_c', 'largo', 'img')
