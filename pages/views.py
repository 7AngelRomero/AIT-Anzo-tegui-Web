from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomLoginForm
from model_poll.models import User, Rol, SiteContent

def home(request):
    # Obtener contenido dinámico
    home_images = SiteContent.objects.filter(content_type='HOME_IMAGE', is_active=True).order_by('order')
    carousel_slides = SiteContent.objects.filter(content_type='CAROUSEL_SLIDE', is_active=True).order_by('order')
    
    context = {
        'home_images': home_images,
        'carousel_slides': carousel_slides,
    }
    return render(request, 'pages/home.html', context)

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    # Obtener contenido dinámico
    about_images = SiteContent.objects.filter(content_type='ABOUT_IMAGE', is_active=True).order_by('order')
    live_stream = SiteContent.objects.filter(content_type='LIVE_STREAM', is_active=True).first()
    
    context = {
        'about_images': about_images,
        'live_stream': live_stream,
    }
    return render(request, 'pages/about.html', context)

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

@login_required
def profile(request):
    if request.method == 'POST':
        # Cambio de foto
        if 'profile_image' in request.FILES:
            request.user.profile_image = request.FILES['profile_image']
            request.user.save()
            messages.success(request, 'Foto de perfil actualizada exitosamente.')
            
        # Cambio de username
        new_username = request.POST.get('username')
        if new_username and new_username != request.user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Este nombre de usuario ya existe.')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Nombre de usuario actualizado exitosamente.')
                
        # Cambio de contraseña
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if old_password and new_password1 and new_password2:
            if new_password1 == new_password2:
                if request.user.check_password(old_password):
                    request.user.set_password(new_password1)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Contraseña cambiada exitosamente.')
                else:
                    messages.error(request, 'La contraseña actual es incorrecta.')
            else:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
        
        return redirect('profile')
    
    return render(request, 'pages/profile.html')

