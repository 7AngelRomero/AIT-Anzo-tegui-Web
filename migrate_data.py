import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_base.settings')
django.setup()

from posts.models import Answer

# Eliminar todas las respuestas existentes para evitar conflictos
Answer.objects.all().delete()
print("Datos existentes eliminados. Ahora puedes hacer las migraciones.")