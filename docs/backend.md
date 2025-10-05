# Backend - Sistema de Detección de Movimiento y Captura de Imágenes

Este backend implementa un sistema de videovigilancia con detección de movimiento.  
Al detectar movimiento mediante un sensor PIR, el sistema activa una cámara, captura una foto, la guarda en el sistema de archivos y registra la información en una base de datos MongoDB.

---
## Descripción de Componentes

### `api/controllers/camera.py`
Controlador encargado de manejar la cámara (OpenCV).

**Funciones principales:**
- `hacer_foto()`:  
    Se encarga de realizar la foto y devuelve un json con el nombre del fichero, la fecha y la ruta donde se encuentra la imagen guardada

---

### `api/controllers/record_camera_bd.py`
Encargado de la comunicación con la base de datos (MongoDB).

**Funciones típicas:**
- `add_photo(data)`: 
    Inserta los datos en record_camera
- `get_all_photos()`: 
    Devuelve todos los documentos que hay registrados en record_camera de la bd
- `get_one_route()`: 
    Obtiene un registro específico.

---

### `api/routes/record_camera.py`
Define los endpoints (rutas) del módulo de cámara.

**Endpoints:**

| Método | Ruta | Descripción | Datos que devuelve |
|--------|------|--------------|--------------------|
| `POST` | `/api/photo` | Captura una foto desde la cámara, la guarda en disco y la inserta en BD | `{ "fichero", "fecha", "ruta" }` |

**Flujo:**
1. Se llama a `CameraController.hacer_foto()`
2. Se validan los datos con `record_camera_schema`
3. Se almacenan en la BD mediante `RecordCameraController`

---

### `api/schemes/record_camera_schema.py`
Define la estructura y lo que se tiene que validar para los datos de la bd

**Campos esperados:**
- `fichero`: nombre del archivo (`string`)
- `fecha`: fecha de captura (`string`)
- `ruta`: ruta donde se guarda la imagen (`string`)

---
