from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, password=password)
                    login(request, user)
                    messages.success(request,'you are now logged in.')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request,'you are registered successfully')
                    return redirect('login') 
        else:
            messages.error(request,'Password do not match')
            return redirect('register')
                   
    else:
        return render(request, 'accounts/register.html')

@login_required(login_url='login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
        'inquiries':user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return redirect('home')
