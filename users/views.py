from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
# from .models import User
from .forms import SignupForm, LoginForm


class Signup(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('main'))
        
        form = SignupForm()
        context = {
            'form': form,
            'title': 'User'
        }
        return render(request, 'users/signup.html', context)
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users:login')
        # TODO: 유효하지 않은 경우 사용자 알림
        print(form.errors)


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('main'))
        
        form = LoginForm()
        context = {
            'form': form,
            'title': 'User'
        }
        return render(request, 'users/login.html', context)
        
    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('main'))
        
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # True, False
            
            if user:
                login(request, user)
                return redirect(reverse('main'))
            
        # form.add_error(None, '아이디가 없습니다.')
        
        context = {
            'form': form
        }
        
        return render(request, 'users/login.html', context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('main'))