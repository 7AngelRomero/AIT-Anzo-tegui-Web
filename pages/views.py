from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm

def home(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # Solo usuarios staff pueden acceder
                login(request, user)
                messages.success(request, 'Has iniciado sesión correctamente')
                return redirect('home')
            else:
                messages.error(request, 'No tienes permisos de administrador')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = CustomLoginForm()
    
    return render(request, 'pages/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')

