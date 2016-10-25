from django import forms
from .models import Debate

class PostForm(forms.ModelForm):
	class Meta:
		model = Debate
		fields = ('titulo', 'argumento',)