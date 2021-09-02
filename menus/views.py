from django.shortcuts import render
from django.views import generic
from menus.models import Menu
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse
import json


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
    template_name = 'menus/menu_recipe_detail.html'
    
    def get_object(self):
        try:
            self.menu = Menu.objects.get(pk=self.kwargs['menuID'])
            self.recipe = self.menu.recipes.get(pk=self.kwargs['recipeID'])
            return self.recipe
        except (Menu.DoesNotExist, Recipe.DoesNotExist):
            raise Http404("Sorry, couldn't find it.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.menu
        context['recipe'] = self.recipe
        context['stepsAndIngredients'] = json.loads(self.recipe.stepsAndIngredients)
        
        return context

class ShoppingDetailView(generic.DetailView):
    model = Menu
    template_name = 'menus/shopping.html'
    
    def get_object(self):
        try:
            self.menu = Menu.objects.get(pk=self.kwargs['menuID'])
            return self.menu
        except (Menu.DoesNotExist):
            raise Http404("Sorry, couldn't find it.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.menu
        item = self.menu.recipes.all()
        context['ingredients'] = list()
        for thing in item:
            print(json.loads(thing.stepsAndIngredients)['ingredients'])
            context['ingredients'] += json.loads(thing.stepsAndIngredients)['ingredients']
        return context

class MenuCreateView(CreateView):
    template_name = 'menus/add_menu.html'
    model = Menu
    fields = ['name', 'recipes', 'servings']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



