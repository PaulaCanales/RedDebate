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

class creaDebateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.creador = kwargs.pop('creador')
        super(creaDebateForm,self).__init__(*args,**kwargs)
        if self.creador:
            self.fields['alias_c'].widget=forms.Select(
                    choices=self.creador,
                    attrs={'class': 'form-control'}
                    )
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
    alias_c = forms.CharField(label='Publicar debate como')
    largo = forms.CharField(
        label='Largo máximo argumentos',
        widget=forms.Select(
            choices=caracteres,
            attrs={'class': 'form-control'}
            ))
    num_rebate = forms.CharField(
        label='Rebates por usuario',
        widget=forms.Select(
            choices=rebates,
            attrs={'class': 'form-control'}
            ))
    img = forms.FileField(label='Añadir imagen', required=False)
    class Meta:
        model = Debate
        fields = ('id_debate', 'titulo', 'descripcion', 'date_fin', 'alias_c', 'largo', 'num_rebate', 'img')
