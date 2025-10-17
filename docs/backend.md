# 🛠️ Guía Completa del Backend - Sistema de Cámara de Seguridad Raspberry Pi

## 🚀 Resumen Rápido

### Arquitectura del Sistema

```Bash
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raspberry Pi  │───▶│   Flask Backend  │───▶│    MongoDB      │
│  (Detección)    │    │   (API + Web)    │    │  (Almacén BD)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
    main.py              app.py + routes/           Colecciones:
    - OpenCV              - Authentication          - users
    - Detección           - Photo management        - record_camera
    - HTTP requests       - Video streaming
```

### Componentes Principales

- **🤖 Raspberry Pi**: `raspberry/main.py` - Detección de movimiento
- **🌐 Flask API**: `api/app.py` - Servidor web y API REST
- **🔐 Autenticación**: `routes/login.py` - Gestión de usuarios
- **📷 Cámara**: `routes/record_camera.py` - Fotos y streaming
- **📊 Dashboard**: `routes/dashboard.py` - Interfaz web
- **🗄️ Base de datos**: `controllers/` - Lógica de persistencia

---

## 🎯 Objetivo

Esta guía detalla la arquitectura del backend del sistema de videovigilancia, explicando cada componente, flujo de datos y casos de uso para facilitar el desarrollo y mantenimiento.

## 🏗️ Arquitectura Detallada

### Patrón MVC Adaptado

```Bash
┌─────────────────────┐
│      ROUTES         │ ◄── Endpoints HTTP/REST
│   (Controllers)     │
├─────────────────────┤
│    CONTROLLERS      │ ◄── Lógica de negocio
│  (Business Logic)   │
├─────────────────────┤
│     SERVICES        │ ◄── Servicios externos
│  (External APIs)    │
├─────────────────────┤
│      MODELS         │ ◄── Validación de datos
│    (Schemas)        │
└─────────────────────┘
```

### Flujo de Datos Principal

**1. Detección → Captura:**

```mermaid
Raspberry Pi → OpenCV → Análisis Frame → Detección → Captura Foto → POST API
```

**2. API → Almacenamiento:**

```mermaid
Flask Route → Validación → Controller → MongoDB → Discord Notification
```

**3. Usuario → Visualización:**

```mermaid
Web Browser → Dashboard → API Request → Database Query → JSON Response
```

---

## 📁 Estructura de Archivos Detallada

### 🚀 Aplicación Principal

**`api/app.py`** - Punto de entrada y configuración

```python
# Configuración principal
- Flask app initialization
- MongoDB connection
- Blueprint registration
- i18n configuration
- CORS and security headers

# Funciones clave:
- main(): Página de inicio con verificación de fotos huérfanas
- Error handlers (404, 500)
- Template context processors
```

### 🛣️ Rutas (Routes Layer)

#### `api/routes/login.py` - Sistema de Autenticación

**Endpoints disponibles:**

| Método | Ruta            | Función             | Descripción           | Autenticación |
| ------ | --------------- | ------------------- | --------------------- | ------------- |
| `GET`  | `/login/`       | `show_page_login()` | Página de login       | No            |
| `POST` | `/login/login`  | `login()`           | Procesar credenciales | No            |
| `POST` | `/login/signup` | `signup()`          | Registrar usuario     | No            |
| `GET`  | `/login/logout` | `logout()`          | Cerrar sesión         | Sí            |
| `POST` | `/login/delete` | `delete_use()`      | Eliminar usuario      | Admin         |
| `GET`  | `/login/users`  | `get_all_users()`   | Listar usuarios       | Admin         |

**Flujo de autenticación:**

```python
# 1. Usuario envía credenciales
POST /login/login
{
  "email": "user@example.com",
  "password": "password123"
}

# 2. Validación en base de datos
LoginController.get_user(email) → MongoDB query

# 3. Creación de sesión
session["email"] = email
session["isAdmin"] = user.isAdmin

# 4. Respuesta con redirección
{
  "message": "Login successful",
  "redirect": "/dashboard",
  "status": 200
}
```

#### `api/routes/record_camera.py` - Gestión de Fotos y Video

**Endpoints disponibles:**

| Método   | Ruta                            | Función              | Descripción               | Parámetros         |
| -------- | ------------------------------- | -------------------- | ------------------------- | ------------------ |
| `GET`    | `/api/photo/`                   | `obtener_foto()`     | Listar fotos              | `?date=YYYY-MM-DD` |
| `POST`   | `/api/photo/`                   | `add_foto()`         | Subir nueva foto          | FormData + file    |
| `GET`    | `/api/photo/<id>`               | `obtener_una_foto()` | Obtener foto específica   | photo_id           |
| `DELETE` | `/api/photo/<id>`               | `borrar_foto()`      | Eliminar foto             | photo_id           |
| `GET`    | `/api/photo/screenshots/<file>` | `media()`            | Servir archivos estáticos | filename           |
| `GET`    | `/api/photo/video`              | `real_streaming()`   | Stream de video           | -                  |
| `DELETE` | `/api/photo/photos/removeAll`   | `clean_photos()`     | Eliminar todas las fotos  | -                  |

**Flujo de captura de foto:**

```python
# 1. Raspberry Pi detecta movimiento (main.py)
movement_detected = np.mean(cv2.absdiff(frame1, frame2)) > 10

# 2. Captura y preparación
filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
cv2.imencode('.jpg', frame) → buffer

# 3. Envío a API
requests.post("/api/photo", files=file, data=metadata)

# 4. Procesamiento en Flask
- Validación con record_camera_schema
- Guardado en media/screenshots/
- Registro en MongoDB
- Notificación a Discord
```

#### `api/routes/dashboard.py` - Panel de Control

**Endpoints disponibles:**

| Método | Ruta                            | Función             | Descripción          | Permisos |
| ------ | ------------------------------- | ------------------- | -------------------- | -------- |
| `GET`  | `/dashboard/`                   | `dashboard()`       | Dashboard principal  | Usuario  |
| `GET`  | `/dashboard/admin`              | `admin_dashboard()` | Panel administrativo | Admin    |
| `GET`  | `/dashboard/admin/manage-users` | `admin_panel()`     | Gestión de usuarios  | Admin    |

**Sistema de permisos:**

```python
# Decoradores de seguridad
@login_required    # Requiere sesión activa
@admin_required    # Requiere permisos de administrador

# Lógica de redirección automática
if session.get("isAdmin"):
    return redirect("/dashboard/admin")
else:
    return render_template("dashboard_user.html")
```

---

### 🎮 Controladores (Controllers Layer)

#### `api/controllers/login_bd.py` - Gestión de Usuarios

```python
class LoginController:
    def __init__(self, mongo):
        self.collection = mongo.db["users"]

    # Métodos principales:
    def get_user(email):           # Buscar usuario por email
    def create_user(user_data):    # Crear nuevo usuario
    def delete_user(email):        # Eliminar usuario
    def get_all_users():          # Listar todos los usuarios
```

**Modelo de datos - Usuario:**

```python
{
  "_id": ObjectId("..."),
  "name": "Nombre Usuario",
  "email": "usuario@email.com",
  "password": "password_hash",    # ⚠️ TODO: Implementar hash
  "isAdmin": boolean,
  "createdAt": ISODate("..."),
  "lastLogin": ISODate("...")
}
```

#### `api/controllers/record_camera_bd.py` - Gestión de Fotos

```python
class RecordCameraController:
    def __init__(self, mongo):
        self.collection = mongo.db["record_camera"]

    # Métodos principales:
    def get_all_photos():              # Todas las fotos
    def get_photos_by_date(date):      # Filtrar por fecha
    def add_photo(data):               # Registrar nueva foto
    def delete_photo(photo_id):        # Eliminar foto específica
    def remove_all_photos():           # Limpiar todas las fotos
    def get_one_photo(photo_id):       # Obtener foto por ID
```

**Modelo de datos - Foto:**

```python
{
  "_id": ObjectId("..."),
  "filename": "20251017_143520.jpg",
  "date": "20251017_143520",         # Formato: YYYYMMDD_HHMMSS
  "file_path": "media/screenshots/20251017_143520.jpg",
  "createdAt": ISODate("..."),
  "size": 1024576,                   # Tamaño en bytes
  "detection_score": 15.7            # Nivel de movimiento detectado
}
```

**Búsqueda por fecha optimizada:**

```python
def get_photos_by_date(self, date_str):
    # Convierte YYYY-MM-DD → YYYYMMDD
    date_formatted = date_obj.strftime("%Y%m%d")

    # Usa regex para buscar por prefijo
    date_pattern = f"^{date_formatted}"
    photos = self.collection.find(
        {"date": {"$regex": date_pattern}},
        {"_id": 0}
    )
```

---

### ⚙️ Servicios (Services Layer)

#### `api/services/video.py` - Streaming de Video

```python
def make_video():
    """
    Genera stream MJPEG para visualización en tiempo real

    Características:
    - Captura de cámara con OpenCV
    - Codificación JPEG frame por frame
    - Stream multipart para navegadores
    - Manejo de errores de cámara
    """

    video = cv2.VideoCapture(0)  # Cámara principal

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Codificar frame como JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Generar chunk de stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')
```

**Configuración del stream:**

```python
# En record_camera.py
@record_cam_bp.route('/video')
def real_streaming():
    return Response(
        video.make_video(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
```

#### `api/services/missatge_discord.py` - Notificaciones

```python
def send_message(data):
    """
    Envía notificaciones a Discord cuando se detecta movimiento

    Parámetros:
    - data: {"date": "ISO_timestamp", "filename": "file.jpg"}

    Funcionalidades:
    - Conversión de timezone (UTC → Europe/Madrid)
    - Formateo de mensaje personalizable
    - Manejo de errores de webhook
    - Logging de estado de envío
    """

    # Conversión de zona horaria
    zona_madrid = pytz.timezone("Europe/Madrid")
    data_time_formateada = datetime.fromisoformat(data["date"])
    hora_madrid = data_time_formateada.astimezone(zona_madrid)

    # Envío de webhook
    webhook = DiscordWebhook(
        url=os.getenv("WEBHOOK_DISCORD"),
        content=f"¡Nueva foto capturada!\nHora: {hora_formateada}\nFilename: {filename}"
    )
```

#### `api/services/remove_photos.py` - Limpieza de Archivos Huérfanos

```python
def detect_photos_exists():
    """
    Detecta y elimina fotos del filesystem que no están en la base de datos

    Proceso:
    1. Lista archivos en media/screenshots/
    2. Consulta registros en MongoDB
    3. Identifica archivos huérfanos
    4. Elimina archivos no referenciados

    Ejecutado automáticamente en app startup
    """
```

---

### 📝 Esquemas de Validación (Models Layer)

#### `api/schemes.py` - Validación con Marshmallow

```python
# Esquema para fotos
class RecordCameraSchema(Schema):
    filename = fields.String(required=True)
    date = fields.String(required=True)
    file_path = fields.String(required=True)

# Esquema para usuarios
class UserSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=24))
    isAdmin = fields.Boolean(required=True)

# Instancias para uso
record_camera_schema = RecordCameraSchema()
user_schema = UserSchema()
```

**Proceso de validación:**

```python
# En las rutas
try:
    validated_data = user_schema.load(request.json)
except ValidationError as err:
    return jsonify({"errors": err.messages}), 400
```

---

## 🤖 Script Raspberry Pi

### `raspberry/main.py` - Detección de Movimiento

**Algoritmo de detección:**

```python
# 1. Captura de dos frames consecutivos
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# 2. Cálculo de diferencia
diferencia = cv2.absdiff(frame1, frame2)
gris = cv2.cvtColor(diferencia, cv2.COLOR_BGR2GRAY)

# 3. Análisis estadístico
average = np.mean(gris)  # Promedio de intensidad

# 4. Decisión de detección
if average > 10:  # Umbral configurable
    print("¡Movimiento detectado!")
    take_photo(frame2)
```

**Sistema de throttling:**

```python
# Limita capturas para evitar spam
count = 1
max_photos = 5

if count == max_photos:
    count = 1
    time.sleep(60)  # Pausa de 1 minuto
```

**Función de captura:**

```python
def take_photo(frame):
    # Generar nombre único
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

    # Codificar imagen
    res, buffer = cv2.imencode(".jpg", frame)
    file = {"file": (filename, buffer.tobytes(), "image/jpeg")}

    # Preparar metadata
    insert = {
        "filename": filename,
        "date": datetime.now().strftime("%Y%m%d_%H%M%S"),
    }

    # Enviar a API
    return requests.post(
        "http://localhost:5000/api/photo",
        files=file,
        data=insert
    )
```

---

## 🔧 Mini-Manuales para Errores Comunes

### ❌ Error: "No module named 'cv2'"

**Síntomas:**

```python
import cv2
# ModuleNotFoundError: No module named 'cv2'
```

**Causas posibles:**

1. **OpenCV no instalado**
2. **Entorno virtual incorrecto**
3. **Versión incompatible**

**✅ Soluciones:**

**1. Instalar OpenCV:**

```bash
# Versión estándar (con GUI)
pip install opencv-python

# Versión headless (sin GUI, recomendada para servidor)
pip install opencv-python-headless

# Verificar instalación
python -c "import cv2; print(cv2.__version__)"
```

**2. Configuración Raspberry Pi:**

```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3-opencv

# O compilar desde fuente (más lento, más control)
sudo apt install build-essential cmake git pkg-config
```

---

### ❌ Error: "Failed to open video device"

**Síntomas:**

```python
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
# ret = False, frame = None
```

**Causas posibles:**

1. **Cámara no conectada/reconocida**
2. **Permisos insuficientes**
3. **Índice de cámara incorrecto**
4. **Cámara en uso por otra aplicación**

**✅ Soluciones:**

**1. Verificar dispositivos disponibles:**

```bash
# Linux - listar cámaras
ls -la /dev/video*
# Debe mostrar: /dev/video0, /dev/video1, etc.

# Windows - usar Device Manager
# Buscar "Cameras" o "Imaging devices"
```

**2. Probar diferentes índices:**

```python
# Probar múltiples índices de cámara
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Cámara encontrada en índice {i}")
        ret, frame = cap.read()
        if ret:
            print(f"Frame capturado: {frame.shape}")
        cap.release()
```

**3. Configurar permisos (Linux):**

```bash
# Añadir usuario al grupo video
sudo usermod -a -G video $USER

# Aplicar cambios (requiere logout/login)
newgrp video
```

---

### ❌ Error: "Connection refused" en requests

**Síntomas:**

```python
requests.post("http://localhost:5000/api/photo", ...)
# ConnectionError: Connection refused
```

**Causas posibles:**

1. **Flask server no ejecutándose**
2. **Puerto incorrecto**
3. **Firewall bloqueando conexión**
4. **IP incorrecta (si Raspberry Pi es remoto)**

**✅ Soluciones:**

**1. Verificar servidor Flask:**

```bash
# Verificar si Flask está ejecutándose
netstat -tuln | grep 5000
# Debe mostrar: tcp 0.0.0.0:5000 LISTEN

# Si no está activo, iniciar servidor
cd backend/api
python app.py
```

**2. Configurar IP dinámica:**

```python
# En raspberry/main.py - configurar IP del servidor
import os

# Obtener IP del servidor Flask (variable de entorno)
FLASK_SERVER_URL = os.getenv('FLASK_SERVER_URL', 'http://localhost:5000')

# Usar en requests
requests.post(f"{FLASK_SERVER_URL}/api/photo", files=file, data=insert)
```

**3. Configurar Flask para acceso remoto:**

```python
# En app.py - permitir conexiones externas
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    # host='0.0.0.0' permite conexiones desde cualquier IP
```

---

### ❌ Error: "Duplicate key error" en MongoDB

**Síntomas:**

```python
# pymongo.errors.DuplicateKeyError: E11000 duplicate key error
```

**Causas posibles:**

1. **Filename duplicado**
2. **Timestamp idéntico (múltiples fotos por segundo)**
3. **Index único en campo problemático**

**✅ Soluciones:**

**1. Mejorar generación de nombres únicos:**

```python
import time
import uuid

def generate_unique_filename():
    # Timestamp con microsegundos + UUID corto
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Remove last 3 microsecond digits
    unique_id = str(uuid.uuid4())[:8]  # 8 caracteres de UUID
    return f"{timestamp}_{unique_id}.jpg"

# Ejemplo: 20251017_143520_123_a1b2c3d4.jpg
```

**2. Manejo de colisiones:**

```python
def add_photo_safe(self, data):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            self.collection.insert_one(data)
            return {"msg": "Photo record created"}
        except DuplicateKeyError:
            # Regenerar filename y reintentar
            data["filename"] = generate_unique_filename()
            data["file_path"] = f"media/screenshots/{data['filename']}"

    raise Exception("No se pudo generar filename único después de varios intentos")
```

---

## 🛡️ Seguridad y Mejores Prácticas

### Autenticación Mejorada

**⚠️ Problemas actuales:**

```python
# INSEGURO - Contraseñas en texto plano
user.get("password") != password  # Comparación directa
```

**✅ Implementación segura recomendada:**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Al registrar usuario
password_hash = generate_password_hash(password, method='pbkdf2:sha256')

# Al verificar login
if not check_password_hash(user.password_hash, password):
    return jsonify({"message": "Invalid credentials"}), 401
```

### Validación de Archivos

```python
# Validar tipos de archivo permitidos
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Validar tamaño de archivo
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Aplicar a endpoints sensibles
@app.route('/api/photo', methods=['POST'])
@limiter.limit("10 per minute")  # Máximo 10 fotos por minuto
def add_foto():
    # ...
```

---

## 📊 Monitoreo y Logs

### Sistema de Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging en app.py
if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/security_camera.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

# Uso en código
app.logger.info(f'Foto capturada: {filename}')
app.logger.error(f'Error al procesar imagen: {str(e)}')
```

### Métricas de Sistema

```python
# Script de monitoreo - monitor.py
import psutil
import time
from datetime import datetime

def system_stats():
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'camera_active': check_camera_active(),
        'flask_running': check_flask_running(),
        'timestamp': datetime.now().isoformat()
    }

def check_camera_active():
    # Verificar si el proceso de detección está activo
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in proc.info['name'] and 'main.py' in ' '.join(proc.info['cmdline']):
            return True
    return False
```

---

## 📋 Checklist de Deployment

### ✅ Preparación del Servidor

- [ ] Python 3.8+ instalado
- [ ] MongoDB configurado y accesible
- [ ] OpenCV instalado correctamente
- [ ] Cámara conectada y con permisos
- [ ] Variables de entorno configuradas
- [ ] Puertos abiertos (5000, 27017)

### ✅ Configuración de Seguridad

- [ ] Hash de contraseñas implementado
- [ ] Rate limiting configurado
- [ ] Validación de archivos activa
- [ ] HTTPS configurado (producción)
- [ ] Firewall configurado correctamente
- [ ] Logs configurados y rotados

### ✅ Optimización

- [ ] Índices de base de datos creados
- [ ] Limpieza automática de archivos antiguos
- [ ] Compresión de imágenes configurada
- [ ] Cache para consultas frecuentes
- [ ] Monitoreo de recursos del sistema

---

## 📚 Referencias y Recursos

### Documentación Oficial

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Python Guide](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PyMongo Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [Marshmallow Validation](https://marshmallow.readthedocs.io/)

### Herramientas de Desarrollo

```bash
# Testing
pip install pytest pytest-flask pytest-cov

# Code quality
pip install pylint black isort

# Debugging
pip install flask-debugtoolbar
```

### Comandos Útiles

```bash
# Verificar estado del sistema
python check_system.py

# Limpiar archivos huérfanos
python cleanup_orphaned_files.py

# Generar reporte de uso
python generate_usage_report.py

# Backup de base de datos
mongodump --db security_camera --out backup/$(date +%Y%m%d)
```

---

## 💡 Consejos Finales

1. **Modularidad**: Mantén separadas las responsabilidades entre capas
2. **Error Handling**: Implementa manejo robusto de errores en cada endpoint
3. **Testing**: Crea tests unitarios para controladores y servicios
4. **Documentación**: Mantén comentarios actualizados en código complejo
5. **Performance**: Optimiza consultas de base de datos frecuentes
6. **Backup**: Implementa respaldo regular de fotos y configuración
7. **Monitoreo**: Configura alertas para errores críticos del sistema

---

_Este backend está diseñado para ser escalable y mantenible. Sigue las mejores prácticas y mantén la documentación actualizada según evolucione el proyecto._
