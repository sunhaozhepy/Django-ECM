from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

def post_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'shopframe/post_list.html', {'animals': animals, 'equipements': equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    form = MoveForm()
    if form.is_valid():
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        ancien_lieu.disponibilite = "vacant"
        ancien_lieu.save()
        form.save()
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        nouveau_lieu.disponibilite = "occupied"
        nouveau_lieu.save()
        return redirect('animal_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        return render(request,
                  'shopframe/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})