from django.shortcuts import render, redirect
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

from .forms import *
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    if request.user.is_authenticated: 
        return HttpResponseRedirect(reverse('pet_shop:index'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        payload = {'login': 'success'}
    else:
        payload = {'login': 'fail'}
    return JsonResponse(payload)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('pet_shop:index'))


class UserCreate(CreateView):
    model = User
    template_name = 'account/signup.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        valid = super(UserCreate, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = form.save()
        user.set_password(password)
        user.save()
        auth.login(self.request, user)
        return valid

    def get_success_url(self):
        return reverse('pet_shop:index')


class PetDetail(DetailView):
    model = Pet
    template_name = 'pet_detail.html'
    context_object_name = 'pet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vaccine_record'] = Pet_Vaccine_Record.objects.filter(pet_id=self.kwargs['pk'])

        try:
            user_id = self.request.user.id
            Record.objects.get(user_id=user_id, pet_id=self.kwargs['pk'])
            context['is_favourite'] = True
        except Record.DoesNotExist:
            context['is_favourite'] = False
        
        context['user_id'] = User
        if User.is_staff:
            context['vaccine_type'] = Vaccine.objects.all()
            try:
                context['adopter'] = Adopters.objects.get(pet_id=self.kwargs['pk'])
            except:
                context['adopter'] = None
        print(context['pet'].adopt)
        return context

def index(request):
    type_list = Type.objects.all()
    color_list = Color.objects.all()
    context = {
        'type_list': type_list,
        'color_list': color_list
    }
    return render(request, 'index.html', context) 

def get_pet_list(request):
    types = request.GET.getlist('types[]', '')
    colors = request.GET.getlist('colors[]', '')
    if len(types) == 0 and len(colors) == 0:
        pet_list = Pet.objects.all().order_by('-update_date')
    elif len(colors) == 0:
        pet_list = Pet.objects.filter(type__in=types).order_by('-update_date')
    elif len(types) == 0:
        pet_list = Pet.objects.filter(color__in=colors).order_by('-update_date')
    else:
        pet_list = Pet.objects.filter(type__in=types, color__in=colors).order_by('-update_date')

    context = {
        'pet_list': pet_list
    }
    print(pet_list)
    data = {'rendered_table': render_to_string('card_table.html', context=context)}
    return JsonResponse(data)


def favourite(request):
    user_id = request.user.id
    records = Record.objects.values_list('pet_id').filter(user_id=user_id).order_by('-date')
    pet_list = Pet.objects.filter(pk__in=records)

    context = {
        'pet_list': pet_list
    }
    data = {
        'title': 'Favourite',
        'rendered_table': render_to_string('card_table.html', context=context)
    }
    return render(request, 'favourite.html', data) 
