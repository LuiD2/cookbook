from django.shortcuts import render
from django.views import generic
from recipes.models import Recipe

# Create your views here.
class IndexView(generic.ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'

class CreateView(generic.CreateView):
    model = Recipe
    template_name = 'recipes/add.html'
    fields = ['name','source','servings','notes','tags']