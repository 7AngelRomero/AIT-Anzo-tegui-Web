from django.core.management.base import BaseCommand
from model_poll.models import User, Rol

class Command(BaseCommand):
    help = 'Actualiza los roles de superusuarios existentes'

    def handle(self, *args, **options):
        # Crear rol Administrador si no existe
        admin_role, created = Rol.objects.get_or_create(name='Administrador')
        
        # Actualizar todos los superusuarios sin rol
        superusers = User.objects.filter(is_superuser=True, rol__isnull=True)
        updated_count = 0
        
        for user in superusers:
            user.rol = admin_role
            user.save()
            updated_count += 1
            self.stdout.write(f'Actualizado usuario: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Se actualizaron {updated_count} superusuarios con rol Administrador')
        )