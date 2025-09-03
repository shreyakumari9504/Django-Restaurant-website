from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('', views.home ,name='home'),
    path('starterpage.html', views.starterpage ,name='starterpage'),
    path('contact.html', views.contact ,name='contact'),
    path('form.html', views.form ,name='form'),
]