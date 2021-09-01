from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from menus.models import Menu
from api.serializers import MenuSerializer

# Create your views here.
@csrf_exempt
def menu_api(request, id = 0):
    if request.method == 'GET':
        menus = Menu.objects.all()
        menus_serializer = MenuSerializer(menus, many=True)
        return JsonResponse(menus_serializer.data, safe=False)
    elif request.method == 'POST':
        menu_data = JSONParser().parse(request)
        menu_serializer = MenuSerializer(data=menu_data)

        if menu_serializer.is_valid():
            menu_serializer.save()
            return JsonResponse("Added Successfully", safe=False)

        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        menu_data = JSONParser().parse(request)
        menu = Menu.objects.get(MenuId=menu_data['MenuId'])
        menu_serializer = MenuSerializer(menu, data=menu_data)

        if menu_serializer.is_valid():
            menu_serializer.save()
            return JsonResponse("Updated successfully", safe=False)


