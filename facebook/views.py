from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenue sur ma première vue Django !")
