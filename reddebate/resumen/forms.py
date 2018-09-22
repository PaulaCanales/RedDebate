# -*- coding: utf-8 -*-

from django import forms
from resumen.models import Debate
from django.contrib.auth import authenticate, login

tipoFiltro=[('1','Todos'),
         ('2','Listas'),
         ('3', 'Recomendados')]

tipoRebate = [('0', 'Ambas posturas'),
                ('1','Postura contraria')]
tipoParticipacion = [('0', 'Publico'),
                ('1','Privado a Usuarios Específicos'),
                ('2', 'Privado a Listas')]
creador=[('username','Nombre Real'),
         ('alias','Alias')]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Usuario",
    widget=(forms.TextInput(attrs={"class":"input-login", 'name':"name", 'id':"name"})))
    password = forms.CharField(max_length=20, required=True, label="Contraseña",
    widget=(forms.PasswordInput(attrs={"class":"input-login", 'name':"pass", 'id':"pass"})))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Login incorrecto. Ingrese nuevamente.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class newDebateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.creador = kwargs.pop('creador')
        self.usuarios = kwargs.pop('usuarios')
        self.listas = kwargs.pop('listado')
        super(newDebateForm,self).__init__(*args,**kwargs)
        if self.creador:
            self.fields['alias_c'].widget=forms.Select(
                    choices=self.creador,
                    attrs={'class': 'form-control', 'id': 'debAliasForm'}
                    )
        if self.usuarios:
            self.fields['participantes'].choices = [(x.id, x) for x in self.usuarios]
        if self.listas:
            self.fields['listado'].choices = [(x['id'], x['nombre']) for x in self.listas]

    titulo = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe un título...',
            'id': 'debTituloForm',
            'maxlength': 100,
        }))
    descripcion = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Escribe una descripción...',
            'rows': 8,
            'id': 'debDescripcionForm',
            'maxlength': 1000,
        }))
    date_fin = forms.DateField(
        required=False,
        label='Fecha fin',
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'debFinForm',
                # 'readonly': True,
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
            attrs={'class': 'form-control', 'id': 'debCambioPostForm', 'value':'3','readonly': True}
            ))
    tipo_rebate = forms.CharField(
        label='Tipo Redebate',
        widget=forms.Select(
            choices=tipoRebate,
            attrs={'class': 'form-control', 'id': 'debTipoRebateForm'}
            ))
    tipo_participacion = forms.CharField(
        label='Tipo Debate',
        widget=forms.Select(
            choices=tipoParticipacion,
            attrs={'class': 'form-control', 'id': 'debTipoParticipacionForm'}
            ))
    participantes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'debParticipantesForm'}
        ),
        label="Usuarios")
    listado = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'debListadoForm'}
        ),
        label="Listas")

    img = forms.FileField(label='Añadir imagen', required=False,
        widget=forms.FileInput(
            attrs={'id': 'debImgForm'}
            ))
    # filtro = forms.ChoiceField(choices=tipoFiltro, widget=forms.RadioSelect())
    class Meta:
        model = Debate
        fields = ('id_debate', 'titulo', 'descripcion', 'date_fin', 'alias_c', 'largo', 'num_argumento', 'num_rebate', 'num_cambio_postura', 'tipo_rebate', 'tipo_participacion','img')
