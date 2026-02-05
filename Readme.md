# AIT Anzoátegui - Portal Web Oficial

Portal web oficial de la Dirección de Automatización, Informática y Telecomunicaciones del Estado Anzoátegui, desarrollado con Django y Bootstrap 5.

## Descripción

Sitio web institucional que presenta los servicios, información y recursos de AIT Anzoátegui. Incluye sistema completo de encuestas interactivas, páginas informativas, panel de administración y generación de reportes PDF.

## Características Principales

- **Sistema de Encuestas Completo**: Creación, gestión y análisis de encuestas públicas
- **Tipos de Preguntas**: Texto libre, selección múltiple y escala numérica (1-5)
- **Roles de Usuario**: Administrador, Trabajador y Usuario con permisos específicos
- **Estadísticas Avanzadas**: Gráficas interactivas con Chart.js
- **Reportes PDF**: Exportación profesional con gráficas integradas
- **Panel de Administración**: Gestión completa de contenido y usuarios
- **Diseño Responsivo**: Interfaz adaptable con Bootstrap 5
- **Gestión de Contenido**: Imágenes dinámicas, carousel y transmisiones en vivo

## Tecnologías Utilizadas

- **Backend**: Django 5.x, Python 3.x
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Base de Datos**: MySQL (producción), SQLite (desarrollo)
- **Gráficas**: Chart.js, Matplotlib
- **PDF**: ReportLab
- **Autenticación**: Sistema de usuarios personalizado con roles
- **Fuentes**: Google Fonts (Noto Sans, Open Sans)
- **Iconos**: Font Awesome

## Estructura del Proyecto

```
ait_anzoategui/
├── model_poll/         # Modelos principales (8 tablas)
├── pages/              # App principal (home, about, contact)
├── posts/              # App de encuestas y gestión
├── static/             # Archivos estáticos (CSS, SVG, JS)
├── templates/          # Templates HTML
├── requirements.txt    # Dependencias del proyecto
└── manage.py          # Comando principal de Django
```

## Instalación y Configuración

1. **Clonar el repositorio**
```bash
git clone [URL_DEL_REPOSITORIO]
cd ait_anzoategui
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

## Sistema de Encuestas

### Tipos de Preguntas
- **Texto Libre**: Respuestas abiertas de los usuarios
- **Selección Múltiple**: Opciones predefinidas (radio buttons)
- **Escala Numérica**: Calificación del 1 al 5

### Roles y Permisos
- **Administrador**: Acceso completo, gestión de usuarios y encuestas
- **Trabajador**: Creación y edición de encuestas propias
- **Usuario**: Participación en encuestas públicas

### Funcionalidades
- Creación de encuestas con múltiples preguntas
- Gestión automática de estados (Borrador, Activa, Cerrada)
- Cierre automático por fecha de vencimiento
- Estadísticas en tiempo real con gráficas
- Exportación de reportes PDF profesionales

## Gestión de Contenido

- **Imágenes de Inicio**: Máximo 3 imágenes para la página principal
- **Imágenes Acerca de**: Máximo 3 imágenes para la página institucional
- **Carousel**: Slides dinámicos en la lista de encuestas
- **Transmisión en Vivo**: Integración con YouTube

## Reportes PDF

Cada encuesta puede generar un reporte profesional que incluye:
- Encabezado institucional oficial
- Información general de la encuesta
- Gráficas integradas (torta y barras)
- Respuestas individuales con datos del usuario
- Estadísticas detalladas por pregunta

## Configuración de Base de Datos

### MySQL (Producción)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ait_anzoategui',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

## Dependencias Principales

```
django>=5.0
reportlab>=3.6.0
pillow>=9.0.0
matplotlib>=3.5.0
mysqlclient>=2.1.0  # Para MySQL
```

## Diseño y Estilo

- **Colores Institucionales**: 
  - Azul principal: #184da1
  - Azul secundario: #2D64BB, #3498db
  - Verde: #27ae60
- **Tipografía**: 
  - Headers: Noto Sans
  - Contenido: Open Sans
- **Layout**: Diseño responsivo con contenedores personalizados

## Contacto y Redes Sociales

- **Email**: aitanzoátegui@gmail.com
- **Instagram**: [@aitanzoategui](https://www.instagram.com/aitanzoategui/)
- **Twitter/X**: [@aitanzoategui](https://x.com/aitanzoategui)
- **Dirección**: Av. 5 de Julio, Barcelona 6001, Anzoátegui - Venezuela

## Licencia

Proyecto desarrollado para la Gobernación del Estado Anzoátegui.

---

**Dirección de Automatización, Informática y Telecomunicaciones**  
**Estado Anzoátegui**  
*Impulsando la tecnología e innovación en Venezuela*