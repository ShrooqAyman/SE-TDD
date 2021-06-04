from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email 
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading

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

#**************************************************************

class ResstPasswordView(View):
    def get(self, request):
        return render(request, 'auth/resetpassword.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'auth/resetpassword.html')

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset your Password]'
            message = render_to_string('auth/reset-user-password.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0])
                                       }
                                       )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            EmailThread(email_message).start()

        messages.success(
            request, 'We have sent you an email with instructions on how to reset your password')
        return render(request, 'auth/request-reset-email.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password reset link, is invalid, please request a new one')
                return render(request, 'auth/resetpassword.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.success(
                request, 'Invalid link')
            return render(request, 'auth/resetpassword.html')

        return render(request, 'auth/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be at least 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords don`t match')
            context['has_error'] = True

        if context['has_error'] == True:
            return render(request, 'auth/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request, 'Password reset success, you can login with new password')

            return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')
            return render(request, 'auth/set-new-password.html', context)

        return render(request, 'auth/set-new-password.html', context)