# 🚀 Proyect‑IEEE Backend

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Django](https://img.shields.io/badge/Django-supported-green) ![Status](https://img.shields.io/badge/status-in%20development-yellow)

Backend del proyecto IEEE — API REST, autenticación y lógica de negocio. Esta documentación reúne guía rápida, instalación, API, contribución y ejemplos en un solo lugar, con iconos y estilo para que sea más agradable.

---

## 📚 Tabla de contenidos
- [Descripción](#-descripción)
- [Estado y composición](#-estado-y-composición)
- [Requisitos](#-requisitos)
- [Instalación rápida](#-instalación-rápida)
- [Configuración (.env)](#-configuración-env)
- [Ejecutar en desarrollo](#-ejecutar-en-desarrollo)
- [API (resumen)](#-api-resumen)
- [Ejemplos de uso](#-ejemplos-de-uso)
- [Tests y Calidad](#-tests-y-calidad)
- [Despliegue sugerido](#-despliegue-sugerido)
- [Contribuir](#-contribuir)
- [Licencia y contacto](#-licencia-y-contacto)

---

## ✨ Descripción
Este repositorio contiene el backend del proyecto IEEE, implementado con Django (Django REST Framework recomendado). Provee endpoints para autenticación, gestión de usuarios y recursos del proyecto. Diseñado para ser modular (apps/), configurable (config/) y fácil de desplegar.

---

## 📦 Estado y composición
Estructura detectada (top-level):
- `apps/` — apps Django del dominio
- `config/` — configuración del proyecto
- `manage.py` — comandos Django
- `requirements.txt` — dependencias
- `.gitignore`

Estado: En desarrollo — actualiza según avance del proyecto.

---

## 🛠 Requisitos
- Python 3.8+ (recomendado 3.10+)
- pip
- (Opcional) Docker y docker-compose
- Base de datos: PostgreSQL (recomendado para producción), SQLite para desarrollo

---

## 🚀 Instalación rápida (Local)
1. Clonar repo
```bash
git clone https://github.com/Rodrigo-Salva/Proyect-ieee-backend.git
cd Proyect-ieee-backend
```

2. Crear y activar entorno virtual
```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
- Copia el ejemplo y edita:
```bash
cp .env.example .env
# luego abre .env y completa valores
```

5. Migraciones y superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Ejecutar servidor
```bash
python manage.py runserver
```

---

## 🔑 Configuración (.env)
A continuación un ejemplo que puedes copiar a `.env`:

```env
# .env (ejemplo)
DJANGO_SECRET_KEY=changeme
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgres://user:password@localhost:5432/dbname

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=changeme

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

JWT_SECRET_KEY=changeme
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
```

⚠️ Nunca subas datos sensibles al repositorio. Usa secrets en CI/CD.

---

## 🧭 API (resumen)
Formato: JSON  
Autenticación: JWT (Bearer token) — ajusta si usas sesiones/cookies.

Rutas principales (actualiza según implementación real):

- Auth
  - POST /api/auth/login/ — Iniciar sesión → { access: "<token>" }
  - POST /api/auth/register/ — Crear cuenta
  - POST /api/auth/logout/ — Cerrar sesión / invalidar token

- Usuarios
  - GET /api/users/ — Listar (permiso)
  - GET /api/users/{id}/ — Detalle usuario
  - PATCH /api/users/{id}/ — Actualizar

- Recursos del proyecto (ejemplo: items)
  - GET /api/items/
  - POST /api/items/
  - GET /api/items/{id}/
  - PUT/PATCH /api/items/{id}/
  - DELETE /api/items/{id}/

Documentación interactiva (si está configurada):
- /swagger/  — Swagger UI
- /redoc/    — Redoc

> Sugerencia: Generar un archivo OpenAPI (YAML/JSON) mediante drf-spectacular o drf-yasg y enlazarlo aquí.

---

## 🔍 Ejemplos de uso (curl)

Login:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"miusuario","password":"miclave"}'
```

Llamada autenticada:
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## ✅ Tests y Calidad
- Ejecutar tests:
```bash
python manage.py test
# o
pytest
```

- Formato y lint:
  - Formatear con: `black .`
  - Ordenar imports: `isort .`
  - Lint: `flake8` o `ruff`

- CI sugerido: Pipeline en GitHub Actions con jobs para:
  - instalar dependencias
  - ejecutar linters
  - ejecutar tests
  - build (opcional)

---

## 🐳 Docker (sugerencia rápida)
Puedes añadir:
- `Dockerfile` para la app Django
- `docker-compose.yml` con servicios: web, db (postgres), redis

¿Quieres que genere un `Dockerfile` y `docker-compose.yml` configurados para este repo? Puedo hacerlo en el siguiente paso.

---

## 🤝 Contribuir
¡Gracias por querer colaborar! Sigue estos pasos:

1. Fork → Rama: `feature/xxx` o `fix/xxx`
2. Commits atómicos y descriptivos (usa Conventional Commits)
3. PR contra `main` con descripción y pasos para probar
4. Añade tests para cambios relevantes

Reglas rápidas:
- Formato: `black` + `isort`
- Escribe tests para nuevas rutas/funcionalidades
- Revisa que CI pase antes de merge

Ejemplo de mensaje de commit:
```
feat(auth): añadir endpoint login con JWT
```

---

## 📦 Flujo de despliegue (resumen)
Producción recomendada:
- Gunicorn como servidor WSGI
- Nginx como proxy y manejo de estáticos
- PostgreSQL como DB
- Redis para cache y celery (si aplica)
- HTTPS (Let's Encrypt)

---

## 🧾 Licencia y contacto
- Licencia: Añade la licencia (ej. MIT) en LICENSE
- Autor: Rodrigo‑Salva
- Contacto: rodrigodanielsalvasaccatoma@gmail.com

---
