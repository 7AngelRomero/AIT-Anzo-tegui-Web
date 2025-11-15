from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm
from model_poll.models import User, Rol

def home(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = CustomLoginForm()
    
    return render(request, 'pages/registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        terms = request.POST.get('terms')
        
        if not terms:
            messages.error(request, 'Debes aceptar los términos y condiciones')
            return render(request, 'pages/registration/register.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'pages/registration/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'pages/registration/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'pages/registration/register.html')
        
        # Crear usuario con rol de Usuario por defecto
        user_role, created = Rol.objects.get_or_create(name='Usuario')
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
            rol=user_role
        )
        
        messages.success(request, 'Usuario creado exitosamente. Puedes iniciar sesión.')
        return redirect('login')
    
    return render(request, 'pages/registration/register.html')

