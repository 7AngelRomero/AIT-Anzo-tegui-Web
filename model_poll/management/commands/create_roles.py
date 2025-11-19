from django.core.management.base import BaseCommand
from model_poll.models import Rol

class Command(BaseCommand):
    help = 'Crea los roles básicos del sistema'

    def handle(self, *args, **options):
        roles = [
            {'name': 'Administrador', 'descripcion': 'Control total del sistema'},
            {'name': 'Trabajador', 'descripcion': 'Gestión de encuestas'},
            {'name': 'Usuario', 'descripcion': 'Participación en encuestas'}
        ]
        
        for role_data in roles:
            role, created = Rol.objects.get_or_create(
                name=role_data['name'],
                defaults={'descripcion': role_data['descripcion']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Rol "{role.name}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Rol "{role.name}" ya existe')
                )