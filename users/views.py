from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegisterFrorm
from django.contrib import messages

# Create your views here.

def sign_up(request):
    form = CustomRegisterFrorm
    if request.method == 'GET':
        form = CustomRegisterFrorm()
    else:
        form = CustomRegisterFrorm(request.POST)
        if(form.is_valid()):
            print(form.cleaned_data)
            form.save()
    return render(request,'registration/register.html',{"form":form})

def sign_in(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('sign_in')
    return render(request,'registration/signin.html')

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign_in')