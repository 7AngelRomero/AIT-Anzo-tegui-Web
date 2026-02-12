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
    
    # Obtener todos los usuarios con estadísticas de participación
    users = User.objects.all().order_by('username')
    
    # Agregar estadísticas de participación a cada usuario
    for user in users:
        user.participation_count = Participation.objects.filter(user=user).count()
        user.last_participation = Participation.objects.filter(user=user).order_by('-sent_date').first()
    
    # Calcular estadísticas por rol
    admin_count = users.filter(rol__name='Administrador').count()
    worker_count = users.filter(rol__name='Trabajador').count()
    user_count = users.filter(Q(rol__name='Usuario') | Q(rol__isnull=True)).count()
    
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
def create_poll(request):
    """Vista para crear nueva encuesta - Solo Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para crear encuestas.")
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'BORRADOR')
        star_date = request.POST.get('star_date')
        end_date = request.POST.get('end_date')
        image = request.FILES.get('image')
        
        # Las fechas son opcionales ahora
        from django.utils import timezone
        if not star_date:
            star_date = timezone.now()
        if not end_date:
            star_date_obj = timezone.datetime.fromisoformat(star_date.replace('T', ' '))
            end_date = star_date_obj + timezone.timedelta(days=30)
        
        # Crear encuesta
        poll = Poll.objects.create(
            title=title,
            description=description,
            image=image,
            created_by=request.user,
            status=status,
            star_date=star_date,
            end_date=end_date
        )
        
        # Procesar preguntas
        question_order = 0
        for key, value in request.POST.items():
            if key.startswith('question_text_'):
                question_id = key.split('_')[-1]
                question_text = value
                question_type = request.POST.get(f'question_type_{question_id}')
                is_obligatory = request.POST.get(f'is_obligatory_{question_id}') == 'true'
                
                if question_text and question_type:
                    question = Question.objects.create(
                        poll=poll,
                        question_text=question_text,
                        question_type=question_type,
                        is_obligatory=is_obligatory,
                        order=question_order
                    )
                    question_order += 1
                    
                    # Procesar opciones según el tipo de pregunta
                    if question_type == 'SELECCION_MULTIPLE':
                        for option_key, option_value in request.POST.items():
                            if option_key.startswith(f'option_{question_id}_') and option_value:
                                Options.objects.create(
                                    question=question,
                                    options_text=option_value
                                )
                    elif question_type == 'ESCALA_NUMERICA':
                        # Crear opciones automáticamente para escala 1-5
                        for i in range(1, 6):
                            Options.objects.create(
                                question=question,
                                options_text=str(i),
                                value=i
                            )
        
        messages.success(request, 'Encuesta creada exitosamente con todas sus preguntas.')
        return redirect('posts:poll_manager')
    
    return render(request, 'posts/create_poll.html')

@login_required
def edit_poll(request, poll_id):
    """Vista para editar encuesta completa con preguntas y opciones"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para editar encuestas.")
    
    # Administrador: Puede editar cualquier encuesta
    if request.user.rol.name == 'Administrador':
        poll = get_object_or_404(Poll, id=poll_id)
    # Trabajador: Solo puede editar sus propias encuestas
    else:
        poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)
    
    if request.method == 'POST':
        # Actualizar datos básicos de la encuesta
        poll.title = request.POST.get('title')
        poll.description = request.POST.get('description')
        poll.status = request.POST.get('status')
        
        # Manejar imagen
        if request.POST.get('remove_image'):
            # Eliminar imagen existente
            if poll.image:
                poll.image.delete()
                poll.image = None
        elif 'image' in request.FILES:
            # Reemplazar con nueva imagen
            poll.image = request.FILES['image']
        
        poll.save()
        
        # Procesar eliminación de preguntas
        for key in request.POST.keys():
            if key.startswith('delete_question_'):
                question_id = key.split('_')[-1]
                try:
                    question = Question.objects.get(id=question_id, poll=poll)
                    question.delete()
                except Question.DoesNotExist:
                    pass
        
        # Procesar eliminación de opciones
        for key in request.POST.keys():
            if key.startswith('delete_option_'):
                parts = key.split('_')
                if len(parts) >= 4:
                    option_id = parts[-1]
                    try:
                        option = Options.objects.get(id=option_id)
                        option.delete()
                    except Options.DoesNotExist:
                        pass
        
        # Actualizar preguntas existentes
        for key, value in request.POST.items():
            if key.startswith('existing_question_text_'):
                question_id = key.split('_')[-1]
                try:
                    question = Question.objects.get(id=question_id, poll=poll)
                    question.question_text = value
                    question.question_type = request.POST.get(f'existing_question_type_{question_id}')
                    question.is_obligatory = request.POST.get(f'existing_is_obligatory_{question_id}') == 'true'
                    question.save()
                    
                    # Actualizar opciones existentes
                    for opt_key, opt_value in request.POST.items():
                        if opt_key.startswith(f'existing_option_text_{question_id}_'):
                            option_id = opt_key.split('_')[-1]
                            try:
                                option = Options.objects.get(id=option_id, question=question)
                                option.options_text = opt_value
                                option.save()
                            except Options.DoesNotExist:
                                pass
                    
                    # Agregar nuevas opciones a preguntas existentes
                    for new_opt_key, new_opt_value in request.POST.items():
                        if new_opt_key.startswith(f'new_existing_option_{question_id}_') and new_opt_value:
                            Options.objects.create(
                                question=question,
                                options_text=new_opt_value
                            )
                
                except Question.DoesNotExist:
                    pass
        
        # Procesar nuevas preguntas
        question_order = poll.preguntas.count()
        for key, value in request.POST.items():
            if key.startswith('new_question_text_'):
                question_id = key.split('_')[-1]
                question_text = value
                question_type = request.POST.get(f'new_question_type_{question_id}')
                is_obligatory = request.POST.get(f'new_is_obligatory_{question_id}') == 'true'
                
                if question_text and question_type:
                    question = Question.objects.create(
                        poll=poll,
                        question_text=question_text,
                        question_type=question_type,
                        is_obligatory=is_obligatory,
                        order=question_order
                    )
                    question_order += 1
                    
                    # Procesar opciones de nuevas preguntas
                    if question_type == 'SELECCION_MULTIPLE':
                        for option_key, option_value in request.POST.items():
                            if option_key.startswith(f'new_option_{question_id}_') and option_value:
                                Options.objects.create(
                                    question=question,
                                    options_text=option_value
                                )
                    elif question_type == 'ESCALA_NUMERICA':
                        # Crear opciones automáticamente para escala 1-5
                        for i in range(1, 6):
                            Options.objects.create(
                                question=question,
                                options_text=str(i),
                                value=i
                            )
        
        messages.success(request, 'Encuesta actualizada exitosamente con todas sus preguntas.')
        return redirect('posts:poll_manager')
    
    return render(request, 'posts/edit_poll.html', {'poll': poll})

@login_required
def change_user_role(request, user_id, new_role):
    """Vista para cambiar rol de usuario - Solo Administradores"""
    from django.http import JsonResponse
    
    if not request.user.rol or request.user.rol.name != 'Administrador':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'No tienes permisos para cambiar roles.'})
        return HttpResponseForbidden("No tienes permisos para cambiar roles.")
    
    user = get_object_or_404(User, id=user_id)
    
    # Evitar que los administradores se cambien el rol a sí mismos
    if user.id == request.user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'No puedes cambiar tu propio rol por seguridad.'})
        messages.error(request, 'No puedes cambiar tu propio rol por seguridad.')
        return redirect('posts:user_list')
    
    try:
        role = Rol.objects.get(name=new_role)
    except Rol.DoesNotExist:
        # Crear el rol si no existe
        role = Rol.objects.create(name=new_role, descripcion=f'Rol {new_role}')
    
    user.rol = role
    user.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'message': f'Rol de {user.username} cambiado a {new_role} exitosamente.',
            'user_id': user.id,
            'new_role': new_role
        })
    
    messages.success(request, f'Rol de {user.username} cambiado a {new_role} exitosamente.')
    return redirect('posts:user_list')

@login_required
def answer_poll(request, poll_id):
    """Vista para que usuarios y trabajadores respondan encuestas"""
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Verificar y actualizar estado si es necesario
    if poll.check_and_update_status():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse('<div class="alert alert-warning"><i class="fas fa-exclamation-triangle me-2"></i>Esta encuesta ha finalizado y ya no acepta respuestas.</div>')
        messages.error(request, 'Esta encuesta ha finalizado y ya no acepta respuestas.')
        return redirect('posts:poll_list')
    
    # Verificar que esté activa
    if poll.status != 'ACTIVA':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse('<div class="alert alert-warning"><i class="fas fa-exclamation-triangle me-2"></i>Esta encuesta no está disponible para responder.</div>')
        messages.error(request, 'Esta encuesta no está disponible para responder.')
        return redirect('posts:poll_list')
    
    # Verificar si ya participó
    if Participation.objects.filter(poll=poll, user=request.user).exists():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse('<div class="alert alert-info"><i class="fas fa-info-circle me-2"></i>Ya has participado en esta encuesta.</div>')
        messages.error(request, 'Ya has participado en esta encuesta.')
        return redirect('posts:poll_list')
    
    context = {
        'poll': poll,
    }
    
    # Si es petición AJAX, devolver solo el contenido del modal
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'posts/answer_poll_modal.html', context)
    
    return render(request, 'posts/answer_poll.html', context)

@login_required
def submit_poll(request, poll_id):
    """Vista para procesar las respuestas de la encuesta - Usuarios y Trabajadores"""
    # Usuarios y Trabajadores pueden responder encuestas
    if request.user.rol and request.user.rol.name == 'Administrador':
        messages.error(request, 'Los administradores no pueden responder encuestas.')
        return redirect('posts:poll_list')
    
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id, status='ACTIVA')
        
        # Verificar si el usuario ya participó
        if Participation.objects.filter(poll=poll, user=request.user).exists():
            messages.error(request, 'Ya has participado en esta encuesta.')
            return redirect('posts:poll_list')
        
        # Crear participación
        participation = Participation.objects.create(
            poll=poll,
            user=request.user
        )
        
        # Procesar cada pregunta
        for question in poll.preguntas.all():
            question_key = f'question_{question.id}'
            
            if question_key in request.POST:
                if question.question_type in ['SELECCION_MULTIPLE', 'ESCALA_NUMERICA']:
                    option_id = request.POST[question_key]
                    if option_id:
                        option = question.opciones.get(id=option_id)
                        QuestionDetails.objects.create(
                            participation=participation,
                            question=question,
                            selected_options=option
                        )
                
                elif question.question_type == 'TEXTO_LIBRE':
                    text_answer = request.POST[question_key]
                    if text_answer.strip():
                        QuestionDetails.objects.create(
                            participation=participation,
                            question=question,
                            answer_text=text_answer
                        )
        
        messages.success(request, '¡Gracias por participar en la encuesta!')
        return redirect('posts:poll_list')
    
    return redirect('posts:poll_detail', poll_id=poll_id)

@login_required
def poll_results(request, poll_id):
    """Vista para mostrar resultados de encuesta - Todos los usuarios pueden ver resultados de encuestas cerradas"""
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Solo administradores y trabajadores pueden ver resultados de encuestas activas
    if poll.status == 'ACTIVA' and (not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']):
        return HttpResponseForbidden("No tienes permisos para ver resultados de encuestas activas.")
    
    # Para encuestas cerradas, verificar permisos según el rol
    if poll.status == 'ACTIVA':
        # Administrador: Puede ver resultados de cualquier encuesta activa
        if request.user.rol.name == 'Administrador':
            pass  # Puede ver cualquier encuesta
        # Trabajador: Solo puede ver resultados de sus propias encuestas activas
        elif request.user.rol.name == 'Trabajador':
            if poll.created_by != request.user:
                return HttpResponseForbidden("Solo puedes ver resultados de tus propias encuestas activas.")
    # Las encuestas cerradas son públicas para todos los usuarios autenticados
    
    # Calcular estadísticas
    total_participations = poll.participaciones.count()
    
    # Crear lista de preguntas con sus resultados
    questions_with_results = []
    
    for question in Question.objects.filter(poll=poll).prefetch_related('opciones'):
        question_data = {
            'id': question.id,
            'text': question.question_text,
            'type': question.question_type,
            'options_list': [],
            'text_responses': [],
            'average_rating': 0,
            'rating_counts': [0, 0, 0, 0, 0]
        }
        
        if question.question_type == 'SELECCION_MULTIPLE':
            # Calcular porcentajes para opciones
            for option in question.opciones.all():
                count = QuestionDetails.objects.filter(
                    question=question,
                    selected_options=option
                ).count()
                percentage = (count / total_participations * 100) if total_participations > 0 else 0
                question_data['options_list'].append({
                    'text': option.options_text,
                    'count': count,
                    'percentage': percentage
                })
        
        elif question.question_type == 'TEXTO_LIBRE':
            # Obtener respuestas de texto
            question_data['text_responses'] = QuestionDetails.objects.filter(
                question=question,
                answer_text__isnull=False
            ).select_related('participation__user')
        
        elif question.question_type == 'ESCALA_NUMERICA':
            # Calcular promedio y distribución
            responses = QuestionDetails.objects.filter(
                question=question,
                selected_options__isnull=False
            )
            
            if responses.exists():
                ratings = []
                for response in responses:
                    try:
                        rating = int(response.selected_options.options_text)
                        ratings.append(rating)
                    except (ValueError, AttributeError):
                        pass
                
                question_data['average_rating'] = sum(ratings) / len(ratings) if ratings else 0
                question_data['rating_counts'] = [ratings.count(i) for i in range(1, 6)]
        
        questions_with_results.append(question_data)
    
    context = {
        'poll': poll,
        'total_participations': total_participations,
        'questions_with_results': questions_with_results,
    }
    
    # Si es una petición AJAX, devolver solo el contenido del modal
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'posts/poll_results_modal.html', context)
    
    return render(request, 'posts/poll_results_modal.html', context)

@login_required
def delete_poll(request, poll_id):
    """Vista para eliminar encuesta - Solo Administradores"""
    if not request.user.rol or request.user.rol.name != 'Administrador':
        return HttpResponseForbidden("Solo los administradores pueden eliminar encuestas.")
    
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        poll_title = poll.title
        poll.delete()
        
        # Si es petición AJAX, devolver respuesta JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'Encuesta "{poll_title}" eliminada exitosamente.'})
        
        messages.success(request, f'Encuesta "{poll_title}" eliminada exitosamente.')
        return redirect('posts:poll_manager')
    
    return HttpResponseForbidden("Método no permitido.")

@login_required
def content_manager(request):
    """Vista para gestionar contenido del sitio - Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para gestionar contenido.")
    
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        link_url = request.POST.get('link_url')
        image = request.FILES.get('image')
        
        # Validar límite de imágenes
        if content_type in ['HOME_IMAGE', 'ABOUT_IMAGE']:
            existing_count = SiteContent.objects.filter(content_type=content_type, is_active=True).count()
            if existing_count >= 3:
                messages.error(request, f'Solo se permiten máximo 3 imágenes para {"Inicio" if content_type == "HOME_IMAGE" else "Acerca de"}.')
                return redirect('posts:content_manager')
        
        # Validar límite de slides del carousel
        if content_type == 'CAROUSEL_SLIDE':
            existing_count = SiteContent.objects.filter(content_type=content_type, is_active=True).count()
            if existing_count >= 5:
                messages.error(request, 'Solo se permiten máximo 5 slides en el carousel.')
                return redirect('posts:content_manager')
            
            # Validar longitud de título y descripción para carousel
            if len(title) > 15:
                messages.error(request, 'El título del slide no puede exceder 15 caracteres.')
                return redirect('posts:content_manager')
            
            if description and len(description) > 50:
                messages.error(request, 'La descripción del slide no puede exceder 50 caracteres.')
                return redirect('posts:content_manager')
        
        # Procesar URL de YouTube si es transmisión en vivo
        if content_type == 'LIVE_STREAM' and link_url:
            # Convertir URL normal a embed si es necesario
            if 'watch?v=' in link_url:
                video_id = link_url.split('watch?v=')[1].split('&')[0]
                link_url = f'https://www.youtube.com/embed/{video_id}?autoplay=0&mute=0&controls=1&rel=0'
            elif 'embed/' in link_url and '?' not in link_url:
                # Agregar parámetros si no los tiene
                link_url += '?autoplay=0&mute=0&controls=1&rel=0'
        
        SiteContent.objects.create(
            content_type=content_type,
            title=title,
            description=description,
            link_url=link_url,
            image=image,
            created_by=request.user
        )
        
        messages.success(request, 'Contenido agregado exitosamente.')
        return redirect('posts:content_manager')
    
    # Obtener contenido por tipo
    home_images = SiteContent.objects.filter(content_type='HOME_IMAGE', is_active=True)
    about_images = SiteContent.objects.filter(content_type='ABOUT_IMAGE', is_active=True)
    carousel_slides = SiteContent.objects.filter(content_type='CAROUSEL_SLIDE', is_active=True)
    live_stream = SiteContent.objects.filter(content_type='LIVE_STREAM', is_active=True).first()
    
    context = {
        'home_images': home_images,
        'about_images': about_images,
        'carousel_slides': carousel_slides,
        'live_stream': live_stream,
    }
    
    return render(request, 'posts/content_manager.html', context)

@login_required
def delete_content(request, content_id):
    """Vista para eliminar contenido - Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para eliminar contenido.")
    
    try:
        content = SiteContent.objects.get(id=content_id)
        content_title = content.title
        content.delete()
        messages.success(request, f'Contenido "{content_title}" eliminado exitosamente.')
    except SiteContent.DoesNotExist:
        messages.error(request, 'El contenido que intentas eliminar no existe.')
    
    return redirect('posts:content_manager')

@login_required
def poll_statistics(request):
    """Vista para mostrar estadísticas de todas las encuestas creadas"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para ver estadísticas.")
    
    all_polls = Poll.objects.all().order_by('-star_date')
    
    # Crear diccionario con respuestas de texto libre y datos de gráficas
    text_responses = {}
    chart_data = {}
    for poll in all_polls:
        text_responses[poll.id] = {}
        chart_data[poll.id] = {}
        for question in poll.preguntas.all():
            if question.question_type == 'TEXTO_LIBRE':
                responses = QuestionDetails.objects.filter(
                    question=question,
                    answer_text__isnull=False,
                    answer_text__gt=''
                ).select_related('participation__user')
                text_responses[poll.id][question.id] = list(responses)
            
            elif question.question_type == 'SELECCION_MULTIPLE':
                labels = []
                data = []
                for option in question.opciones.all():
                    count = QuestionDetails.objects.filter(
                        question=question,
                        selected_options=option
                    ).count()
                    labels.append(option.options_text)
                    data.append(count)
                
                chart_data[poll.id][question.id] = {
                    'labels': labels,
                    'data': data,
                    'type': 'pie'
                }
            
            elif question.question_type == 'ESCALA_NUMERICA':
                labels = ['1', '2', '3', '4', '5']
                data = []
                
                for i in range(1, 6):
                    # Buscar por valor numérico primero
                    count = QuestionDetails.objects.filter(
                        question=question,
                        selected_options__value=i
                    ).count()
                    
                    # Si no hay resultados, buscar por texto (encuestas antiguas)
                    if count == 0:
                        count = QuestionDetails.objects.filter(
                            question=question,
                            selected_options__options_text=str(i)
                        ).count()
                    
                    data.append(count)
                
                chart_data[poll.id][question.id] = {
                    'labels': labels,
                    'data': data,
                    'type': 'bar'
                }
    
    context = {
        'all_polls': all_polls,
        'text_responses': text_responses,
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'posts/poll_statistics.html', context)

@login_required
def export_poll_pdf(request, poll_id):
    """Vista para exportar encuesta a PDF"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para exportar reportes.")
    
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Crear respuesta HTTP para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_{poll.title.replace(" ", "_")}.pdf"'
    
    # Crear documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30, alignment=TA_CENTER)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, spaceAfter=12, textColor=colors.HexColor('#184da1'))
    normal_style = styles['Normal']
    
    # Contenido del PDF
    story = []
    
    # Encabezado institucional mejorado
    header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=16, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=colors.HexColor('#184da1'))
    subheader_style = ParagraphStyle('SubHeader', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#666666'))
    
    story.append(Paragraph("REPÚBLICA BOLIVARIANA DE VENEZUELA", subheader_style))
    story.append(Paragraph("GOBERNACIÓN DEL ESTADO ANZOÁTEGUI", subheader_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("DIRECCIÓN DE AUTOMATIZACIÓN, INFORMÁTICA Y TELECOMUNICACIONES", header_style))
    story.append(Paragraph("(AIT ANZOÁTEGUI)", header_style))
    story.append(Spacer(1, 20))
    
    # Línea separadora
    line_data = [['', '']]
    line_table = Table(line_data, colWidths=[6*inch])
    line_table.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#184da1'))]))
    story.append(line_table)
    story.append(Spacer(1, 30))
    
    # Título del reporte
    story.append(Paragraph(f"REPORTE DE ENCUESTA: {poll.title.upper()}", title_style))
    story.append(Spacer(1, 20))
    
    # Información básica
    story.append(Paragraph("INFORMACIÓN GENERAL", heading_style))
    
    # Truncar descripción si es muy larga
    description = poll.description or 'Sin descripción'
    if len(description) > 100:
        description = description[:100] + '...'
    
    info_data = [
        ['Título:', poll.title],
        ['Descripción:', description],
        ['Estado:', poll.status],
        ['Fecha de inicio:', poll.star_date.strftime('%d/%m/%Y %H:%M') if poll.star_date else 'No definida'],
        ['Fecha de fin:', poll.end_date.strftime('%d/%m/%Y %H:%M') if poll.end_date else 'No definida'],
        ['Total participaciones:', str(poll.participaciones.count())],
        ['Fecha del reporte:', datetime.now().strftime('%d/%m/%Y %H:%M')]
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (1, 0), (1, -1), True)
    ]))
    story.append(info_table)
    story.append(Spacer(1, 30))
    
    # Preguntas y respuestas
    story.append(Paragraph("PREGUNTAS Y RESPUESTAS", heading_style))
    
    for i, question in enumerate(poll.preguntas.all(), 1):
        story.append(Paragraph(f"Pregunta {i}: {question.question_text}", ParagraphStyle('QuestionStyle', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold', spaceAfter=10)))
        story.append(Paragraph(f"Tipo: {question.get_question_type_display()}", normal_style))
        
        if question.question_type == 'TEXTO_LIBRE':
            responses = QuestionDetails.objects.filter(
                question=question,
                answer_text__isnull=False,
                answer_text__gt=''
            ).select_related('participation__user')
            
            if responses.exists():
                story.append(Paragraph("Respuestas:", ParagraphStyle('SubHeading', parent=styles['Normal'], fontName='Helvetica-Bold', spaceAfter=5)))
                for resp in responses:
                    story.append(Paragraph(f"• {resp.participation.user.username} ({resp.participation.sent_date.strftime('%d/%m/%Y %H:%M')}): {resp.answer_text}", normal_style))
            else:
                story.append(Paragraph("No hay respuestas", normal_style))
        
        elif question.question_type in ['SELECCION_MULTIPLE', 'ESCALA_NUMERICA']:
            # Generar gráfica
            chart_buffer = BytesIO()
            fig, ax = plt.subplots(figsize=(8, 6))
            
            if question.question_type == 'SELECCION_MULTIPLE':
                labels = []
                sizes = []
                colors_list = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                
                for option in question.opciones.all():
                    count = QuestionDetails.objects.filter(question=question, selected_options=option).count()
                    if count > 0:
                        labels.append(option.options_text)
                        sizes.append(count)
                
                if sizes:
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_list[:len(sizes)])
                    ax.set_title(f'Resultados: {question.question_text[:50]}...', fontsize=12, fontweight='bold')
                else:
                    ax.text(0.5, 0.5, 'Sin respuestas', ha='center', va='center', transform=ax.transAxes, fontsize=14)
                    ax.set_title(f'Resultados: {question.question_text[:50]}...', fontsize=12, fontweight='bold')
            
            elif question.question_type == 'ESCALA_NUMERICA':
                labels = ['1', '2', '3', '4', '5']
                values = []
                
                for i in range(1, 6):
                    count = QuestionDetails.objects.filter(question=question, selected_options__value=i).count()
                    if count == 0:
                        count = QuestionDetails.objects.filter(question=question, selected_options__options_text=str(i)).count()
                    values.append(count)
                
                ax.bar(labels, values, color='#36A2EB')
                ax.set_xlabel('Calificación')
                ax.set_ylabel('Número de respuestas')
                ax.set_title(f'Resultados: {question.question_text[:50]}...', fontsize=12, fontweight='bold')
                ax.set_ylim(0, max(values) + 1 if max(values) > 0 else 1)
            
            plt.tight_layout()
            plt.savefig(chart_buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            
            # Añadir gráfica al PDF
            chart_buffer.seek(0)
            chart_img = Image(chart_buffer, width=5*inch, height=3.75*inch)
            chart_img.hAlign = 'CENTER'
            story.append(chart_img)
            story.append(Spacer(1, 20))
            
            # Estadísticas de opciones
            stats_data = [['Opción', 'Respuestas', 'Porcentaje']]
            total_responses = QuestionDetails.objects.filter(question=question, selected_options__isnull=False).count()
            
            if question.question_type == 'SELECCION_MULTIPLE':
                for option in question.opciones.all():
                    count = QuestionDetails.objects.filter(question=question, selected_options=option).count()
                    percentage = (count / total_responses * 100) if total_responses > 0 else 0
                    stats_data.append([option.options_text, str(count), f"{percentage:.1f}%"])
            
            elif question.question_type == 'ESCALA_NUMERICA':
                for i in range(1, 6):
                    count = QuestionDetails.objects.filter(
                        question=question,
                        selected_options__value=i
                    ).count()
                    if count == 0:
                        count = QuestionDetails.objects.filter(
                            question=question,
                            selected_options__options_text=str(i)
                        ).count()
                    percentage = (count / total_responses * 100) if total_responses > 0 else 0
                    stats_data.append([f"Calificación {i}", str(count), f"{percentage:.1f}%"])
            
            if len(stats_data) > 1:
                stats_table = Table(stats_data, colWidths=[2*inch, 1*inch, 1*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#184da1')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_table)
            else:
                story.append(Paragraph("No hay respuestas", normal_style))
            
            # Respuestas individuales
            individual_responses = QuestionDetails.objects.filter(
                question=question,
                selected_options__isnull=False
            ).select_related('participation__user', 'selected_options')
            
            if individual_responses.exists():
                story.append(Paragraph("Respuestas individuales:", ParagraphStyle('SubHeading', parent=styles['Normal'], fontName='Helvetica-Bold', spaceAfter=5, spaceBefore=10)))
                for resp in individual_responses:
                    story.append(Paragraph(f"• {resp.participation.user.username} ({resp.participation.sent_date.strftime('%d/%m/%Y %H:%M')}): {resp.selected_options.options_text}", normal_style))
        
        story.append(Spacer(1, 20))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener contenido del buffer
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response