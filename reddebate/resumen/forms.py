# -*- coding: utf-8 -*-

from django import forms
from resumen.models import Debate

tipoRebate = [('0', 'Ambas posturas'),
                ('1','Postura contraria')]
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
                'id': 'debFinForm',
                'readonly': True,
            }))
    alias_c = forms.CharField(label='Publicar debate como')
    largo = forms.CharField(
        label='Caracteres/argumento',
        widget=forms.TextInput(
            # choices=caracteres,
            attrs={'class':'form-control', 'id': 'debLargoForm', 'value':'140','readonly': True}
            ))
    num_argumento = forms.CharField(
        label='Argumentos/usuario',
        widget=forms.TextInput(
            # choices=rebates,
            attrs={'class': 'form-control', 'id': 'debArgsForm', 'value':'1','readonly': True}
            ))
    num_rebate = forms.CharField(
        label='Rebates/usuario',
        widget=forms.TextInput(
            # choices=rebates,
            attrs={'class': 'form-control', 'id': 'debRebateForm', 'value':'1','readonly': True}
            ))
    num_cambio_postura = forms.CharField(
        label='Cambio postura/usr',
        widget=forms.TextInput(
            # choices=rebates,
            attrs={'class': 'form-control', 'id': 'debCambioPostForm', 'value':'1','readonly': True}
            ))
    tipo_rebate = forms.CharField(
        label='Tipo Redebate',
        widget=forms.Select(
            choices=tipoRebate,
            attrs={'class': 'form-control', 'id': 'debTipoRebateForm'}
            ))
    img = forms.FileField(label='Añadir imagen', required=False,
        widget=forms.FileInput(
            attrs={'id': 'debImgForm'}
            ))
    class Meta:
        model = Debate
        fields = ('id_debate', 'titulo', 'descripcion', 'date_fin', 'alias_c', 'largo', 'num_argumento', 'num_rebate', 'num_cambio_postura', 'tipo_rebate','img')
