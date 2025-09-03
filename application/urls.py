from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('submissions/', views.submissions, name='submissions'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('starterpage.html', views.starterpage, name='starterpage'),
    path('contact.html', views.contact, name='contact'),
    path('form.html', views.form, name='form'),
    path('dashboard.html', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
