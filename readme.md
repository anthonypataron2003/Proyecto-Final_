# 🍎 NutriScan Kids

> **Una plataforma integral para el análisis nutricional y seguimiento alimentario infantil**

[![Django](https://img.shields.io/badge/Django-5.2.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

---

## 📋 Descripción

NutriScan Kids es una aplicación web desarrollada en Django que permite realizar análisis nutricionales especializados para niños. La plataforma ofrece herramientas avanzadas para el seguimiento dietético, análisis de hábitos alimentarios y gestión de recursos nutricionales enfocados en la población infantil.

### ✨ Características Principales

- 🔐 **Sistema de Autenticación Personalizado**: Gestión segura de usuarios con roles específicos
- 👶 **Módulo Kids**: Gestión especializada de perfiles infantiles
- 📊 **Análisis Nutricional**: Herramientas avanzadas para evaluación dietética
- 📚 **Recursos Educativos**: Base de conocimientos nutricionales
- 🛡️ **Seguridad Integrada**: Módulo de seguridad robusto
- 📧 **Notificaciones por Email**: Sistema de comunicación automatizado
- 🌍 **Localización**: Configurado para español y zona horaria de Ecuador

---

## 👥 Equipo de Desarrollo

Este proyecto ha sido desarrollado por:

- **Hernan Sarango** - *Desarrollador Full-Stack*
- **Ayrton Oña** - *Desarrollador Full-Stack*

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/nutriscan-kids.git
   cd nutriscan-kids
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env en el directorio raíz
   cp .env.example .env
   
   # Editar .env con tus configuraciones
   ```

5. **Realizar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Recopilar archivos estáticos**
   ```bash
   python manage.py collectstatic
   ```

8. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

La aplicación estará disponible en `http://localhost:8000/`

---

## 🏗️ Estructura del Proyecto

```
NutriScan_Kids/
├── apps/
│   ├── security/          # Módulo de autenticación y seguridad
│   ├── Kids/              # Gestión de perfiles infantiles
│   ├── recursos/          # Recursos educativos y nutricionales
│   └── analisis/          # Herramientas de análisis nutricional
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── media/                 # Archivos multimedia subidos por usuarios
├── templates/             # Plantillas HTML
├── NutriScan_Kids/        # Configuración principal del proyecto
│   ├── settings.py        # Configuraciones del proyecto
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── manage.py             # Script de gestión de Django
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

---

## ⚙️ Configuración

### Variables de Entorno

Crear un archivo `.env` en el directorio raíz con las siguientes variables:

```env
# Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com

# Base de datos (si usas PostgreSQL en producción)
DB_NAME=nutriscan_kids
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
```

### Configuración de Email

El sistema está configurado para usar Gmail SMTP. Para configurar el envío de emails:

1. Habilitar autenticación de dos factores en tu cuenta de Gmail
2. Generar una contraseña de aplicación específica
3. Actualizar las variables `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD`

---

## 📚 Módulos del Sistema

### 🔐 Security
- Autenticación personalizada de usuarios
- Gestión de permisos y roles
- Sistema de recuperación de contraseñas

### 👶 Kids
- Registro y gestión de perfiles infantiles
- Seguimiento de datos antropométricos
- Historial médico y nutricional

### 📊 Análisis
- Evaluación nutricional automatizada
- Generación de reportes personalizados
- Comparación con estándares nutricionales

### 📚 Recursos
- Base de datos de alimentos
- Guías nutricionales
- Material educativo para padres

---

## 🛠️ Uso del Sistema

### Panel de Administración

Accede al panel de administración en `/admin/` con las credenciales de superusuario para:

- Gestionar usuarios y permisos
- Administrar contenido del sistema
- Monitorear estadísticas de uso
- Configurar parámetros del sistema

### Flujo de Usuario

1. **Registro/Login**: Los usuarios se registran o inician sesión
2. **Dashboard**: Panel principal con resumen de información
3. **Gestión de Perfiles**: Creación y edición de perfiles infantiles
4. **Análisis Nutricional**: Evaluación de dietas y hábitos alimentarios
5. **Recursos**: Acceso a material educativo y guías

---

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Ejecutar tests
python manage.py test

# Crear nueva migración
python manage.py makemigrations nombre_app

# Aplicar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py loaddata fixtures/sample_data.json

# Exportar datos
python manage.py dumpdata app_name --indent 2 > backup.json
```

### Estándares de Código

- Seguir PEP 8 para estilo de código Python
- Usar nombres descriptivos para variables y funciones
- Documentar funciones complejas
- Escribir tests para nuevas funcionalidades

---

## 🚀 Despliegue

### Producción

Para desplegar en producción:

1. **Configurar variables de entorno de producción**
2. **Usar una base de datos robusta** (PostgreSQL recomendado)
3. **Configurar servidor web** (Nginx + Gunicorn)
4. **Habilitar HTTPS**
5. **Configurar copias de seguridad automatizadas**

### Docker (Opcional)

```dockerfile
# Dockerfile básico
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "NutriScan_Kids.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 📞 Soporte

Para soporte técnico o consultas:

- **Email**: soporte@nutriscan-kids.com
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/nutriscan-kids/wiki)
- **Issues**: [Reportar problemas](https://github.com/tu-usuario/nutriscan-kids/issues)

### Contacto del Equipo de Desarrollo

- **Hernan Sarango** - [GitHub](https://github.com/hernan-sarango) | [Email](mailto:hernan.sarango@email.com)
- **Ayrton Oña** - [GitHub](https://github.com/ayrton-ona) | [Email](mailto:ayrton.ona@email.com)

---

## 🙏 Agradecimientos

- **Hernan Sarango** y **Ayrton Oña** - Desarrolladores principales del proyecto
- Equipo de desarrollo de Django
- Comunidad de desarrolladores Python
- Especialistas en nutrición infantil que colaboraron en el proyecto

---

**Desarrollado con ❤️ por Hernan Sarango y Ayrton Oña para el bienestar nutricional infantil**