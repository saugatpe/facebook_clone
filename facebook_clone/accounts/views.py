from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

@login_required
def index(request):
    return render(request, 'accounts/index.html', {
        'username': request.user.username
    })

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'login_form': form})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already taken')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return HttpResponseRedirect(reverse("login"))
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'register_form': form})
