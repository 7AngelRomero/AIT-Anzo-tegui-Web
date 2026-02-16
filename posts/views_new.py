from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator
from model_poll.models import Poll, Question, Options, Participation, QuestionDetails, User, Rol, SiteContent
import json
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI

@login_required
def poll_list(request):
    """Vista para mostrar todas las encuestas"""
    # Verificar y actualizar estado de encuestas vencidas
    active_polls = Poll.objects.filter(status='ACTIVA')
    for poll in active_polls:
        poll.check_and_update_status()
    
    # Obtener todas las encuestas (activas y cerradas) excluyendo borradores
    polls = Poll.objects.exclude(status='BORRADOR').order_by('-star_date')
    
    # Obtener slides del carousel
    carousel_slides = SiteContent.objects.filter(content_type='CAROUSEL_SLIDE', is_active=True).order_by('order')
    
    context = {
        'polls': polls,
        'carousel_slides': carousel_slides,
    }
    
    return render(request, 'posts/poll_list.html', context)

@login_required
def poll_detail(request, poll_id):
    """Vista para mostrar una encuesta específica"""
    poll = get_object_or_404(Poll, id=poll_id, status='ACTIVA')
    return render(request, 'posts/poll_detail.html', {'poll': poll})

@login_required
def poll_manager(request):
    """Vista para gestión de encuestas y usuarios - Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    
    # Administrador: Ve todas las encuestas y puede CRUD completo
    if request.user.rol.name == 'Administrador':
        polls = Poll.objects.all().order_by('-star_date')
        users = User.objects.all().order_by('username')
        
        # Filtros de búsqueda para usuarios
        search_query = request.GET.get('search', '')
        role_filter = request.GET.get('role', '')
        
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if role_filter:
            users = users.filter(rol__name=role_filter)
            
    # Trabajador: Ve todas las encuestas pero solo puede editar las suyas
    else:
        polls = Poll.objects.all().order_by('-star_date')
        users = User.objects.all().order_by('username')
    
    # Verificar y actualizar encuestas vencidas
    for poll in polls.filter(status='ACTIVA'):
        poll.check_and_update_status()
    
    # Calcular estadísticas para el dashboard
    active_polls = polls.filter(status='ACTIVA').count()
    total_responses = Participation.objects.count()
    total_users = User.objects.count()
    
    context = {
        'polls': polls, 
        'users': users,
        'active_polls': active_polls,
        'total_responses': total_responses,
        'total_users': total_users
    }
    
    return render(request, 'posts/poll_manager.html', context)

@login_required
def user_list(request):
    """Vista para listado completo de usuarios - Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para ver el listado de usuarios.")
    
    # Obtener todos los usuarios
    users = User.objects.all().order_by('username')
    
    # Filtros de búsqueda
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        users = users.filter(
            Q(id__icontains=search_query) |
            Q(cedula__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(rol__name=role_filter)
    
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Calcular estadísticas por rol
    admin_count = User.objects.filter(rol__name='Administrador').count()
    worker_count = User.objects.filter(rol__name='Trabajador').count()
    user_count = User.objects.filter(Q(rol__name='Usuario') | Q(rol__isnull=True)).count()
    
    # Paginación - 15 usuarios por página
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'page_obj': page_obj,
        'admin_count': admin_count,
        'worker_count': worker_count,
        'user_count': user_count,
    }
    
    return render(request, 'posts/user_list.html', context)

@login_required
def manage_user(request, user_id):
    """Vista para gestionar usuario - Solo Administradores"""
    if not request.user.rol or request.user.rol.name != 'Administrador':
        return HttpResponseForbidden("No tienes permisos para gestionar usuarios.")
    
    usuario = get_object_or_404(User, id=user_id)
    
    # Evitar que el administrador se gestione a sí mismo
    if usuario.id == request.user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'No puedes gestionar tu propia cuenta.'})
        return HttpResponseForbidden("No puedes gestionar tu propia cuenta.")
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        usuario.cedula = request.POST.get('cedula', '')
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.first_name = request.POST.get('first_name', '')
        usuario.last_name = request.POST.get('last_name', '')
        
        # Actualizar rol
        role_name = request.POST.get('role')
        try:
            role = Rol.objects.get(name=role_name)
        except Rol.DoesNotExist:
            role = Rol.objects.create(name=role_name, descripcion=f'Rol {role_name}')
        usuario.rol = role
        
        # Actualizar permisos
        usuario.is_staff = request.POST.get('is_staff') == 'on'
        usuario.is_superuser = request.POST.get('is_superuser') == 'on'
        
        usuario.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario {usuario.username} actualizado exitosamente.'
        })
    
    # Si es petición AJAX, devolver el modal
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'posts/manage_user_modal.html', {'usuario': usuario})
    
    return HttpResponseForbidden("Método no permitido.")

@login_required
def toggle_user(request, user_id):
    """Vista para activar/desactivar usuario - Solo Administradores"""
    if not request.user.rol or request.user.rol.name != 'Administrador':
        return JsonResponse({'success': False, 'error': 'No tienes permisos.'})
    
    usuario = get_object_or_404(User, id=user_id)
    
    # Evitar que el administrador se desactive a sí mismo
    if usuario.id == request.user.id:
        return JsonResponse({'success': False, 'error': 'No puedes desactivar tu propia cuenta.'})
    
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        activate = data.get('activate', False)
        
        usuario.is_active = activate
        usuario.save()
        
        status = 'activado' if activate else 'desactivado'
        return JsonResponse({
            'success': True,
            'message': f'Usuario {usuario.username} {status} exitosamente.'
        })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})

@login_required
def delete_user(request, user_id):
    """Vista para eliminar usuario - Solo Administradores"""
    if not request.user.rol or request.user.rol.name != 'Administrador':
        return JsonResponse({'success': False, 'error': 'No tienes permisos.'})
    
    usuario = get_object_or_404(User, id=user_id)
    
    # Evitar que el administrador se elimine a sí mismo
    if usuario.id == request.user.id:
        return JsonResponse({'success': False, 'error': 'No puedes eliminar tu propia cuenta.'})
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario {username} eliminado permanentemente.'
        })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})
