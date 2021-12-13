from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Type)
admin.site.register(Pet)
admin.site.register(Record)
admin.site.register(Color)
admin.site.register(Gender)
admin.site.register(Pet_Vaccine_Record)
admin.site.register(Vaccine)
admin.site.register(Adopters)

