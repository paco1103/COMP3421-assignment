from django.conf.urls import include, url
from django.urls import path
from django.template import loader
from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import views_manager

app_name = 'pet_shop'
urlpatterns = [
    path('account/login', views.login, name='login'),
    path('account/logout', views.logout, name='logout'),
    path('account/signup', views.UserCreate.as_view(), name='signup'),

    
    path('pet/<int:pk>', views.PetDetail.as_view(), name='pet-detail'),
    path('index', views.index, name='index'),
    path('ajax_pet_table', views.get_pet_list, name='ajax-get-pet-list'),
    path('about', views.about, name='about'),

    #pet info
    path('manager/create_pet', views_manager.PetCreate.as_view(), name='pet-create'),
    path('manager/delete_pet/<int:pk>', views_manager.pet_delete, name='pet-delete'),
    path('ajax_pet_update', views_manager.get_pet_updat, name='ajax-pet-update'),

    #pet vaccine record
    path('ajax_pet_vaccine_create', views_manager.pet_vaccine_create, name='ajax-pet-vaccine-create'),
    path('ajax_pet_vaccine_delete', views_manager.pet_vaccine_delete, name='ajax-pet-vaccine-delete'),
    
    #vaccine
    path('ajax_vaccine_create', views_manager.vaccine_create, name='ajax-vaccine-create'),

    #favourite
    path('ajax_favourite', views_manager.ajax_favourite, name='ajax-favourite'),
    path('favourite', views.favourite, name='favourite'),
    
    #adopter
    path('ajax_adopter', views_manager.adopter, name='ajax-adopter'),

    
]
print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))