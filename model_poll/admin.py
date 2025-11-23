from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Rol, Poll, Question, Options, Participation, QuestionDetails

# Configuración personalizada para el modelo User
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Campos editables en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('full_name', 'rol')}),
    )
    
    # Campos para crear nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('email', 'first_name', 'last_name', 'rol')}),
    )
    
    # Acciones personalizadas
    actions = ['reset_password', 'activate_users', 'deactivate_users', 'make_admin', 'make_worker', 'make_user']
    
    def reset_password(self, request, queryset):
        """Resetear contraseña a 'temporal123' para usuarios seleccionados"""
        count = 0
        for user in queryset:
            user.set_password('temporal123')
            user.save()
            count += 1
        self.message_user(request, f'{count} usuarios actualizados. Nueva contraseña: temporal123')
    reset_password.short_description = "🔑 Resetear contraseña a 'temporal123'"
    
    def activate_users(self, request, queryset):
        """Activar usuarios seleccionados"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} usuarios activados')
    activate_users.short_description = "✅ Activar usuarios"
    
    def deactivate_users(self, request, queryset):
        """Desactivar usuarios seleccionados"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} usuarios desactivados')
    deactivate_users.short_description = "❌ Desactivar usuarios"
    
    def make_admin(self, request, queryset):
        """Cambiar rol a Administrador"""
        admin_role, created = Rol.objects.get_or_create(name='Administrador')
        count = queryset.update(rol=admin_role)
        self.message_user(request, f'{count} usuarios cambiados a Administrador')
    make_admin.short_description = "👑 Hacer Administrador"
    
    def make_worker(self, request, queryset):
        """Cambiar rol a Trabajador"""
        worker_role, created = Rol.objects.get_or_create(name='Trabajador')
        count = queryset.update(rol=worker_role)
        self.message_user(request, f'{count} usuarios cambiados a Trabajador')
    make_worker.short_description = "👔 Hacer Trabajador"
    
    def make_user(self, request, queryset):
        """Cambiar rol a Usuario"""
        user_role, created = Rol.objects.get_or_create(name='Usuario')
        count = queryset.update(rol=user_role)
        self.message_user(request, f'{count} usuarios cambiados a Usuario')
    make_user.short_description = "👤 Hacer Usuario"

# Configuración para Roles
class RolAdmin(admin.ModelAdmin):
    list_display = ('name', 'descripcion', 'usuarios_count')
    search_fields = ('name',)
    
    def usuarios_count(self, obj):
        return obj.usuarios.count()
    usuarios_count.short_description = 'Usuarios'

# Configuración para Encuestas
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'star_date', 'questions_count', 'participations_count')
    list_filter = ('status', 'star_date', 'created_by')
    search_fields = ('title', 'description')
    ordering = ('-star_date',)
    
    def questions_count(self, obj):
        return obj.preguntas.count()
    questions_count.short_description = 'Preguntas'
    
    def participations_count(self, obj):
        return obj.participaciones.count()
    participations_count.short_description = 'Participaciones'

# Configuración para Preguntas
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'poll', 'question_type', 'is_obligatory', 'order')
    list_filter = ('question_type', 'is_obligatory', 'poll')
    search_fields = ('question_text', 'poll__title')
    ordering = ('poll', 'order')
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Pregunta'

# Registrar modelos en el admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Options)
admin.site.register(Participation)
admin.site.register(QuestionDetails)

# Personalizar títulos del admin
admin.site.site_header = "AIT Anzoátegui - Administración"
admin.site.site_title = "AIT Admin"
admin.site.index_title = "Panel de Administración"