from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import PostForm

# Create your views here.
from django.http import HttpResponse
from resumen.models import Usuario, Debate

#class PhotoListView(ListView):
#    model = Photo


#class PhotoDetailView(DetailView):
 #   model = Photo
##hola
def index(request):
	category_list = Debate.objects.all()
	context = {'object_list': category_list}
	return render(request, 'index.html', context)

	#titulos= []
	#argumentos=[]
#debates = Debate.objects.all()
#	for i in range(len(debates)):
#		titulos[i]= debates[i].titulo()
		#argumentos[i] = debates[i].argumento()
#	html = "<html><body>It is now %s  .</body></html>" %  titulos
#	return HttpResponse(html)

#Formulario
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                #return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})