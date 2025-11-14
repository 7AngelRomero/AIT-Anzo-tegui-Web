from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


### Tabla de Roles

class Rol(models.Model):
    name = models.CharField(max_length=25, unique=True, help_text="Adminitrador, Trabajador, Usuario")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


### Tabla de Usuarios 

# AbstractUser ya incluye: username, first_name, last_name, email, password, is_staff, is_active, etc.    
# Campo adicional para 'nombre_completo' según tu ERD, aunque Django prefiere first_name y last_name

class User(AbstractUser):

    full_name = models.CharField(max_length=255, blank=True)
        
    # Relación con el Rol
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios")

    def save(self, *args, **kwargs):
        # Opcional: Sincronizar nombre_completo con first_name y last_name
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
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

    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORRADOR)
    star_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True, help_text="Opcional: Dejar en blanco si no hay fecha límite")

    def __str__(self):
        return self.title 

### Tabla de Preguntas

class Question(models.Model):

    class QuestionType(models.TextChoices):
        TEXTO_LIBRE = 'TEXTO_LIBRE', 'Texto Libre'
        SELECCION_MULTIPLE = 'SELECCION_MULTIPLE', 'Selección Múltiple (Radio)'
        CASILLA_VERIFICACION = 'CASILLA_VERIFICACION', 'Casilla de Verificación (Checkbox)'
        ESCALA_NUMERICA = 'ESCALA_NUMERICA', 'Escala Numérica (1-5)'

    Poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="Preguntas")
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QuestionType.choices)
    is_obligatory = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Orden de las preguntas (0, 1, 2 ...)")

    class Meta:
        ordering = ['orden'] # Ordena las preguntas por defecto según el campo 'orden'

    def __str__(self):
        return f"{self.poll.title} - Pregunta {self.order}: {self.question_text[:30]}..."
    

### Tabla de las preguntas

class Options():
    
    Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="Opciones")
    options_text = models.CharField(max_length=255)
    value = models.IntegerField(null=True, blank=True, help_text="Valor numérico opcional para análisis")

    def __str__(self):
        return self.options_text
    

### Tabla de Respuestas y Participación

class Participation(models.Model):

    Poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="Participaciones")
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Participaciones")
    sent_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('encuesta', 'usuario')

    def __str__(self):
        return f"Participación de {self.user.username} en {self.poll.title}"


class QuestionDetails(models.model):

    Participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name="Respuestas")
    Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="Respuestas")
    selected_options = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True)

    class Meta:
        # Solo una respuesta por pregunta por participación
        unique_together = ('participacion', 'pregunta')

    def __str__(self):
        return f"Respuesta a Pregunta ID {self.question.id} (Participación ID {self.participation.id})"