from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import PostForm

# Create your views here.
from django.http import HttpResponse
from resumen.models import Usuario, Debate


def index(request):
	category_list = Debate.objects.all()
	context = {'object_list': category_list}
	return render(request, 'index.html', context)

#Formulario
def post_new(request):
        form = PostForm()
        return render(request, 'post_edit.html', {'form': form})