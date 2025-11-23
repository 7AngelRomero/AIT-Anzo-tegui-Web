from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from django.http import JsonResponse

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pages/registration/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Verificar si la nueva contraseña es igual a la actual
        user = form.user
        new_password = form.cleaned_data['new_password1']
        
        if user.check_password(new_password):
            # Usar el sistema de notificaciones React
            messages.error(self.request, 'La nueva contraseña no puede ser igual a la contraseña actual.')
            return self.form_invalid(form)
        
        # Si todo está bien, proceder con el cambio
        response = super().form_valid(form)
        # Agregar mensaje de éxito para mostrar en login
        messages.success(self.request, '¡Contraseña cambiada exitosamente! Ya puedes iniciar sesión con tu nueva contraseña.')
        return response
    
    def form_invalid(self, form):
        # Agregar mensajes de error específicos usando el sistema React
        for field, errors in form.errors.items():
            for error in errors:
                if 'password' in field:
                    if 'similar' in error.lower():
                        messages.error(self.request, 'La contraseña es muy similar a tu información personal.')
                    elif 'common' in error.lower():
                        messages.error(self.request, 'Esta contraseña es muy común. Elige una más segura.')
                    elif 'short' in error.lower():
                        messages.error(self.request, 'La contraseña debe tener al menos 8 caracteres.')
                    elif 'numeric' in error.lower():
                        messages.error(self.request, 'La contraseña no puede ser completamente numérica.')
                    elif 'match' in error.lower():
                        messages.error(self.request, 'Las contraseñas no coinciden.')
                    else:
                        messages.error(self.request, f'Error en contraseña: {error}')
                else:
                    messages.error(self.request, f'Error: {error}')
        
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar mensajes para React
        django_messages = []
        for message in messages.get_messages(self.request):
            django_messages.append({
                'message': str(message),
                'type': message.tags
            })
        context['react_messages'] = django_messages
        return context