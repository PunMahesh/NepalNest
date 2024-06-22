from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .helpers import send_forget_password_mail
import uuid
from .models import Profile
from datetime import date
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.conf import settings
import os



def home(request):
    today = date.today()
    return render(request,'home.html',{'today':today})

# check if string is email
def is_email(string):
    if '@' in string:
        return True
    return False


def registration_view(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        print("Registration")
        # check if user exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            context = {
                "full_name": full_name,
                "email": email,
                "contact": contact,
                "password1": password1,
                "password2": password2,
            }
            return render(request, 'login.html', context=context)

        if password1 == password2:
            user = User(email=email, full_name=full_name, contact=contact)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('login')
    return render(request, 'login.html')

def login_view(request):
    user_is_authenticated = False
    button_text = "Login"
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

       # Check if a user with the given email exists
        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            messages.error(request, 'User does not exist')
            context = {
                "email": email,
                "password": password,
                "error": "User does not exist"
            }
            return render(request, 'login.html', context)

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            context = {
                "email": email,
                "password": password,
                "pwerror": "Invalid Credentials"
            }
            return render(request, 'login.html', context)
        elif user is not None and user.is_superuser:
            login(request, user)
            return redirect("/admin/")
        elif user is not None and user.is_user:  
             login(request, user)
             user_info = {
                "is_authenticated": True,
                "full_name": user.full_name,
                "contact": user.contact,
                "email": user.email,
                "is_admin": user.is_superuser,
                "is_user": user.is_user,
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
            email = request.POST.get('email')
            
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'No user found with this username.')
                return redirect('/forget-password/')
            else:
                user_obj = User.objects.get(email=email)
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        # Process profile update form data
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        
        # Update user profile
        user = request.user
        user.email = email
        user.full_name = full_name
        user.contact = contact
        user.address = address
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('update_profile')

    return render(request, 'my_account.html')

@login_required
def update_password(request):
    error_message = None  # Initialize error_message to None
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        # Check if the old password matches the password in the database
        if check_password(old_password, user.password):
            # Check if the new passwords match
            if new_password1 == new_password2:
                # Update the user's password
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('update_profile')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            # Set error_message for invalid old password
            error_message = 'Invalid old password.'

    # Pass error_message to the template context
    return render(request, 'my_account.html', {'error_message': error_message})

@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        
        # Check if a file was uploaded
        if profile_pic:
            # Define the directory where profile pictures will be stored
            profile_pic_dir = os.path.join(settings.MEDIA_ROOT, 'User_profile')
            
            # Save the uploaded file to the directory
            with open(os.path.join(profile_pic_dir, profile_pic.name), 'wb+') as destination:
                for chunk in profile_pic.chunks():
                    destination.write(chunk)
            
            # Update the user's profile picture field with the file path
            request.user.profile_pic = os.path.join('User_profile', profile_pic.name)
            request.user.save()
            
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('update_profile')
        else:
            messages.error(request, 'No file uploaded.')
    
    return render(request, 'my_account.html')