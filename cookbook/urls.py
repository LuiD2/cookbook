"""zdcp_recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipes import views as recipe_views
from menus import views as menu_views
from cookbook import views as cookbook_views
from django.conf.urls import url, include

urlpatterns = [
    path('', cookbook_views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('cookbook/', cookbook_views.HomeView.as_view(), name='home'),
    path('cookbook/recipes', recipe_views.IndexView.as_view(), name='recipe_index'),
    path('cookbook/recipes/<int:pk>', recipe_views.DetailView.as_view(), name='recipe_detail'),
    path('cookbook/menus', menu_views.IndexView.as_view(), name='menu_index'),
    path('cookbook/menus/<int:pk>', menu_views.DetailView.as_view(), name='menu_detail'),
    path('cookbook/menus/<int:menuID>/recipes/<int:recipeID>', menu_views.MenuRecipeDetailView.as_view(), name='menu_recipe_detail'),
    path('cookbook/menus/addmenu', menu_views.MenuCreateView.as_view(), name='add_menu'),
    path('cookbook/menus/<int:menuID>/shop', menu_views.ShoppingDetailView.as_view(), name='shopping'),
    url(r'^', include('api.urls'))
]
