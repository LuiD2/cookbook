from django.shortcuts import render
from django.views import generic
from menus.models import Menu
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView


# Create your views here.
class IndexView(generic.ListView):
    model = Menu
    template_name = 'menus/index.html'
    context_object_name = 'menus'


class DetailView(generic.DetailView):
    model = Menu
    template_name = 'menus/detail.html'


class MenuRecipeDetailView(generic.DetailView):
    model = Menu
    template_name = 'menus/MenuRecipeDetail.html'


class MenuCreateView(CreateView):
    model = Menu
    template_name = 'menus/add_menu.html'
    fields = ['name', 'recipes', 'servings']
