from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


### Tabla de Roles

class Rol(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Administrador, Trabajador, Usuario")
    descripcion = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name


### Tabla de Usuarios 

# AbstractUser ya incluye: username, first_name, last_name, email, password, is_staff, is_active, etc.    
# Campo adicional para 'nombre_completo' según tu ERD, aunque Django prefiere first_name y last_name

class User(AbstractUser):

    full_name = models.CharField(max_length=255, blank=True, default='')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
        
    # Relación con el Rol
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios")

    def save(self, *args, **kwargs):
        # Opcional: Sincronizar nombre_completo con first_name y last_name
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        
        # Asignar rol según tipo de usuario
        if not self.rol:
            if self.is_superuser or self.is_staff:
                # Superusuarios y staff tienen rol de Administrador
                admin_role, created = Rol.objects.get_or_create(name='Administrador')
                self.rol = admin_role
            else:
                # Usuarios normales tienen rol de Usuario
                user_role, created = Rol.objects.get_or_create(name='Usuario')
                self.rol = user_role
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

### Tabla de Encuestas

class Poll(models.Model):

    class Status(models.TextChoices):
        BORRADOR = 'BORRADOR', 'Borrador'
        ACTIVA = 'ACTIVA', 'Activa'
        CERRADA = 'CERRADA', 'Cerrada'
        
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="encuestas_creadas")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='polls/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORRADOR)
    star_date = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora de inicio de la encuesta")
    end_date = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora de finalización de la encuesta")

    def check_and_update_status(self):
        """Verifica y actualiza el estado de la encuesta según las fechas"""
        from django.utils import timezone
        now = timezone.now()
        
        if self.end_date and now > self.end_date and self.status == 'ACTIVA':
            self.status = 'CERRADA'
            self.save(update_fields=['status'])
            return True
        return False
    
    def __str__(self):
        return self.title 

### Tabla de Preguntas

class Question(models.Model):

    class QuestionType(models.TextChoices):
        TEXTO_LIBRE = 'TEXTO_LIBRE', 'Texto Libre'
        SELECCION_MULTIPLE = 'SELECCION_MULTIPLE', 'Selección Múltiple (Radio)'
        CASILLA_VERIFICACION = 'CASILLA_VERIFICACION', 'Casilla de Verificación (Checkbox)'
        ESCALA_NUMERICA = 'ESCALA_NUMERICA', 'Escala Numérica (1-5)'

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="preguntas")
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QuestionType.choices)
    is_obligatory = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Orden de las preguntas (0, 1, 2 ...)")

    class Meta:
        ordering = ['order'] # Ordena las preguntas por defecto según el campo 'order'

    def __str__(self):
        return f"{self.poll.title} - Pregunta {self.order}: {self.question_text[:30]}..."
    

### Tabla de las opciones

class Options(models.Model):
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="opciones")
    options_text = models.CharField(max_length=255)
    value = models.IntegerField(null=True, blank=True, help_text="Valor numérico opcional para análisis")

    def __str__(self):
        return self.options_text
    

### Tabla de Respuestas y Participación

class Participation(models.Model):

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="participaciones")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participaciones")
    sent_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')

    def __str__(self):
        return f"Participación de {self.user.username} en {self.poll.title}"


class QuestionDetails(models.Model):

    participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name="respuestas")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="respuestas")
    selected_options = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True, default='')

    class Meta:
        # Solo una respuesta por pregunta por participación
        unique_together = ('participation', 'question')

    def __str__(self):
        return f"Respuesta a Pregunta ID {self.question.id} (Participación ID {self.participation.id})"


### Tabla de Contenido Dinámico

class SiteContent(models.Model):
    
    class ContentType(models.TextChoices):
        HOME_IMAGE = 'HOME_IMAGE', 'Imagen de Inicio'
        ABOUT_IMAGE = 'ABOUT_IMAGE', 'Imagen de Acerca de'
        CAROUSEL_SLIDE = 'CAROUSEL_SLIDE', 'Slide del Carousel'
        LIVE_STREAM = 'LIVE_STREAM', 'Enlace de Transmisión en Vivo'
    
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    title = models.CharField(max_length=200, help_text="Título o descripción del contenido")
    image = models.ImageField(upload_to='content/', blank=True, null=True)
    link_url = models.URLField(blank=True, null=True, help_text="URL de redirección (opcional)")
    description = models.TextField(blank=True, null=True, help_text="Descripción adicional")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['content_type', 'order']
        verbose_name = 'Contenido del Sitio'
        verbose_name_plural = 'Contenidos del Sitio'
    
    def __str__(self):
        return f"{self.get_content_type_display()} - {self.title}"