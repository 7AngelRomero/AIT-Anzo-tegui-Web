from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Avg, Q
from model_poll.models import Poll, Question, Options, Participation, QuestionDetails, User, Rol

@login_required
def poll_list(request):
    """Vista para mostrar todas las encuestas activas"""
    polls = Poll.objects.filter(status='ACTIVA').order_by('-star_date')
    return render(request, 'posts/poll_list.html', {'polls': polls})

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
        users = None
    
    return render(request, 'posts/poll_manager.html', {'polls': polls, 'users': users})

@login_required
def create_poll(request):
    """Vista para crear nueva encuesta - Solo Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para crear encuestas.")
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'BORRADOR')
        image = request.FILES.get('image')
        
        # Crear encuesta
        poll = Poll.objects.create(
            title=title,
            description=description,
            image=image,
            created_by=request.user,
            status=status
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
        if 'image' in request.FILES:
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
        return redirect('posts:poll_manager')
    
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
    return redirect('posts:poll_manager')

@login_required
def submit_poll(request, poll_id):
    """Vista para procesar las respuestas de la encuesta - Solo usuarios normales"""
    # Solo usuarios con rol 'Usuario' pueden responder encuestas
    if request.user.rol and request.user.rol.name != 'Usuario':
        messages.error(request, 'Solo los usuarios pueden responder encuestas.')
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
                if question.question_type == 'SELECCION_MULTIPLE':
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
    """Vista para mostrar resultados de encuesta - Solo Administradores y Trabajadores"""
    if not request.user.rol or request.user.rol.name not in ['Administrador', 'Trabajador']:
        return HttpResponseForbidden("No tienes permisos para ver resultados.")
    
    # Administrador: Puede ver resultados de cualquier encuesta
    if request.user.rol.name == 'Administrador':
        poll = get_object_or_404(Poll, id=poll_id)
    # Trabajador: Solo puede ver resultados de sus propias encuestas
    else:
        poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)
    
    # Calcular estadísticas
    total_participations = poll.participaciones.count()
    
    # Procesar resultados por pregunta
    for question in poll.preguntas.all():
        if question.question_type == 'SELECCION_MULTIPLE':
            # Calcular porcentajes para opciones
            for option in question.opciones.all():
                option.response_count = QuestionDetails.objects.filter(
                    question=question, 
                    selected_options=option
                ).count()
                option.percentage = (option.response_count / total_participations * 100) if total_participations > 0 else 0
        
        elif question.question_type == 'TEXTO_LIBRE':
            # Obtener respuestas de texto
            question.text_responses = QuestionDetails.objects.filter(
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
                # Asumir que las opciones de escala tienen valores 1-5
                ratings = []
                for response in responses:
                    try:
                        rating = int(response.selected_options.options_text)
                        ratings.append(rating)
                    except (ValueError, AttributeError):
                        pass
                
                question.average_rating = sum(ratings) / len(ratings) if ratings else 0
                question.rating_counts = [ratings.count(i) for i in range(1, 6)]
            else:
                question.average_rating = 0
                question.rating_counts = [0, 0, 0, 0, 0]
    
    context = {
        'poll': poll,
        'total_participations': total_participations,
    }
    
    return render(request, 'posts/poll_results.html', context)

@login_required
def delete_poll(request, poll_id):
    """Vista para eliminar encuesta - Solo Administradores"""
    if not request.user.rol or request.user.rol.name != 'Administrador':
        return HttpResponseForbidden("Solo los administradores pueden eliminar encuestas.")
    
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        poll_title = poll.title
        poll.delete()
        messages.success(request, f'Encuesta "{poll_title}" eliminada exitosamente.')
        return redirect('posts:poll_manager')
    
    return render(request, 'posts/confirm_delete.html', {'poll': poll})