from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
# Model = table
class Type(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, help_text='Enter new pet type')
    description = models.CharField(max_length=300, help_text='Enter description')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Color(models.Model):
    color = models.CharField(max_length=30, unique=True, null=False, help_text='Enter color')

    class Meta:
        ordering = ['color']

    def __str__(self):
        return self.color

class Gender(models.Model):
    gender = models.CharField(max_length=10, unique=True, null=False, help_text='Enter gender')

    class Meta:
        ordering = ['gender']

    def __str__(self):
        return self.gender

class Pet(models.Model):
    name = models.CharField(max_length=30, null=False, help_text='Enter pet name', default='')
    birth = models.DateField(null=True, help_text='Enter pet birth')
    gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL, default='')
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=False, help_text='Enter pet weigth', default=0)
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL, default='')
    description = models.CharField(max_length=300, help_text='Enter description', default='')
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL, default='')
    create_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now_add=False, auto_now=True)  
    adopt = models.BooleanField(default=False)  
    image = models.ImageField(upload_to='images/', default='') 

    class Meta:
        ordering = ['name', '-update_date']

    def __str__(self):
        return f'{self.name}'

class Record(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    pet_id = models.ForeignKey(Pet, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['date']

class Vaccine(models.Model):
    name = models.CharField(max_length=30, null=False, help_text='Enter Vaccine name', default='')
    description = models.CharField(max_length=300, help_text='Enter description', default='')

    class Meta:
        ordering = ['pk']
    
    def __str__(self):
        return self.name

class Pet_Vaccine_Record(models.Model):
    pet_id = models.ForeignKey(Pet, null=True, on_delete=models.SET_NULL, default='')
    type = models.ForeignKey(Vaccine, null=True, on_delete=models.SET_NULL, default='')
    description = models.CharField(max_length=300, help_text='Enter description', default='')
    date = models.DateField(null=False, help_text='Enter Date')

    class Meta:
        ordering = ['pet_id']

class Adopters(models.Model):
    pet_id = models.ForeignKey(Pet, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, null=False, help_text='Enter Adopter name', default='')
    phone = models.CharField(max_length=30, null=False, help_text='Enter Phone', default='')
    adopt_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['name', '-adopt_date']
