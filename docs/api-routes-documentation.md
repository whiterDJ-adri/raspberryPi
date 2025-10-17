# 📋 Documentación Completa de API - Sistema de Monitoreo Raspberry Pi

## 🚀 Resumen Rápido

### Endpoints Principales

```bash
# Autenticación
POST /login/login          # Iniciar sesión
POST /login/signup         # Registrar usuario
GET  /login/logout         # Cerrar sesión

# Dashboard
GET  /dashboard/           # Panel usuario
GET  /dashboard/admin      # Panel administrador

# Gestión de Fotos
GET    /api/photo/         # Listar fotos
POST   /api/photo/         # Subir nueva foto
DELETE /api/photo/<id>     # Eliminar foto específica
GET    /api/photo/video    # Stream de video en vivo
```

### Configuración de Entorno Requerida

```env
URL_MONGO=mongodb://localhost:27017/security_camera
WEBHOOK_DISCORD=https://discord.com/api/webhooks/YOUR_WEBHOOK
SECRET_KEY=tu-clave-secreta-flask
```

---

## 🎯 Objetivo

Esta documentación detalla todos los endpoints, parámetros, respuestas y flujos de datos del sistema de cámara de seguridad Raspberry Pi, facilitando la integración y el desarrollo de nuevas funcionalidades.

## 🏗️ Estructura del Proyecto

Este proyecto es un sistema de monitoreo con cámara implementado en Flask, que incluye autenticación de usuarios, captura de fotos, streaming de video en tiempo real y notificaciones a Discord.

---

## 📁 Arquitectura de Archivos

### 🚀 Archivo Principal

- **`backend/api/app.py`** - Punto de entrada de la aplicación Flask

### 🛣️ Rutas (Routes)

- **`backend/api/routes/login.py`** - Manejo de autenticación
- **`backend/api/routes/dashboard.py`** - Panel de control de usuarios
- **`backend/api/routes/record_camera.py`** - Gestión de fotos y video

### 🎮 Controladores (Controllers)

- **`backend/api/controllers/login_bd.py`** - Lógica de base de datos para usuarios
- **`backend/api/controllers/record_camera_bd.py`** - Lógica de base de datos para fotos

### ⚙️ Servicios (Services)

- **`backend/api/services/video.py`** - Streaming de video en tiempo real
- **`backend/api/services/missatge_discord.py`** - Notificaciones a Discord

### 🔧 Utilidades

- **`backend/api/schemes.py`** - Validación de datos con Marshmallow
- **`backend/raspberry/main.py`** - Script de detección de movimiento para Raspberry Pi

---

## 🌐 Rutas de la API

### 🔐 Rutas de Autenticación (`/login`)

#### `GET /login/`

- **Función**: `show_page_login()`
- **Descripción**: Muestra la página de login
- **Comportamiento**:
  - Si el usuario ya está logueado, redirige al dashboard
  - Si no está logueado, muestra `login.html`
- **Respuesta**: Template HTML o redirection

#### `POST /login/login`

- **Función**: `login()`
- **Descripción**: Procesa el inicio de sesión
- **Parámetros JSON**:

  ```json
  {
   "email": "usuario@email.com",
   "password": "contraseña"
  }
  ```

- **Funcionalidad**:
  - Valida credenciales contra la base de datos
  - Crea sesión de usuario
  - Establece permisos de administrador si aplica
- **Respuestas**:
  - `200`: Login exitoso con redirection al dashboard
  - `401`: Credenciales inválidas

#### `POST /login/signup`

- **Función**: `signup()`
- **Descripción**: Registra un nuevo usuario
- **Parámetros JSON**:

  ```json
  {
   "name": "Nombre Usuario",
   "email": "usuario@email.com",
   "password": "contraseña123",
   "isAdmin": false
  }
  ```

- **Funcionalidad**:
  - Valida datos usando `user_schema`
  - Verifica que el usuario no exista
  - Crea nuevo usuario en base de datos
- **Respuestas**:
  - `201`: Usuario creado exitosamente
  - `400`: Usuario ya existe

#### `GET /login/logout`

- **Función**: `logout()`
- **Descripción**: Cierra la sesión del usuario
- **Funcionalidad**: Limpia la sesión y redirige al login
- **Respuesta**: JSON con redirection al login

#### `POST /login/delete`

- **Función**: `delete_use()`
- **Descripción**: Elimina un usuario
- **Parámetros JSON**:

  ```json
  {
   "email": "usuario@email.com"
  }
  ```

- **Respuesta**: `200` con mensaje de confirmación

#### `GET /login/users`

- **Función**: `get_all_users()`
- **Descripción**: Obtiene lista de todos los usuarios
- **Respuesta**: Array JSON con usuarios:

  ```json
  [
   {
    "name": "Nombre",
    "email": "email@example.com",
    "isAdmin": false
   }
  ]
  ```

---

### 📊 Rutas del Dashboard (`/dashboard`)

#### `GET /dashboard/`

- **Función**: `dashboard()`
- **Descripción**: Página principal del dashboard
- **Funcionalidad**:
  - Verifica que el usuario esté logueado
  - Redirige a admin dashboard si es administrador
  - Muestra dashboard de usuario normal
- **Plantillas**: `dashboard_user.html`

#### `GET /dashboard/admin`

- **Función**: `admin_dashboard()`
- **Descripción**: Panel de administración
- **Funcionalidad**:
  - Verifica autenticación y permisos de admin
  - Muestra interfaz de administrador
- **Plantillas**: `dashboard_admin.html`

---

### 📸 Rutas de Cámara (`/api/photo`)

#### `GET /api/photo/`

- **Función**: `obtener_foto()`
- **Descripción**: Obtiene lista de todas las fotos
- **Funcionalidad**: Consulta base de datos y retorna IDs de fotos
- **Respuesta**: `200` con array de fotos

#### `POST /api/photo/`

- **Función**: `add_foto()`
- **Descripción**: Sube una nueva foto
- **Parámetros Form-Data**:
  - `filename`: Nombre del archivo
  - `date`: Fecha de captura
  - `file`: Archivo de imagen
- **Funcionalidad**:
  - Guarda archivo en `media/screenshots/`
  - Registra en base de datos
  - Envía notificación a Discord
- **Respuesta**: `201` con confirmación

#### `GET /api/photo/<photo_id>`

- **Función**: `obtener_una_foto(photo_id)`
- **Descripción**: Obtiene una foto específica por ID
- **Respuesta**: `200` con datos de la foto

#### `DELETE /api/photo/<photo_id>`

- **Función**: `borrar_foto(photo_id)`
- **Descripción**: Elimina una foto específica
- **Respuestas**:
  - `200`: Foto eliminada
  - `404`: Foto no encontrada

#### `GET /api/photo/screenshots/<filename>`

- **Función**: `media(filename)`
- **Descripción**: Sirve archivos de imagen estáticos
- **Funcionalidad**: Devuelve archivos desde `media/screenshots/`

#### `GET /api/photo/video`

- **Función**: `real_streaming()`
- **Descripción**: Stream de video en tiempo real
- **Funcionalidad**:
  - Captura frames de la cámara continuamente
  - Devuelve stream MJPEG
- **Content-Type**: `multipart/x-mixed-replace; boundary=frame`

---

### 🏠 Ruta Principal (`/`)

#### `GET /`

- **Función**: `main()`
- **Descripción**: Página de inicio
- **Funcionalidad**:
  - Verifica autenticación
  - Redirige al login si no está logueado
  - Muestra página principal si está autenticado
- **Plantillas**: `index.html`

---

## 🗄️ Controladores de Base de Datos

### 👤 LoginController (`login_bd.py`)

#### `get_user(email)`

- **Descripción**: Busca un usuario por email
- **Parámetros**: `email` (string)
- **Retorna**: Documento de usuario o None

#### `create_user(user_data)`

- **Descripción**: Crea un nuevo usuario
- **Parámetros**: `user_data` (dict) - Datos validados del usuario
- **Funcionalidad**: Inserta documento en colección 'users'

#### `delete_user(email)`

- **Descripción**: Elimina un usuario por email
- **Parámetros**: `email` (string)
- **Funcionalidad**: Borra documento de la colección

#### `get_all_users()`

- **Descripción**: Obtiene todos los usuarios
- **Retorna**: Lista de usuarios sin campo `_id`

### 📷 RecordCameraController (`record_camera_bd.py`)

#### `get_one_photo(photo_id)`

- **Descripción**: Busca una foto por ID
- **Parámetros**: `photo_id` (string) - ObjectId de MongoDB
- **Retorna**: Cursor con la foto encontrada

#### `get_all_photos()`

- **Descripción**: Obtiene todas las fotos
- **Funcionalidad**:
  - Maneja errores de conexión a base de datos
  - Retorna solo los IDs para eficiencia
- **Respuestas**:
  - `200`: Lista de fotos
  - `503`: Error de conexión
  - `500`: Error de base de datos

#### `add_photo(data)`

- **Descripción**: Registra una nueva foto
- **Parámetros**: `data` (dict) - Datos validados de la foto
- **Retorna**: Mensaje de confirmación

#### `delete_photo(photo_id)`

- **Descripción**: Elimina registro de foto
- **Parámetros**: `photo_id` (string)
- **Respuestas**:
  - `200`: Foto eliminada
  - `404`: Foto no encontrada

---

## 🛠️ Servicios

### 📹 Servicio de Video (`video.py`)

#### `make_video()`

- **Descripción**: Generador de stream de video
- **Funcionalidad**:
  - Abre cámara (índice 1)
  - Captura frames continuamente
  - Codifica frames como JPEG
  - Genera stream MJPEG para el navegador
- **Formato**: Multipart stream con boundary 'frame'
- **Manejo de errores**: Logs detallados de estado de cámara

### 📢 Servicio Discord (`missatge_discord.py`)

#### `send_message(data)`

- **Descripción**: Envía notificaciones a Discord
- **Parámetros**:

  ```python
  {
    "date": "2025-10-16T15:30:00",  # ISO format
    "filename": "20251016_153000.jpg"
  }
  ```

- **Funcionalidad**:
  - Parsea fecha ISO y convierte a hora de Madrid
  - Formatea mensaje con fecha y nombre de archivo
  - Envía webhook a Discord
- **Variables de entorno**: `WEBHOOK_DISCORD`
- **Respuestas**:
  - `200/204`: Mensaje enviado
  - `RuntimeError`: Error en envío

---

## 📝 Esquemas de Validación (`schemes.py`)

### RecordCameraSchema

```python
{
  "filename": str (required),     # Nombre del archivo
  "date": str (required),         # Fecha en formato string
  "file_path": str (required)     # Ruta del archivo
}
```

### UserSchema

```python
{
  "name": str (optional, 1-100 chars),      # Nombre del usuario
  "email": str (required, valid email),     # Email válido
  "password": str (required, 8-24 chars),   # Contraseña
  "isAdmin": bool (required)                # Permisos de admin
}
```

---

## 🤖 Script Raspberry Pi (`main.py`)

### `take_photo(frame)`

- **Descripción**: Captura y envía foto al servidor
- **Parámetros**: `frame` - Frame de OpenCV
- **Funcionalidad**:
  - Genera nombre único con timestamp
  - Codifica frame como JPEG
  - Envía POST a `/api/photo/` con archivo y metadata
- **Formato fecha**: `YYYYMMDD_HHMMSS`

### Loop Principal de Detección

- **Funcionalidad**:
  - Captura 2 frames consecutivos
  - Calcula diferencia absoluta entre frames
  - Convierte a escala de grises para análisis
  - Detecta movimiento si promedio > 10
  - Limita a 5 fotos por minuto
  - Pausa 60 segundos después del límite
- **Variables**:
  - `max_photos = 5`: Límite de fotos
  - `average > 10`: Umbral de detección
  - `time.sleep(2)`: Intervalo entre captures

---

## 🔧 Configuración de la Aplicación (`app.py`)

### Configuración MongoDB

- **Variable**: `URL_MONGO` (environment variable)
- **Colecciones**: `users`, `record_camera`

### Internacionalización (i18n)

- **Idiomas soportados**: Español (`es`), Catalán (`ca`)
- **Zona horaria**: `Europe/Madrid`
- **Directorio**: `locales/`

### Blueprints Registrados

- `/api/photo` → `record_cam_bp`
- `/login` → `login_bp`
- `/dashboard` → `dashboard_bp`

### Configuración de Entorno del Servidor

- `URL_MONGO`: Conexión a MongoDB
- `WEBHOOK_DISCORD`: URL del webhook de Discord

---

## 🚦 Flujo de Trabajo Típico

1. **Usuario accede** → Redirigido a `/login/` si no autenticado
2. **Login/Signup** → Validación y creación de sesión
3. **Dashboard** → Interfaz diferenciada por rol (user/admin)
4. **Raspberry Pi** → Detección de movimiento automática
5. **Captura** → Foto guardada, registrada en BD, notificación Discord
6. **Visualización** → Stream en tiempo real disponible en `/api/photo/video`
7. **Gestión** → Admins pueden ver/eliminar fotos y usuarios

---

## 🆘 Mini-Manual de Errores Comunes

### Error 401 - No autorizado

```bash
# Problema: Token de sesión expirado o inválido
{
  "error": "No autorizado",
  "message": "Debes iniciar sesión"
}

# Solución:
curl -X POST http://localhost:5000/login/login \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "contraseña"}'
```

### Error 403 - Acceso denegado

```bash
# Problema: Usuario sin permisos de administrador
{
  "error": "Acceso denegado",
  "message": "Permisos insuficientes"
}

# Solución: Verificar rol de usuario en MongoDB
db.users.find({"username": "usuario"})
```

### Error 404 - Foto no encontrada

```bash
# Problema: ID de foto inexistente
{
  "error": "Foto no encontrada",
  "message": "La foto con ID 507f1f77bcf86cd799439011 no existe"
}

# Solución: Verificar IDs disponibles
curl http://localhost:5000/api/photo/
```

### Error 500 - Error del servidor

```bash
# Problema: Error en conexión a MongoDB o cámara
{
  "error": "Error interno del servidor",
  "message": "Error de conexión a la base de datos"
}

# Solución: Verificar servicios
# 1. MongoDB
sudo systemctl status mongod

# 2. Conexión de cámara
python -c "import cv2; cap = cv2.VideoCapture(0); print('Cámara OK' if cap.isOpened() else 'Error cámara')"

# 3. Variables de entorno
echo $URL_MONGO
```

### Problemas de Streaming

```bash
# Problema: Video stream no funciona
# Verificar cámara disponible
ls /dev/video*

# Probar captura directa
python -c "
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print('Stream OK' if ret else 'Error stream')
cap.release()
"

# Reiniciar servicio si es necesario
sudo systemctl restart tu-servicio-camera
```

### Debugging de Discord Webhook

```bash
# Problema: Notificaciones no llegan a Discord
# Probar webhook manualmente
curl -X POST $WEBHOOK_DISCORD \
  -H "Content-Type: application/json" \
  -d '{"content": "Test desde API"}'

# Verificar logs de la aplicación
tail -f app.log | grep -i discord
```

---

## 📞 Soporte y Contacto

Para problemas adicionales:

1. **Logs de aplicación**: Revisar `app.log` en el directorio del proyecto
2. **Logs del sistema**: `journalctl -u tu-servicio -f`
3. **Estado de servicios**: `systemctl status mongod nginx`
4. **Diagnóstico de red**: `netstat -tlnp | grep :5000`

## 🔗 Referencias Adicionales

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook)

## 🛡️ Seguridad

- **Autenticación por sesión**: Verificación en rutas protegidas
- **Validación de datos**: Esquemas Marshmallow
- **Separación de roles**: Dashboard diferente para admins
- **Variables de entorno**: Credenciales sensibles externalizadas
