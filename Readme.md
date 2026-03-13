# AIT Anzoátegui - Portal Web Oficial

Portal web oficial de la Agencia de Innovación Tecnológica del Estado Anzoátegui (Dirección de Automatización, Informática y Telecomunicaciones), desarrollado con Django 5 y Bootstrap 5.

## Descripción

Sitio web institucional que presenta los servicios, información y recursos de AIT Anzoátegui. Incluye sistema de encuestas interactivas con múltiples tipos de preguntas, panel de administración completo, gestión de usuarios con roles, sistema de respaldos de base de datos y generación de reportes en PDF.

## Características Principales

### Sistema de Encuestas
- **Tipos de preguntas**: Selección múltiple, Escala lineal (configurable), Calificación por estrellas (3-10)
- **Encuestas públicas e internas**: Control de visibilidad según rol
- **Programación de fechas**: Inicio y fin automático de encuestas
- **Estadísticas en tiempo real**: Gráficas interactivas con Chart.js
- **Exportación a PDF**: Reportes profesionales con gráficas incluidas

### Panel de Administración (Dashboard)
- **Gestión de encuestas**: Crear, editar, eliminar, programar
- **Gestión de usuarios**: Activar/desactivar, cambiar roles, eliminar
- **Estadísticas detalladas**: Filtros por título, autor, estado, fechas
- **Gestión de contenido**: Carousel, imágenes de inicio y acerca de
- **Sistema de respaldos**: Crear, descargar, subir y restaurar base de datos

### Sistema de Roles
- **Administrador**: Acceso completo, gestión de usuarios, encuestas públicas e internas
- **Trabajador**: Crear encuestas públicas, ver estadísticas públicas, gestionar usuarios (limitado)
- **Usuario**: Responder encuestas, ver resultados de encuestas cerradas

### Diseño y UX
- **Diseño responsivo**: Interfaz adaptable con Bootstrap 5
- **Notificaciones dinámicas**: Sistema de alertas animadas sin dependencias
- **Tema institucional**: Colores azul (#184da1, #2D64BB) y verde (#27ae60)
- **Sidebar fijo**: Navegación persistente en dashboard

## Tecnologías Utilizadas

### Backend
- **Django 5.x**: Framework web principal
- **Python 3.x**: Lenguaje de programación
- **MySQL/MariaDB**: Base de datos (MariaDB 10.5+ requerido)

### Frontend
- **Bootstrap 5**: Framework CSS
- **JavaScript Vanilla**: Sin dependencias de frameworks
- **Chart.js**: Gráficas interactivas (vía CDN)
- **Font Awesome 6**: Iconografía

### Librerías Python
- **Pillow**: Procesamiento de imágenes
- **ReportLab**: Generación de PDFs
- **Matplotlib**: Gráficas para reportes PDF
- **mysqlclient**: Conector MySQL/MariaDB

## Estructura del Proyecto

```
ait_anzoategui/
├── backups/                    # Respaldos de base de datos
├── django_base/                # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                      # Archivos subidos por usuarios
│   ├── content/
│   │   ├── carousel/          # Slides del carousel
│   │   ├── home/              # Imágenes de inicio
│   │   └── about/             # Imágenes de acerca de
│   ├── polls/                 # Imágenes de encuestas
│   └── profiles/              # Fotos de perfil
├── model_poll/                 # Modelos de datos
│   ├── models.py              # Base de datos: Poll, Question, Options, User, etc.
│   └── migrations/
├── pages/                      # App de páginas estáticas
│   ├── views.py               # Home, About, Contact
│   └── urls.py
├── posts/                      # App de encuestas y dashboard
│   ├── views.py               # Lógica de encuestas y gestión
│   ├── urls.py                # URLs públicas (/polls/)
│   └── dashboard_urls.py      # URLs de dashboard (/dashboard/)
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── styles.css         # Estilos personalizados
│   ├── js/
│   │   └── notifications.js   # Sistema de notificaciones
│   └── SVG/                   # Logos e iconos
├── templates/                  # Templates HTML
│   ├── pages/
│   │   ├── layouts/           # Layouts base
│   │   └── registration/      # Login, registro, etc.
│   └── posts/                 # Templates de encuestas
├── manage.py
├── requirements.txt
└── README.md
```

## Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MySQL/MariaDB 10.5 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd ait_anzoategui
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
Editar `django_base/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_base_datos',
        'USER': 'usuario_mysql',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

Acceder a: `http://localhost:8000`

## Funcionalidades Detalladas

### Páginas Públicas
- **Home** (`/`): Carousel informativo y contenido sobre tecnología
- **Acerca de AIT** (`/about/`): Misión, visión e información institucional
- **Contacto** (`/contact/`): Formulario, mapa y datos de contacto
- **Encuestas** (`/polls/`): Lista de encuestas disponibles
- **Resultados** (`/polls/<id>/results/`): Resultados de encuestas cerradas

### Panel de Administración (`/dashboard/`)
- **Home**: Vista general de encuestas con estadísticas resumidas
- **Usuarios**: Gestión completa de usuarios y roles
- **Crear Encuesta**: Formulario con múltiples tipos de preguntas
- **Estadísticas**: Gráficas y análisis detallado con filtros
- **Contenido**: Gestión de carousel e imágenes del sitio
- **Respaldos**: Crear, descargar, subir y restaurar base de datos

### Sistema de Encuestas

#### Tipos de Preguntas
1. **Selección Múltiple**: Radio buttons con opciones personalizables
2. **Escala Lineal**: Rango configurable (0-10 o 1-10) con etiquetas opcionales
3. **Calificación**: Estrellas configurables (3-10 estrellas)

#### Flujo de Encuesta
1. Crear encuesta con título, descripción e imagen
2. Agregar preguntas de diferentes tipos
3. Configurar fechas de inicio y fin
4. Publicar (cambiar estado a ACTIVA)
5. Usuarios responden
6. Ver estadísticas en tiempo real
7. Exportar reporte PDF

### Sistema de Respaldos

#### Funcionalidades
- **Descargar Respaldo**: Descarga inmediata del estado actual (no se guarda en servidor)
- **Crear y Guardar**: Crea respaldo y lo guarda en `/backups/` del servidor
- **Subir Respaldo**: Importar respaldo descargado previamente
- **Restaurar**: Cargar datos desde respaldo guardado
- **Eliminar**: Borrar respaldos del servidor

#### Formato
- Archivos JSON con formato legible
- Excluye datos temporales (sesiones, permisos)
- Nomenclatura: `backup_ait_YYYYMMDD_HHMMSS.json`

### Generación de Reportes PDF

#### Características
- Encabezado institucional con logo
- Información general de la encuesta
- Gráficas visuales para cada pregunta
- Tablas de estadísticas con porcentajes
- Formato profesional con fuente Helvetica
- Tamaños: Títulos 14pt, Cuerpo 12pt

## Diseño y Estilo

### Colores Institucionales
- **Azul Principal**: #184da1
- **Azul Secundario**: #2D64BB, #3498db
- **Verde**: #27ae60
- **Rojo**: #e74c3c
- **Naranja**: #f39c12

### Tipografía
- **Headers**: Noto Sans (400, 600, 700)
- **Contenido**: Open Sans (400, 600)
- **PDFs**: Helvetica

### Layout
- **Contenedores**: max-width 1220px
- **Sidebar Dashboard**: 280px fijo
- **Tablas**: Gradient header, striped, hover
- **Cards**: Border-radius 8px, shadow-sm

## Contacto y Redes Sociales

- **Email**: aitanzoátegui@gmail.com
- **Instagram**: [@aitanzoategui](https://www.instagram.com/aitanzoategui/)
- **Twitter/X**: [@aitanzoategui](https://x.com/aitanzoategui)
- **Dirección**: Av. 5 de Julio, Barcelona 6001, Anzoátegui - Venezuela
- **Horario**: 8:00 A.M - 5:00 P.M

## Comandos Útiles

### Desarrollo
```bash
# Ejecutar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic
```

### Respaldos
```bash
# Crear respaldo manual
python manage.py dumpdata --exclude contenttypes --exclude auth.permission --exclude sessions --indent 2 > backup.json

# Restaurar respaldo
python manage.py loaddata backup.json
```

### Base de Datos
```bash
# Acceder a shell de Django
python manage.py shell

# Acceder a base de datos
python manage.py dbshell
```

## Seguridad

- Autenticación requerida para todas las funcionalidades
- Control de acceso basado en roles
- Validación de permisos en cada vista
- Protección CSRF en formularios
- Sanitización de entradas de usuario
- Respaldos solo para Administradores

