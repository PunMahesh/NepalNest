from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import JsonResponse


# check if string is email
def is_email(string):
    if '@' in string:
        return True
    return False


def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            context = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "address": address,
                "contact": contact,
                "password1": password1,
                "password2": password2,
                "username_error": "User already exists"
            }
            return render(request, 'home.html', context=context)

        if password1 == password2:
            user = User(username=username, first_name=first_name, last_name=last_name,
                        email=email, address=address, contact=contact)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('home')
    return render(request, 'home.html')

def login_view(request):
    user_is_authenticated = False
    button_text = "Login"
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        if not username_or_email or not password:
            # messages.error(request, 'Please fill in all fields')
            # context = {
            #     "username_or_email": username_or_email,
            #     "password": password,
            #     "error": "Please fill in all fields"
            # }
            # return render(request, 'home.html', context)
            error_message = "Please fill in all fields"
            return JsonResponse({'error': error_message})

        if is_email(username_or_email):
            username = User.objects.get(email=username_or_email).username
            user_exists = User.objects.filter(email=username_or_email).exists()
        else:
            user_exists = User.objects.filter(username=username_or_email).exists()
            username = username_or_email

        if not user_exists:
            messages.error(request, 'User does not exist')
            context = {
                "username_or_email": username_or_email,
                "password": password,
                "error": "User does not exist"
            }
            return render(request, 'home.html', context)

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            context = {
                "username_or_email": username_or_email,
                "password": password,
                "pwerror": "Invalid Credentials"
            }
            return render(request, 'home.html', context)
        elif user.is_superuser and user.is_staff:
            login(request, user)
            return redirect("/admin/")
        elif user.is_user:  
             login(request, user)
            #  user_info = {
            #     "is_authenticated": True,
            #     "first_name": user.first_name,
            #     "last_name": user.last_name,
            #     "email": user.email,
            #     "is_admin": user.is_superuser,
            #     "is_customer": user.is_user,
            #     "role": "User"
            # }
            #  request.session['user_info'] = user_info
             messages.success(request, 'Login Successful')
             return redirect("/")
    else:
        if request.user.is_authenticated:
            user_is_authenticated = True
            button_text = "Profile"
    return render(request, 'home.html', {'user_is_authenticated': user_is_authenticated, 'button_text': button_text})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')

def home(request):
    return render(request,'home.html')