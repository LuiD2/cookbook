from django.shortcuts import render
from django.views import generic
from menus.models import Menu
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse


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
    template_name = 'menus/add_menu.html'
    model = Menu
    fields = ['name', 'servings']

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return super(MenuCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('menu_detail', kwargs={'pk': self.pk})
