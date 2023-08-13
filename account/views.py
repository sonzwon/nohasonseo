from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from account.forms import SignUpForm, LoginForm
from account.models import MyUser
from argon2 import PasswordHasher

def test(request):
    return render(request, 'account/test.html')


def home(request):
    return render(request, 'account/home.html')

def signup(request):
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = MyUser(
                email=form.email,
                name=form.name,
                password=form.password1)
            user.save()
            return redirect('account:login')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['remember_me'] = form.remember_me
            request.session.set_expiry(0)
            return render(request, "account/home.html", {'form': form})
    else: #GET
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('home')
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('home')