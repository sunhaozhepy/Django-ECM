from django.shortcuts import render
from .models import Equipement, Animal

def post_list(request):
    animals = Animal.objects.all()
    return render(request, 'shopframe/post_list.html', {'animals': animals})
