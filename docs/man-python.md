# 🐍 Guía Completa de Configuración Python - Raspberry Pi Security Camera

## 🚀 Resumen Rápido

### Comandos Esenciales

```bash
# 1. Crear entorno virtual
cd backend
python -m venv .venv

# 2. Activar entorno virtual
# Windows PowerShell/CMD
.venv\Scripts\activate
# Windows Git Bash
source .venv/Scripts/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
python app.py
```

### Para Desarrollo Rápido

```bash
# Todo en una línea (PowerShell)
cd backend; python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt; python app.py
```

---

## 🎯 Objetivo

Esta guía te ayudará a configurar correctamente el entorno Python para el proyecto de cámara de seguridad Raspberry Pi, desde la instalación inicial hasta la resolución de errores comunes.

## ⚡ Configuración Inicial

### 1. Requisitos Previos

**Verificar Python instalado:**

```bash
python --version
# Debe mostrar Python 3.8 o superior
```

**Si no tienes Python:**

- **Windows**: Descargar desde [python.org](https://python.org) o usar `winget install Python.Python.3.11`
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-venv python3-pip`

### 2. Estructura del Proyecto

```Bash
raspberryPi/
├── backend/
│   ├── api/
│   │   ├── app.py              # 🚀 Aplicación principal
│   │   ├── requirements.txt    # 📦 Dependencias
│   │   ├── config.ini          # ⚙️ Configuración
│   │   └── ...
│   ├── .venv/                  # 🐍 Entorno virtual (se crea)
│   └── raspberry/
│       └── main.py             # 📷 Script detección movimiento
```

### 3. Configuración del Entorno Virtual

**¿Por qué usar entorno virtual?**

- Aísla las dependencias del proyecto
- Evita conflictos entre versiones de librerías
- Permite fácil reproducción del entorno

```bash
# Navegar al directorio del backend
cd raspberryPi/backend

# Crear entorno virtual
python -m venv .venv

# Verificar creación
ls .venv/  # Debe mostrar: Include/ Lib/ Scripts/ pyvenv.cfg
```

---

## 🔄 Activación del Entorno Virtual

### Windows

**PowerShell (Recomendado):**

```powershell
.venv\Scripts\Activate.ps1
```

**Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**Git Bash:**

```bash
source .venv/Scripts/activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

### Verificar Activación

```bash
# El prompt debe mostrar (.venv) al inicio
(.venv) PS C:\...\backend>

# Verificar ubicación de Python
which python    # Unix/macOS
where python    # Windows
# Debe apuntar a .venv/Scripts/python o .venv/bin/python
```

---

## 📦 Gestión de Dependencias

### Instalación de Dependencias

```bash
# Asegúrate de que el entorno virtual esté activado
pip install -r requirements.txt

# Verificar instalación
pip list
```

### Dependencias del Proyecto

**requirements.txt actual:**

```txt
flask                    # Framework web
Flask-PyMongo           # Integración MongoDB
opencv-python-headless  # Procesamiento de imágenes (sin GUI)
Requests               # Cliente HTTP
marshmallow           # Validación de datos
numpy                 # Operaciones numéricas
discord-webhook       # Notificaciones Discord
Flask-Babel          # Internacionalización
Babel               # Herramientas i18n
```

### Actualizar Dependencias

```bash
# Actualizar pip primero
pip install --upgrade pip

# Actualizar todas las dependencias
pip install -r requirements.txt --upgrade

# Generar nuevo requirements.txt con versiones exactas
pip freeze > requirements-freeze.txt
```

---

## 🚀 Ejecución de la Aplicación

### Modo Desarrollo

```bash
# Activar entorno virtual
.venv\Scripts\activate

# Navegar a la carpeta API
cd api

# Ejecutar aplicación principal
python app.py

# O con variables de entorno (ver secure-env.md)
infisical run --env=dev python app.py
```

### Script Raspberry Pi

```bash
# Para el script de detección de movimiento
cd raspberry
python main.py
```

### Verificar Funcionamiento

1. **Aplicación Web**: <http://localhost:5000>
2. **Logs en consola**: Debe mostrar mensajes Flask sin errores
3. **Base de datos**: Verificar conexión MongoDB

---

## 🔧 Mini-Manuales para Errores Comunes

### ❌ Error: "python: command not found"

**Síntomas:**

```bash
python --version
# bash: python: command not found
```

**Causas posibles:**

1. **Python no instalado**
2. **Python instalado como `python3`**
3. **PATH no configurado**

**✅ Soluciones:**

**1. Verificar instalación:**

```bash
# Probar diferentes comandos
python --version
python3 --version
py --version      # Windows

# Si python3 funciona, crear alias (Linux/macOS)
alias python=python3
```

**2. Instalar Python:**

```bash
# Windows
winget install Python.Python.3.11

# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

---

### ❌ Error: "No module named 'flask'"

**Síntomas:**

```bash
python app.py
# ModuleNotFoundError: No module named 'flask'
```

**Causas posibles:**

1. **Entorno virtual no activado**
2. **Dependencias no instaladas**
3. **Python usando sistema global**

**✅ Soluciones:**

**1. Verificar entorno virtual:**

```bash
# Debe mostrar (.venv) en el prompt
# Si no, activar:
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix

# Verificar ubicación de Python
where python  # Debe apuntar a .venv
```

**2. Instalar dependencias:**

```bash
# Con entorno virtual activado
pip install -r requirements.txt

# Verificar instalación de Flask
pip show flask
```

---

### ❌ Error: "cannot import name 'app' from 'app'"

**Síntomas:**

```bash
# Error circular de importación
ImportError: cannot import name 'app' from 'app'
```

**Causas posibles:**

1. **Importación circular**
2. **Archivo mal estructurado**

**✅ Soluciones:**

**1. Verificar estructura de app.py:**

```python
# ✅ CORRECTO - app.py
from flask import Flask

app = Flask(__name__)
# ... configuración ...

if __name__ == '__main__':
    app.run(debug=True)
```

**2. Ejecutar desde directorio correcto:**

```bash
# ✅ CORRECTO
cd backend/api
python app.py

# ❌ INCORRECTO
cd backend
python api/app.py  # Puede causar problemas de importación
```

---

### ❌ Error: "Permission denied" al crear entorno virtual

**Síntomas:**

```bash
python -m venv .venv
# PermissionError: [Errno 13] Permission denied
```

**Causas posibles:**

1. **Permisos insuficientes**
2. **Directorio en uso**
3. **Antivirus bloqueando**

**✅ Soluciones:**

**1. Ejecutar como administrador (Windows):**

```powershell
# PowerShell como administrador
python -m venv .venv
```

**2. Cambiar ubicación:**

```bash
# Crear en directorio personal
cd ~
python -m venv proyecto-venv
# Luego activar desde el proyecto
~/proyecto-venv/Scripts/activate
```

**3. Verificar antivirus:**

- Añadir excepción para la carpeta del proyecto
- Deshabilitar temporalmente protección en tiempo real

---

### ❌ Error: "opencv-python installation failed"

**Síntomas:**

```bash
pip install opencv-python-headless
# ERROR: Failed building wheel for opencv-python-headless
```

**Causas posibles:**

1. **Falta Microsoft Visual C++**
2. **Arquitectura incompatible**
3. **Memoria insuficiente**

**✅ Soluciones:**

**1. Instalar Microsoft Visual C++ (Windows):**

- Descargar "Microsoft C++ Build Tools"
- O instalar Visual Studio Community

**2. Usar wheel precompilado:**

```bash
# Instalar wheel específico para tu arquitectura
pip install --only-binary=all opencv-python-headless

# O usar conda si está disponible
conda install opencv
```

**3. Aumentar memoria virtual:**

```bash
# Usar swap file en Linux
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🎯 Scripts de Automatización

### Script de Configuración Completa

**setup.bat (Windows):**

```batch
@echo off
echo 🚀 Configurando entorno Python...
cd backend
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Configuración completada!
echo.
echo Para activar el entorno: .venv\Scripts\activate
echo Para ejecutar la app: python api/app.py
pause
```

**setup.sh (Unix/macOS):**

```bash
#!/bin/bash
echo "🚀 Configurando entorno Python..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Configuración completada!"
echo ""
echo "Para activar el entorno: source .venv/bin/activate"
echo "Para ejecutar la app: python api/app.py"
```

### Script de Desarrollo

**dev.bat (Windows):**

```batch
@echo off
cd backend
call .venv\Scripts\activate
cd api
python app.py
```

### Script de Verificación

**check.py:**

```python
#!/usr/bin/env python3
import sys
import subprocess
import importlib

def check_python_version():
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 8):
        print("❌ Python 3.8+ requerido")
        return False
    print("✅ Versión Python correcta")
    return True

def check_virtual_env():
    venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if venv:
        print("✅ Entorno virtual activado")
        print(f"   Ubicación: {sys.prefix}")
    else:
        print("⚠️  Entorno virtual no activado")
    return venv

def check_dependencies():
    required = ['flask', 'pymongo', 'cv2', 'requests', 'marshmallow', 'numpy', 'babel']
    missing = []

    for module in required:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)

    return len(missing) == 0

if __name__ == '__main__':
    print("🔍 Verificando configuración Python...\n")

    python_ok = check_python_version()
    venv_ok = check_virtual_env()
    deps_ok = check_dependencies()

    print(f"\n📋 Resultado: {'✅ Todo correcto' if all([python_ok, deps_ok]) else '❌ Revisar errores'}")

    if not venv_ok:
        print("\n💡 Recomendación: Activar entorno virtual antes de ejecutar")
```

---

## 🔍 Herramientas de Debugging

### Verificar Configuración Actual

```bash
# Información del entorno Python
python -m site

# Variables de entorno relevantes
echo $VIRTUAL_ENV     # Unix
echo %VIRTUAL_ENV%    # Windows

# Ubicación de pip
which pip    # Unix
where pip    # Windows

# Paquetes instalados con ubicaciones
pip show flask opencv-python-headless
```

### Logs de Desarrollo

```python
# En app.py - Habilitar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar importaciones al inicio
print(f"Python: {sys.version}")
print(f"Flask: {flask.__version__}")
print(f"OpenCV: {cv2.__version__}")
```

---

## 📋 Checklist de Verificación

### ✅ Antes de comenzar desarrollo

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado en `.venv/`
- [ ] Entorno virtual activado (prompt muestra `.venv`)
- [ ] Dependencias instaladas sin errores
- [ ] `python app.py` ejecuta sin errores
- [ ] Navegador abre <http://localhost:5000>

### ✅ Para deployment

- [ ] requirements.txt actualizado
- [ ] Variables de entorno configuradas
- [ ] Puertos abiertos (5000)
- [ ] Permisos de cámara configurados
- [ ] MongoDB accesible

---

## 📚 Recursos Adicionales

### IDEs Recomendados

- **VS Code**: Con extensiones Python y Pylance
- **PyCharm**: IDE completo para Python
- **Sublime Text**: Editor ligero con soporte Python

### Herramientas Útiles

```bash
# Análisis de código
pip install pylint black isort

# Testing
pip install pytest pytest-cov

# Documentación
pip install sphinx
```

### Referencias Online

- [Python Virtual Environments Guide](https://docs.python.org/3/library/venv.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Python Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

---

## 💡 Consejos Finales

1. **Siempre usa entorno virtual**: Evita conflictos entre proyectos
2. **Mantén requirements.txt actualizado**: Facilita el deployment
3. **Documenta dependencias específicas**: Especifica versiones si hay incompatibilidades
4. **Prueba en entorno limpio**: Antes del deployment, prueba en nuevo entorno virtual
5. **Backup de configuración**: Guarda scripts de configuración en el repositorio

---

*Este documento debe actualizarse según evolucione el proyecto. ¡Mantén siempre la documentación sincronizada con tu implementación!*thon

## Instalación

```bash
cd backend
python -m venv .venv

# De forma manual, sin extension
# cd .venv/Scripts
# ./Activate.ps1 O ./activate.bat

pip install -r requeriments.txt
```
