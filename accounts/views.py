from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView

from accounts.forms import RegisterForm

class CustomLoginView(LoginView):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

        return render(request, 'account/login.html', {'form': form})


class UserRegistrationView(CreateView):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
        else:
            return render(request, 'account/register.html', {'form': form})


class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'home.html')