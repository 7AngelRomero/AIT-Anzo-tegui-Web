from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Poll, Response, Answer

def poll_list(request):
    """Vista para mostrar todas las encuestas activas"""
    polls = Poll.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'posts/poll_list.html', {'polls': polls})

def poll_detail(request, poll_id):
    """Vista para mostrar una encuesta específica"""
    poll = get_object_or_404(Poll, id=poll_id, is_active=True)
    return render(request, 'posts/poll_detail.html', {'poll': poll})

def submit_poll(request, poll_id):
    """Vista para procesar las respuestas de la encuesta"""
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id, is_active=True)
        
        # Crear una respuesta nueva
        response = Response.objects.create(
            poll=poll,
            user_ip=request.META.get('REMOTE_ADDR')
        )
        
        # Procesar cada pregunta
        for question in poll.questions.all():
            question_key = f'question_{question.id}'
            
            if question_key in request.POST:
                if question.question_type == 'multiple':
                    choice_id = request.POST[question_key]
                    if choice_id:
                        choice = question.choices.get(id=choice_id)
                        Answer.objects.create(
                            response=response,
                            question=question,
                            choice=choice
                        )
                
                elif question.question_type == 'text':
                    text_answer = request.POST[question_key]
                    if text_answer.strip():
                        Answer.objects.create(
                            response=response,
                            question=question,
                            text_answer=text_answer
                        )
                        
                elif question.question_type == 'rating':
                    rating = request.POST[question_key]
                    if rating:
                        Answer.objects.create(
                            response=response,
                            question=question,
                            rating=int(rating)
                        )
        
        messages.success(request, '¡Gracias por participar en la encuesta!')
        return redirect('poll_list')
    
    return redirect('poll_detail', poll_id=poll_id)