from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email 
from django.contrib.auth.models import User
# Create your views here.

class RegisterationView(View):
    def get( self , request):
        return render (request , 'auth/register.html')
    def post( self , request):
        context = {
        'data' : request.POST,
        'has_error':False
        }

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not validate_email(email):
            messages.add_message(request,messages.ERROR,'please provide valid email ')
            context ['has_error']=True

        if len(password)<8:
            messages.add_message(request,messages.ERROR,'your password less than 8 character  ')
            context ['has_error']=True

        if password != password2:
            messages.add_message(request,messages.ERROR,'your passwords does not match  ')
            context ['has_error']=True
        try:

           if User.objects.get(email=email):

               messages.add_message(request,messages.ERROR,'email is taken ')
               context ['has_error']=True
        except Exception as identifier:
            pass

        try:

           if User.objects.get(username=username):

               messages.add_message(request,messages.ERROR,'username is taken ')
               context ['has_error']=True
        except Exception as identifier:
            pass


        
        if context ['has_error']:

            return render (request , 'auth/register.html',context)

        user =User.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        messages.add_message(request,messages.SUCCESS,'username is created ')
        return redirect('register')
# Create your views here.
