from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return HttpResponse("Hello, world.")

def hello(request):
  return JsonResponse({'response_text':'Hello, world.'})
