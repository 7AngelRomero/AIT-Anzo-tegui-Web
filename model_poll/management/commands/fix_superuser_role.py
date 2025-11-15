from django.core.management.base import BaseCommand
from model_poll.models import User, Rol

class Command(BaseCommand):
    help = 'Fuerza la actualización del rol de todos los superusuarios a Administrador'

    def handle(self, *args, **options):
        # Crear rol Administrador si no existe
        admin_role, created = Rol.objects.get_or_create(name='Administrador')
        
        # Actualizar TODOS los superusuarios
        superusers = User.objects.filter(is_superuser=True)
        updated_count = 0
        
        for user in superusers:
            old_role = user.rol.name if user.rol else 'Sin rol'
            user.rol = admin_role
            user.save()
            updated_count += 1
            self.stdout.write(f'Usuario: {user.username} - Rol anterior: {old_role} -> Nuevo rol: Administrador')
        
        self.stdout.write(
            self.style.SUCCESS(f'Se actualizaron {updated_count} superusuarios con rol Administrador')
        )