# -*- coding: utf-8 -*-

from django import forms
from debate.models import Argumento, Respuesta
from django.core.validators import MaxLengthValidator

class newArgForm1(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.creador = kwargs.pop('creador')
        self.max_length = kwargs.pop('max_length')
        super(newArgForm1,self).__init__(*args,**kwargs)
        if self.creador:
            self.fields['alias_c'].widget=forms.Select(
                    choices=self.creador,
                    attrs={'class': 'form-control', 'maxlength': "30", 'id':"aliasArg1"}
                    )
        if self.max_length:
            self.fields['descripcion'].widget=forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Escribe un argumento...',
                        'rows': 3,
                        'maxlength': self.max_length,
                        'id': 'descArg1'
                })
    descripcion = forms.CharField(label=False)
    alias_c = forms.CharField(label=False)
    class Meta:
        model = Argumento
        fields = ('id_argumento', 'descripcion', 'alias_c')
class newArgForm0(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.creador = kwargs.pop('creador')
        self.max_length = kwargs.pop('max_length')
        super(newArgForm0,self).__init__(*args,**kwargs)
        if self.creador:
            self.fields['alias_c'].widget=forms.Select(
                    choices=self.creador,
                    attrs={'class': 'form-control', 'maxlength': "30", 'id':"aliasArg0"}
                    )
        if self.max_length:
            self.fields['descripcion'].widget=forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Escribe un argumento...',
                        'rows': 3,
                        'maxlength': self.max_length,
                        'id': 'descArg0'
                })

    descripcion = forms.CharField(label=False)
    alias_c = forms.CharField(label=False)
    class Meta:
        model = Argumento
        fields = ('id_argumento', 'descripcion', 'alias_c')

class newCounterargForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.creador = kwargs.pop('creador')
        self.max_length = kwargs.pop('max_length')
        super(newCounterargForm,self).__init__(*args,**kwargs)
        if self.creador:
            self.fields['alias_c'].widget=forms.Select(
                    choices=self.creador,
                    attrs={'class': 'form-control', 'maxlength': "30"}
                    )
        if self.max_length:
            self.fields['descripcion'].widget=forms.Textarea(
                    attrs={
                        'id': 'rebateDesc',
                        'class': 'form-control',
                        'placeholder': 'Escribe un rebate...',
                        'rows': 2,
                        'maxlength': self.max_length
                })

    descripcion = forms.CharField(label=False)
    alias_c = forms.CharField(label=False)
    class Meta:
        model = Respuesta
        fields = ('id_respuesta', 'descripcion', 'alias_c')
