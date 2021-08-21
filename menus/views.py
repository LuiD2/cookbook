from django.shortcuts import render
from django.views import generic
from menus.models import Menu
from django.http import Http404
from menus.forms import ContactForm


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

class AddMenuView(generic.FormView):
    template_name = 'menus/add_menu.html'
    form_class = ContactForm
    success_url = '/cookbook/menus'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


