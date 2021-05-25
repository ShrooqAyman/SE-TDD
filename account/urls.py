from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('register',views.RegisterationView.as_view() , name = 'register'),
    path('login',views.loginView.as_view() , name = 'login'),
    
    path('home',login_required(views.homeView.as_view() ), name = 'home'),
    path('logout',views.LogoutView.as_view() , name = 'logout'),
    
 ] 