# AIT Anzoátegui - Portal Web Oficial

Portal web oficial de la Agencia de Innovación Tecnológica del Estado Anzoátegui, desarrollado con Django y Bootstrap 5.

## Descripción

Sitio web institucional que presenta los servicios, información y recursos de AIT Anzoátegui. Incluye sistema de encuestas interactivas, páginas informativas y panel de administración para la gestión de contenido.

## Características Principales

- **Diseño Responsivo**: Interfaz adaptable con Bootstrap 5
- **Sistema de Encuestas**: Creación y gestión de encuestas públicas
- **Panel de Administración**: Gestión de contenido para staff autorizado
- **Páginas Institucionales**: Home, Acerca de AIT, Contacto
- **Integración con Google Maps**: Ubicación de las oficinas
- **Redes Sociales**: Enlaces a Instagram y Twitter oficial

## Tecnologías Utilizadas

- **Backend**: Django 4.x
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Base de Datos**: SQLite (desarrollo)
- **Fuentes**: Google Fonts (Noto Sans, Open Sans)
- **Iconos**: Font Awesome, SVG personalizados

## Estructura del Proyecto

```
ait_anzoategui/
├── pages/              # App principal (home, about, contact)
├── posts/              # App de encuestas y polls
├── static/             # Archivos estáticos (CSS, SVG)
├── templates/          # Templates HTML
└── manage.py           # Comando principal de Django
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
```

3. **Instalar dependencias**
```bash
pip install django
```

4. **Ejecutar migraciones**
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

## Funcionalidades

### Páginas Públicas
- **Home**: Carousel informativo y contenido sobre tecnología en Venezuela
- **Acerca de AIT**: Misión, visión y información institucional
- **Contacto**: Formulario, mapa de ubicación y datos de contacto
- **Encuestas**: Lista de encuestas disponibles para participar

### Panel de Administración
- Gestión de encuestas y preguntas
- Control de acceso para staff autorizado
- Administración de contenido del sitio

### Sistema de Encuestas
- Creación de polls con múltiples preguntas
- Opciones de respuesta personalizables
- Visualización de resultados
- Interfaz intuitiva para participantes

## Diseño y Estilo

- **Colores Principales**: 
  - Azul institucional: #184da1
  - Azul secundario: #2D64BB, #3498db
  - Verde: #27ae60
- **Tipografía**: 
  - Headers: Noto Sans
  - Contenido: Open Sans
- **Layout**: Diseño alternado con contenedores personalizados (max-width: 1220px)

## Contacto y Redes Sociales

- **Email**: aitanzoátegui@gmail.com
- **Instagram**: [@aitanzoategui](https://www.instagram.com/aitanzoategui/)
- **Twitter/X**: [@aitanzoategui](https://x.com/aitanzoategui)
- **Dirección**: Av. 5 de Julio, Barcelona 6001, Anzoátegui - Venezuela

## Licencia

Proyecto desarrollado para la Gobernación del Estado Anzoátegui.

---

**Agencia de Innovación Tecnológica - Estado Anzoátegui**  
*Impulsando la tecnología e innovación en Venezuela*