from django.apps import AppConfig

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    
    def ready(self):
        from django.contrib import admin
        admin.site.site_header = 'Administración AIT Anzoátegui'
        admin.site.site_title = 'Admin AIT'
        admin.site.index_title = 'Panel de Control'