# -*- coding: utf-8 -*-

from django import forms
from resumen.models import Debate

caracteres = [('300', '300 caracteres'),
                ('200','200 caracteres'),
                ('140','140 caracteres')]
rebates = [('1', '1'),
                ('2','2'),
                ('3','3')]
creador=[('username','Nombre Real'),
         ('alias','Alias')]

class LoginForm(forms.Form):
    name_user = forms.CharField(max_length=20, required=True, label="",
    widget=(forms.TextInput(attrs={"class":"input-login"})))
    password_user = forms.CharField(max_length=20, required=True, label="",
    widget=(forms.PasswordInput(attrs={"class":"input-login"})))

class creaDebateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.creador = kwargs.pop('creador')
        super(creaDebateForm,self).__init__(*args,**kwargs)
        if self.creador:
            self.fields['alias_c'].widget=forms.Select(
                    choices=self.creador,
                    attrs={'class': 'form-control', 'id': 'debAliasForm'}
                    )
    titulo = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe un título...',
            'id': 'debTituloForm'
        }))
    descripcion = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe una descripción...',
            'rows': 8,
            'id': 'debDescripcionForm'
        }))
    date_fin = forms.DateField(
        required=False,
        label='Fecha fin',
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker',
                'id': 'debFinForm'
            }))
    alias_c = forms.CharField(label='Publicar debate como')
    largo = forms.CharField(
        label='Largo máximo argumentos',
        widget=forms.Select(
            choices=caracteres,
            attrs={'class': 'form-control', 'id': 'debLargoForm'}
            ))
    num_rebate = forms.CharField(
        label='Rebates por usuario',
        widget=forms.Select(
            choices=rebates,
            attrs={'class': 'form-control', 'id': 'debRebateForm'}
            ))
    img = forms.FileField(label='Añadir imagen', required=False,
        widget=forms.FileInput(
            attrs={'id': 'debImgForm'}
            ))
    class Meta:
        model = Debate
        fields = ('id_debate', 'titulo', 'descripcion', 'date_fin', 'alias_c', 'largo', 'num_rebate', 'img')
