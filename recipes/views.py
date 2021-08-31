from django.shortcuts import render
from django.views import generic
from recipes.models import Recipe

import json

# Create your views here.
class IndexView(generic.ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stepsAndIngredients'] = json.loads(context['recipe'].stepsAndIngredients)
        return context
