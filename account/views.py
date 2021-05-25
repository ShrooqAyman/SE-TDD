from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email 
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate


# *****************register view class*****************************  
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
            messages.add_message(request,messages.ERROR,'please provide valid email')
            context ['has_error']=True

        if len(password)<8:
            messages.add_message(request,messages.ERROR,'your password less than 8 character')
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
        user.is_active = True
        user.save()
        
        messages.add_message(request,messages.SUCCESS,'user is created ')
        return redirect('register')

# *****************login view class***************************** 
class loginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.add_message(request, messages.ERROR,'Username is required')
            context['has_error'] = True

        if password == '':
            messages.add_message(request, messages.ERROR,'Password is required')
            context['has_error'] = True

        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'auth/login.html', status=401, context=context)


        login(request, user)
        return redirect('home')

# *****************home view class***************************** 
class homeView(View):
    def get(self,request):
        return render(request,'home.html')

# *****************logout view class***************************** 
class LogoutView(View):
    def post(self,request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'logout succesfully')
        return redirect('login')