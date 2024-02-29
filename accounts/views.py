from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import JsonResponse
from .helpers import send_forget_password_mail
import uuid
from .models import Profile



# check if string is email
def is_email(string):
    if '@' in string:
        return True
    return False


def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get("full_name")
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            context = {
                "username": username,
                "email": email,
                "full_name": full_name,
                "contact": contact,
                "password1": password1,
                "password2": password2,
                "username_error": "User already exists"
            }
            return render(request, 'login.html', context=context)

        if password1 == password2:
            user = User(username=username, full_name=full_name, 
                        email=email, contact=contact)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('login')
    return render(request, 'login.html')

def login_view(request):
    user_is_authenticated = False
    button_text = "Login"
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        if is_email(username_or_email):
            username = User.objects.get(email=username_or_email).username
            user_exists = User.objects.filter(email=username_or_email).exists()
        else:
            user_exists = User.objects.filter(username=username_or_email).exists()
            username = username_or_email

        if not user_exists:
            print ("User does not exist")
            messages.error(request, 'User does not exist')
            context = {
                "username_or_email": username_or_email,
                "password": password,
                "error": "User does not exist"
            }
            return render(request, 'login.html', context)

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            context = {
                "username_or_email": username_or_email,
                "password": password,
                "pwerror": "Invalid Credentials"
            }
            return render(request, 'login.html', context)
        elif user.is_superuser and user.is_staff:
            login(request, user)
            return redirect("/admin/")
        elif user.is_user:  
             login(request, user)
             user_info = {
                "is_authenticated": True,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_admin": user.is_superuser,
                "is_customer": user.is_user,
                "role": "User"
            }
             request.session['user_info'] = user_info
             messages.success(request, 'Login Successful')
             return redirect("/")
    else:
        if request.user.is_authenticated:
            user_is_authenticated = True
            button_text = "Profile"
    return render(request, 'login.html', {'user_is_authenticated': user_is_authenticated, 'button_text': button_text})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')

def home(request):
    return render(request,'home.html')

def ChangePassword(request, token):
    try:
        profile_obj = Profile.objects.get(forget_password_token=token)
        user = profile_obj.user
        print("ya samma ta aaija")
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            ("Passowrd liyo ki nai")
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'change-password.html', {'token': token})
            print("herma hai")
            user.set_password(new_password)
            user.save()
            
            # Clear forget password token
            profile_obj.forget_password_token = ''
            profile_obj.save()
            
            messages.success(request, 'Password changed successfully. Please login with your new password.')
            return redirect('login')
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid token.')
        return redirect('/forget-password/')
    except Exception as e:
        messages.error(request, 'An error occurred.')
        print(e)
    
    return render(request, 'change-password.html', {'token': token})


def ForgetPassword(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'No user found with this username.')
                return redirect('/forget-password/')
            else:
                user_obj = User.objects.get(username=username)
                token = str(uuid.uuid4())
                profile_obj, created = Profile.objects.get_or_create(user=user_obj)
                print("yaha samma aayo hai")
                profile_obj.forget_password_token = token
                profile_obj.save()
                send_forget_password_mail(user_obj.email, token)
                return redirect('forget_Message')

        return render(request, 'forget-password.html')

def ForgetMessage(request):
    return render(request, 'forget-message.html')