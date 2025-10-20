# Guía Completa de Gestión Segura de Variables de Entorno

## Resumen Rápido

### Comandos Esenciales

```bash
# 1. Instalar Infisical CLI
winget install infisical

# 2. Configurar proyecto
infisical login
infisical init

# 3. Ejecutar aplicación con variables seguras
infisical run --env=dev python app.py

# 4. Alternativa con archivo .env local
cp .env.example .env
# Editar .env con tus valores
python app.py
```

### Variables Requeridas

```env
# MongoDB
URL_MONGO=mongodb://localhost:27017/security_camera

# Discord
WEBHOOK_DISCORD=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL

# Flask
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
FLASK_ENV=development
```

---

## Objetivo

Esta guía te ayudará a configurar un sistema seguro de gestión de variables de entorno para el proyecto de cámara de seguridad, utilizando **Infisical** como servicio externo o métodos locales alternativos.

## 🔐 ¿Por Qué Gestión Segura de Variables?

### Problemas de Seguridad Comunes

**MAL - Hardcoded en código:**

```python
# ¡NUNCA HAGAS ESTO!
MONGO_URL = "mongodb://admin:password123@localhost:27017/"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/123456789/abcdef"
```

**MAL - Versionado en Git:**

```bash
# ¡NUNCA subas esto a Git!
git add .env
git commit -m "Añadidas credenciales"  # 🚨 PELIGRO
```

**BIEN - Variables de entorno:**

```python
import os
MONGO_URL = os.getenv('URL_MONGO')
DISCORD_WEBHOOK = os.getenv('WEBHOOK_DISCORD')
```

### Beneficios de la Gestión Segura

- **Seguridad**: Credenciales no expuestas en código fuente
- **Colaboración**: Compartir configuraciones sin exponer secretos  
- **Entornos múltiples**: Diferentes configs para dev/test/prod
- **Rotación de claves**: Cambio fácil sin modificar código

---

## Método 1: Infisical (Recomendado para Equipos)

### ¿Qué es Infisical?

[Infisical](https://infisical.com/) es una plataforma **open-source y gratuita** para gestión colaborativa de secretos que permite:

- Sincronización automática entre entornos
- Gestión de permisos por equipo
- Interfaz web intuitiva
- Encriptación end-to-end
- CLI integrado

### Configuración Paso a Paso

#### 1. Crear Cuenta y Proyecto

1. **Registrarse** en [Infisical](https://infisical.com/)
2. **Crear nuevo proyecto** o solicitar acceso al existente
3. **Configurar entornos**: `development`, `staging`, `production`

#### 2. Instalar Infisical CLI

**Windows:**

```bash
# PowerShell/CMD
winget install infisical

# Scoop (alternativa)
scoop install infisical

# Chocolatey (alternativa)
choco install infisical
```

**macOS:**

```bash
# Homebrew
brew install infisical/infisical-cli/infisical

# Manual
curl -1sLf 'https://dl.infisical.com/cli/install.sh' | sh
```

**Linux:**

```bash
# Debian/Ubuntu
curl -1sLf 'https://dl.infisical.com/cli/install.sh' | sh

# Arch Linux
yay -S infisical-cli
```

#### 3. Autenticación y Configuración

```bash
# Iniciar sesión
infisical login

# Navegar al directorio del proyecto
cd raspberryPi/backend

# Inicializar configuración
infisical init

# Seleccionar proyecto y entorno cuando se solicite
```

#### 4. Configurar Variables en Infisical

**Via Web Dashboard:**

1. Abrir dashboard de Infisical
2. Seleccionar proyecto
3. Añadir variables por entorno:

```env
# Environment: development
URL_MONGO=mongodb://localhost:27017/security_camera_dev
WEBHOOK_DISCORD=https://discord.com/api/webhooks/DEV_WEBHOOK
SECRET_KEY=dev-secret-key-12345
FLASK_ENV=development

# Environment: production  
URL_MONGO=mongodb://production-server:27017/security_camera
WEBHOOK_DISCORD=https://discord.com/api/webhooks/PROD_WEBHOOK
SECRET_KEY=super-secure-production-key-98765
FLASK_ENV=production
```

**Via CLI:**

```bash
# Añadir variable individual
infisical secrets set URL_MONGO "mongodb://localhost:27017/security_camera"

# Importar desde archivo
infisical secrets import --env dev .env.example
```

#### 5. Uso en Desarrollo

```bash
# Ejecutar aplicación con variables de development
infisical run --env=dev python app.py

# Ejecutar script específico
infisical run --env=dev python raspberry/main.py

# Abrir shell con variables cargadas
infisical shell --env=dev
```

---

## Método 2: Archivo .env Local (Para Desarrollo Individual)

### Configuración con python-dotenv

#### 1. Instalar Dependencia

```bash
pip install python-dotenv
```

#### 2. Crear Archivos de Configuración

**Crear `.env.example` (versionable):**

```env
# ===========================================
# CONFIGURACIÓN - RASPBERRY PI SECURITY CAMERA
# ===========================================

# --- BASE DE DATOS ---
URL_MONGO=mongodb://localhost:27017/security_camera
# Ejemplo: mongodb://usuario:password@servidor:27017/database

# --- DISCORD NOTIFICATIONS ---
WEBHOOK_DISCORD=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
# Obtener desde: Discord Server Settings → Integrations → Webhooks

# --- FLASK CONFIG ---
SECRET_KEY=cambia-por-una-clave-secreta-unica
FLASK_ENV=development
FLASK_DEBUG=True

# --- OPCIONAL ---
# CAMERA_INDEX=0
# MAX_PHOTOS_PER_MINUTE=5
# DETECTION_THRESHOLD=10
```

**Crear `.env` (NO versionar):**

```bash
# Copiar plantilla
cp .env.example .env

# Editar con valores reales
nano .env  # o code .env
```

#### 3. Configurar en la Aplicación

**Modificar `app.py`:**

```python
import os
from dotenv import load_dotenv

# Cargar variables de entorno al inicio
load_dotenv()

# Uso normal de variables
app.config["MONGO_URI"] = os.getenv("URL_MONGO")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
```

#### 4. Proteger Archivo .env

**Añadir a `.gitignore`:**

```gitignore
# Variables de entorno
.env
.env.local
.env.*.local

# Logs
*.log

# Cache de Python
__pycache__/
*.pyc
```

---

## 🔧 Mini-Manuales para Errores Comunes

### Error: "infisical: command not found"

**Síntomas:**

```bash
infisical --version
# bash: infisical: command not found
```

**Causas posibles:**

1. **CLI no instalado correctamente**
2. **PATH no configurado**
3. **Terminal no reiniciada**

**Soluciones:**

**1. Verificar instalación:**

```bash
# Windows - verificar en PATH
where infisical

# Unix - verificar ubicación
which infisical

# Si no existe, reinstalar
winget uninstall infisical
winget install infisical
```

**2. Configurar PATH manualmente (Windows):**

```powershell
# Añadir a PATH del usuario
$env:PATH += ";C:\Program Files\Infisical\bin"

# Permanente via System Properties
# Sistema → Configuración avanzada → Variables de entorno
```

**3. Reiniciar terminal:**

```bash
# Cerrar y abrir nueva terminal
# O recargar configuración
source ~/.bashrc  # Unix
```

---

### Error: "Authentication failed"

**Síntomas:**

```bash
infisical secrets list
# Error: Authentication failed. Please login again.
```

**Causas posibles:**

1. **Token expirado**
2. **Credenciales incorrectas**
3. **Proyecto no accesible**

**Soluciones:**

**1. Re-autenticar:**

```bash
# Logout y login nuevamente
infisical logout
infisical login

# Verificar usuario actual
infisical user
```

**2. Verificar permisos del proyecto:**

```bash
# Listar proyectos accesibles
infisical projects list

# Re-inicializar si es necesario
rm .infisical.json
infisical init
```

---

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Síntomas:**

```python
from dotenv import load_dotenv
# ModuleNotFoundError: No module named 'dotenv'
```

**Causas posibles:**

1. **python-dotenv no instalado**
2. **Entorno virtual incorrecto**

**Soluciones:**

**1. Instalar dependencia:**

```bash
# Verificar entorno virtual activado
pip install python-dotenv

# Añadir a requirements.txt
echo "python-dotenv" >> requirements.txt
```

**2. Verificar importación:**

```python
# Método seguro con try/except
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv no instalado. Usando variables del sistema.")
```

---

### Error: Variables no se cargan correctamente

**Síntomas:**

```python
print(os.getenv('URL_MONGO'))
# None (debería mostrar la URL)
```

**Causas posibles:**

1. **Archivo .env en ubicación incorrecta**
2. **load_dotenv() no llamado**
3. **Sintaxis incorrecta en .env**

**Soluciones:**

**1. Verificar ubicación de .env:**

```bash
# Debe estar en la raíz del proyecto
ls -la .env  # Unix
dir .env     # Windows

# Si está en subdirectorio, especificar ruta
```

**2. Cargar explícitamente:**

```python
from dotenv import load_dotenv
import os

# Cargar desde ubicación específica
load_dotenv('.env')
# o
load_dotenv('/ruta/completa/al/.env')

# Verificar carga
print("Variables cargadas:", list(os.environ.keys()))
```

**3. Verificar sintaxis de .env:**

```env
# CORRECTO
URL_MONGO=mongodb://localhost:27017/db
SECRET_KEY=mi-clave-secreta

# INCORRECTO
URL_MONGO = mongodb://localhost:27017/db  # Espacios problemáticos
SECRET_KEY="mi clave con espacios"        # Comillas innecesarias
```

---

## Mejores Prácticas de Seguridad

### Generación de Claves Seguras

```python
# Script para generar SECRET_KEY segura
import secrets

def generate_secret_key():
    return secrets.token_urlsafe(32)

print("SECRET_KEY:", generate_secret_key())
# Ejemplo: SECRET_KEY=dGVzdC1rZXktMTIzNDU2Nzg5MGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3
```

### Rotación de Credenciales

**Programar cambios regulares:**

1. **MongoDB**: Crear usuario específico con permisos mínimos
2. **Discord Webhook**: Regenerar URL periódicamente  
3. **SECRET_KEY**: Cambiar en cada deployment importante

### Separación por Entornos

```env
# development.env
URL_MONGO=mongodb://localhost:27017/security_camera_dev
FLASK_DEBUG=True

# production.env  
URL_MONGO=mongodb://prod-server:27017/security_camera
FLASK_DEBUG=False
```

### Validación de Variables

```python
# En app.py - Validar variables críticas
required_vars = ['URL_MONGO', 'WEBHOOK_DISCORD', 'SECRET_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"❌ Variables requeridas faltantes: {missing_vars}")
```

---

## Herramientas de Debugging

### Script de Verificación de Variables

```python
# check_env.py
import os
from dotenv import load_dotenv

def check_environment():
    load_dotenv()
    
    required_vars = {
        'URL_MONGO': 'Conexión a base de datos MongoDB',
        'WEBHOOK_DISCORD': 'URL del webhook de Discord',  
        'SECRET_KEY': 'Clave secreta de Flask'
    }
    
    optional_vars = {
        'FLASK_ENV': 'Entorno de Flask (development/production)',
        'FLASK_DEBUG': 'Modo debug de Flask'
    }
    
    print("🔍 Verificando variables de entorno...\n")
    
    # Variables requeridas
    print("📋 Variables Requeridas:")
    all_ok = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Ocultar valor sensible, mostrar solo inicio
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value} ({description})")
        else:
            print(f"❌ {var}: NO CONFIGURADA ({description})")
            all_ok = False
    
    # Variables opcionales
    print(f"\n📋 Variables Opcionales:")
    for var, description in optional_vars.items():
        value = os.getenv(var, 'No configurada')
        print(f"ℹ️  {var}: {value} ({description})")
    
    print(f"\n🎯 Estado: {'✅ Configuración completa' if all_ok else '❌ Configuración incompleta'}")
    return all_ok

if __name__ == '__main__':
    check_environment()
```

### Comando de Verificación Rápida

```bash
# Con Infisical
infisical run --env=dev python check_env.py

# Con .env local
python check_env.py
```

---

## Checklist de Configuración

### Para Desarrollo Local

- [ ] Infisical CLI instalado y configurado, O archivo .env creado
- [ ] Todas las variables requeridas configuradas
- [ ] `.env` añadido a `.gitignore` (si usas método local)
- [ ] Script de verificación ejecutado sin errores
- [ ] Aplicación se ejecuta correctamente

### Para Deployment

- [ ] Variables de producción configuradas por separado
- [ ] Credenciales de producción diferentes a desarrollo
- [ ] Backup de configuración en lugar seguro
- [ ] Accesos de equipo configurados correctamente

### Para Seguridad

- [ ] Claves generadas aleatoriamente (no palabras comunes)
- [ ] Permisos mínimos necesarios en base de datos
- [ ] Rotación programada de credenciales sensibles
- [ ] Monitoreo de accesos no autorizados

---

## Recursos Adicionales

### Herramientas Alternativas

**Para gestión de secretos:**

- [HashiCorp Vault](https://www.vaultproject.io/): Solución enterprise
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/): Para AWS
- [Azure Key Vault](https://azure.microsoft.com/services/key-vault/): Para Azure
- [Google Secret Manager](https://cloud.google.com/secret-manager): Para GCP

**Para desarrollo local:**

- [direnv](https://direnv.net/): Auto-carga de variables por directorio
- [pass](https://www.passwordstore.org/): Gestor de contraseñas CLI
- [1Password CLI](https://1password.com/downloads/command-line/): Integración con 1Password

### Referencias de Seguridad

- [OWASP Environment Variable Security](https://owasp.org/www-community/vulnerabilities/Information_exposure_through_environment_variables)
- [12-Factor App Config](https://12factor.net/config)
- [Infisical Documentation](https://infisical.com/docs)

---

## Consejos Finales

1. **Nunca hardcodees secretos**: Siempre usa variables de entorno
2. **Separa entornos**: Diferentes credenciales para dev/staging/prod  
3. **Documenta variables**: Mantén `.env.example` actualizado
4. **Automatiza verificación**: Scripts que validen configuración
5. **Planifica rotación**: Cambios regulares de credenciales críticas
6. **Backup seguro**: Guarda configuraciones en lugar seguro
7. **Equipo informado**: Todos deben conocer el flujo de secretos

---

*La seguridad es un proceso continuo. Revisa y actualiza regularmente tus prácticas de gestión de secretos.*
