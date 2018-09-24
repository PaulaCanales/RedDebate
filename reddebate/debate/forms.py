# -*- coding: utf-8 -*-

from django import forms
from debate.models import Argumento, Counterargument
from django.core.validators import MaxLengthValidator

class newArgForm1(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.owner = kwargs.pop('owner')
        self.max_length = kwargs.pop('max_length')
        super(newArgForm1,self).__init__(*args,**kwargs)
        if self.owner:
            self.fields['owner_type'].widget=forms.Select(
                    choices=self.owner,
                    attrs={'class': 'form-control', 'maxlength': "30", 'id':"aliasArg1"}
                    )
        if self.max_length:
            self.fields['text'].widget=forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Escribe un argument...',
                        'rows': 3,
                        'maxlength': self.max_length,
                        'id': 'descArg1'
                })
    text = forms.CharField(label=False)
    owner_type = forms.CharField(label=False)
    class Meta:
        model = Argumento
        fields = ('id_argument', 'text', 'owner_type')
class newArgForm0(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.owner = kwargs.pop('owner')
        self.max_length = kwargs.pop('max_length')
        super(newArgForm0,self).__init__(*args,**kwargs)
        if self.owner:
            self.fields['owner_type'].widget=forms.Select(
                    choices=self.owner,
                    attrs={'class': 'form-control', 'maxlength': "30", 'id':"aliasArg0"}
                    )
        if self.max_length:
            self.fields['text'].widget=forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Escribe un argument...',
                        'rows': 3,
                        'maxlength': self.max_length,
                        'id': 'descArg0'
                })

    text = forms.CharField(label=False)
    owner_type = forms.CharField(label=False)
    class Meta:
        model = Argumento
        fields = ('id_argument', 'text', 'owner_type')

class newCounterargForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.owner = kwargs.pop('owner')
        self.max_length = kwargs.pop('max_length')
        super(newCounterargForm,self).__init__(*args,**kwargs)
        if self.owner:
            self.fields['owner_type'].widget=forms.Select(
                    choices=self.owner,
                    attrs={'class': 'form-control', 'maxlength': "30"}
                    )
        if self.max_length:
            self.fields['text'].widget=forms.Textarea(
                    attrs={
                        'id': 'rebateDesc',
                        'class': 'form-control',
                        'placeholder': 'Escribe un rebate...',
                        'rows': 2,
                        'maxlength': self.max_length
                })

    text = forms.CharField(label=False)
    owner_type = forms.CharField(label=False)
    class Meta:
        model = Counterargument
        fields = ('id_counterarg', 'text', 'owner_type')
