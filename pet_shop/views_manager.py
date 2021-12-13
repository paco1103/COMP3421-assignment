from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.template.loader import render_to_string

import datetime

from .forms import *
from .models import *

class PetCreate(CreateView):
    model = Pet
    template_name = 'manager/pet_create.html'
    form_class = PetCreateForm

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        valid = super(PetCreate, self).form_valid(form)

        new_color = self.request.POST['new_color']
        new_type = self.request.POST['new_type']

        #will be clear while submit if not chose for new color or type  
        if new_color != '':
            new_obj = Color.objects.create(color=new_color)
            Pet.objects.filter(pk=self.object.id).update(color=new_obj.id)

        if new_type != '':
            new_obj = Type.objects.create(name=new_type)
            Pet.objects.filter(pk=self.object.id).update(type=new_obj.id)
        return valid

    def get_success_url(self):
        return reverse('pet_shop:pet-detail', kwargs={'pk': self.object.id})


def get_pet_updat(request):
    id = request.POST.get('id', '')
    text = request.POST.get('text', '')
    field = request.POST.get('field', '')

    Pet.objects.filter(id=id).update(**{field: text, 'update_date': datetime.datetime.now()})
    context = {
        'success': 'success'
    }
    return JsonResponse(context)


def pet_delete(request, pk):
    pet = Pet.objects.get(id=pk)
    pet.delete()
    pvr = Pet_Vaccine_Record.objects.filter(pet_id=pet)
    pvr.delete()
    return redirect('pet_shop:index')             # Finally, redirect to the homepage.


def pet_vaccine_create(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    description = request.POST.get('description', '')
    date = request.POST.get('date', '')

    pet = Pet.objects.get(pk=id)
    vaccine = Vaccine.objects.get(pk=type)

    pvr = Pet_Vaccine_Record(pet_id=pet, type=vaccine, description=description, date=date)
    pvr.save()
    
    context = {
        'id': pvr.pk,
        'success': 'success'
    }
    return JsonResponse(context)


def pet_vaccine_delete(request):
    id = request.POST.get('id', '')

    pvr = Pet_Vaccine_Record.objects.get(pk=id)
    pvr.delete()
    
    context = {
        'success': 'success'
    }
    return JsonResponse(context)


def vaccine_create(request):
    name = request.POST.get('name', '')

    vaccine = Vaccine(name=name)
    vaccine.save()
    
    context = {
        'id': vaccine.pk,
        'success': 'success'
    }
    return JsonResponse(context)


def ajax_favourite(request):
    pet_id = request.POST.get('pet_id', '')
    user_id = request.user.id
    is_already_favourite = False

    try:
        record = Record.objects.get(user_id=user_id, pet_id=pet_id)
        record.delete()
        is_already_favourite = True
    except Record.DoesNotExist:
        user = User.objects.get(id=user_id)
        pet = Pet.objects.get(pk=pet_id)
        record = Record(user_id=user, pet_id=pet)
        record.save()
        
    context = {
        'is_already_favourite': is_already_favourite
    }
    return JsonResponse(context)


def adopter(request):
    pet_id = request.POST.get('pet_id', '')
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    action = request.POST.get('action', '')
    
    if action == "create":
        Pet.objects.filter(pk=pet_id).update(adopt=True)
        pet = Pet.objects.get(pk=pet_id)
        adopter = Adopters(pet_id=pet, name=name, phone=phone)
        adopter.save()

    elif action == "update":
        adopter = Adopters.objects.filter(pet_id=pet_id).update(name=name, phone=phone)
        pet = Pet.objects.get(pk=pet_id)

    elif action == "delete":
        adopter = Adopters.objects.filter(pet_id=pet_id)
        adopter.delete()
        Pet.objects.filter(pk=pet_id).update(adopt=False)
        pet = Pet.objects.get(pk=pet_id)

    context = {
        'status': pet.adopt
    }
    return JsonResponse(context)
