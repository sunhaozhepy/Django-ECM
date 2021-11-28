from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

def post_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'shopframe/post_list.html', {'animals': animals, 'equipements': equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    form = MoveForm(request.POST, instance=animal)
    if form.is_valid():
        form.save(commit=False)
        if animal.lieu.disponibilite == "vacant" or animal.lieu.id_equip == "litter":
            animal.save()
            #nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if ancien_lieu.id_equip != "litter":
                ancien_lieu.disponibilite = "vacant"
                ancien_lieu.save()
            animal.lieu.disponibilite = "occupied"
            animal.save()
            if animal.lieu.id_equip == "nest":
                animal.etat = "asleep"
            elif animal.lieu.id_equip == "litter":
                animal.etat = "hungry"
            elif animal.lieu.id_equip == "manger":
                animal.etat = "bored"
            elif animal.lieu.id_equip == "roller":
                animal.etat = "tired"
            animal.save()
            return redirect('animal_detail', id_animal=id_animal)
        else :
            animal.lieu = ancien_lieu
            animal.save()
            return render(request,
                          'shopframe/animal_detail.html',
                          {'animal': animal, 'lieu': animal.lieu, 'form': form, 'message' : "le lieu indiqué n'est pas disponible"})
    else:
        form = MoveForm()
        return render(request,
                  'shopframe/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form, 'message' : 'indiquer un lieu'})
