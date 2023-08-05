from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import *
from account.models import User

# Create your views here.
def test(request):
    return render(request, 'account/test.html')


def home(request):
    return render(request, 'account/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register_msg.html')
        return render(request, 'account/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            try:
                user = User.objects.get(email=email)
            except:
                raise ValueError('사용자를 찾을 수 없습니다.')
            else:
                if user.check_password(raw_password):
                    login(request, user)
                    request.session['remember_me'] = remember_me
                    return render(request, "account/home.html")
    else: #GET
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('account:home')
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')