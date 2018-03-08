from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def player_me_detail(request):
    return HttpResponse("Here is your response testing goat!")