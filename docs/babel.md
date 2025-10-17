# 📖 Guía Completa de Internacionalización con PyBabel

## 🚀 Resumen Rápido

### Comandos Esenciales

```bash
# 1. Extraer cadenas del código
pybabel extract -F babel.cfg -o locales/messages.pot .

# 2. Actualizar traducciones existentes
pybabel update -i locales/messages.pot -d locales

# 3. Compilar traducciones para producción
pybabel compile -d locales
```

### Para Nuevos Idiomas

```bash
# Inicializar un nuevo idioma (ej: francés)
pybabel init -i locales/messages.pot -d locales -l fr
```

---

## 🎯 Objetivo

Esta guía te ayudará a implementar un sistema completo de internacionalización (i18n) en tu proyecto usando **PyBabel**. Aprenderás desde la configuración inicial hasta la resolución de errores comunes.

## ⚡ Configuración Inicial

### 1. Instalación de Dependencias

```bash
pip install Flask-Babel Babel
```

### 2. Estructura de Directorios Recomendada

```Bash
proyecto/
├── babel.cfg                 # Configuración de Babel
├── app.py                    # Aplicación principal
├── locales/                  # Carpeta de traducciones
│   ├── messages.pot          # Plantilla principal
│   ├── es/LC_MESSAGES/
│   │   ├── messages.po       # Traducciones en español
│   │   └── messages.mo       # Archivo compilado
│   └── ca/LC_MESSAGES/
│       ├── messages.po       # Traducciones en catalán
│       └── messages.mo       # Archivo compilado
└── templates/                # Plantillas HTML
    └── *.html
```

### 3. Configuración de `babel.cfg`

```ini
[python: **.py]
[jinja2: templates/**.html]
extensions=jinja2.ext.i18n
```

**¿Qué hace cada línea?**

- `[python: **.py]`: Escanea todos los archivos Python
- `[jinja2: templates/**.html]`: Escanea plantillas Jinja2 en la carpeta templates
- `extensions=jinja2.ext.i18n`: Habilita las funciones de traducción en Jinja2

---

## 🔄 Flujo de Trabajo Completo

### Paso 1: Marcar Cadenas para Traducir

**En archivos Python:**

```python
from flask_babel import gettext as _

# Marcar cadenas
mensaje = _("Bienvenido al sistema")
error = _("Usuario no encontrado")
```

**En plantillas HTML:**

```html
<h1>{{ _("Título de la página") }}</h1>
<p>{{ _("Descripción del contenido") }}</p>
```

### Paso 2: Extraer Cadenas

```bash
pybabel extract -F babel.cfg -o locales/messages.pot .
```

### Paso 3: Crear/Actualizar Traducciones

**Para un nuevo idioma:**

```bash
pybabel init -i locales/messages.pot -d locales -l es
```

**Para actualizar idiomas existentes:**

```bash
pybabel update -i locales/messages.pot -d locales
```

### Paso 4: Traducir Cadenas

Edita los archivos `.po` y completa las traducciones:

```po
#: templates/index.html:15
msgid "Welcome"
msgstr "Bienvenido"

#: app.py:25
msgid "User not found"
msgstr "Usuario no encontrado"
```

### Paso 5: Compilar Traducciones

```bash
pybabel compile -d locales
```

---

## 🛠️ Configuración en Flask

### Configuración Básica en `app.py`

```python
from flask import Flask, request
from flask_babel import Babel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta'

# Configuración de Babel
app.config.update(
    BABEL_DEFAULT_LOCALE='es',
    BABEL_DEFAULT_TIMEZONE='Europe/Madrid',
    LANGUAGES=['es', 'ca', 'en'],
    BABEL_TRANSLATION_DIRECTORIES='locales'
)

# Selector de idioma
def get_locale():
    return (
        request.args.get('lang') or
        request.accept_languages.best_match(app.config['LANGUAGES']) or
        'es'
    )

babel = Babel(app, locale_selector=get_locale)
```

### Cambio de Idioma en URLs

```html
<!-- Enlaces para cambiar idioma -->
<a href="?lang=es" class="btn btn-sm">Español</a>
<a href="?lang=ca" class="btn btn-sm">Català</a>
<a href="?lang=en" class="btn btn-sm">English</a>
```

---

## 🔧 Mini-Manuales para Errores Comunes

### ❌ Error: "No se encuentran nuevas cadenas"

**Síntomas:**

- Ejecutas `pybabel extract` pero las nuevas cadenas no aparecen en el `.pot`

**Causas posibles:**

1. **Función de traducción incorrecta**
2. **Configuración de `babel.cfg` incorrecta**
3. **Ruta de archivos incorrecta**

**✅ Soluciones:**

**1. Verificar funciones de traducción:**

```python
# ✅ CORRECTO
from flask_babel import gettext as _
titulo = _("Mi título")

# ❌ INCORRECTO
titulo = gettext("Mi título")  # Sin importar como _
```

**2. Verificar babel.cfg:**

```ini
# ✅ Para Flask con Jinja2
[python: **.py]
[jinja2: templates/**.html]
extensions=jinja2.ext.i18n

# ❌ Extensión incorrecta
[jinja2: templates/**.html]
extensions=jinja2.ext.autoescape  # Falta i18n
```

**3. Ejecutar desde la raíz del proyecto:**

```bash
# ✅ CORRECTO - desde la carpeta raíz
cd /ruta/a/tu/proyecto
pybabel extract -F babel.cfg -o locales/messages.pot .

# ❌ INCORRECTO - desde subcarpeta
cd /ruta/a/tu/proyecto/templates
pybabel extract -F babel.cfg -o locales/messages.pot .
```

---

### ❌ Error: "Traducciones no se aplican en la web"

**Síntomas:**

- Las cadenas siguen en el idioma original
- Los archivos `.po` están traducidos

**Causas posibles:**

1. **Archivos `.mo` no compilados**
2. **Configuración incorrecta en Flask**
3. **Ruta de `locales` incorrecta**

**✅ Soluciones:**

**1. Compilar traducciones:**

```bash
# Siempre después de editar .po
pybabel compile -d locales

# Verificar que se crean los .mo
ls locales/es/LC_MESSAGES/  # Debe mostrar messages.mo
```

**2. Verificar configuración Flask:**

```python
# ✅ CORRECTO
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'locales'

# ❌ INCORRECTO
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'  # Carpeta incorrecta
```

**3. Verificar estructura de carpetas:**

```Bash
locales/
├── es/LC_MESSAGES/
│   ├── messages.po
│   └── messages.mo  ← Este archivo es crucial
└── ca/LC_MESSAGES/
    ├── messages.po
    └── messages.mo  ← Este archivo es crucial
```

---

### ❌ Error: "UnicodeDecodeError" o caracteres extraños

**Síntomas:**

- Caracteres como "ñ", "ç", acentos se muestran incorrectamente
- Errores de codificación al compilar

**Causas posibles:**

1. **Codificación incorrecta en archivos `.po`**
2. **Editor de texto con codificación incorrecta**

**✅ Soluciones:**

**1. Verificar cabecera de archivos `.po`:**

```po
# ✅ CORRECTO
"Content-Type: text/plain; charset=utf-8\n"

# ❌ INCORRECTO
"Content-Type: text/plain; charset=iso-8859-1\n"
```

**2. Configurar editor correctamente:**

- **VS Code**: File → Preferences → Settings → `files.encoding` → UTF-8
- **Notepad++**: Encoding → UTF-8
- **Vim**: `:set encoding=utf-8`

**3. Forzar UTF-8 al compilar:**

```bash
pybabel compile -d locales --statistics
```

---

### ❌ Error: "Cadenas marcadas como obsoletas (#~)"

**Síntomas:**

- Traducciones aparecen con `#~` al principio
- Cadenas no se muestran traducidas

**Causas posibles:**

1. **Cadenas cambiadas en el código**
2. **Actualización automática de babel**

**✅ Soluciones:**

**1. Revisar cambios en el código:**

```python
# ✅ Si cambiaste esto:
_("Usuario logueado")
# ✅ Por esto:
_("Usuario autenticado")

# La cadena anterior se marca como obsoleta
```

**2. Limpiar cadenas obsoletas manualmente:**

```bash
# Editar archivos .po y eliminar líneas que empiecen con #~
```

**3. O regenerar desde cero:**

```bash
# ⚠️ CUIDADO: Esto borra todas las traducciones
rm locales/*/LC_MESSAGES/messages.po
pybabel init -i locales/messages.pot -d locales -l es
pybabel init -i locales/messages.pot -d locales -l ca
```

---

### ❌ Error: "babel.core.UnknownLocaleError"

**Síntomas:**

```Bash
babel.core.UnknownLocaleError: unknown locale 'ca'
```

**Causas posibles:**

1. **Código de idioma no estándar**
2. **Babel no reconoce el locale**

**✅ Soluciones:**

**1. Usar códigos estándar:**

```bash
# ✅ CORRECTO
pybabel init -i locales/messages.pot -d locales -l ca  # Catalán
pybabel init -i locales/messages.pot -d locales -l es  # Español

# ❌ INCORRECTO
pybabel init -i locales/messages.pot -d locales -l cat  # No estándar
```

**2. Verificar códigos disponibles:**

```python
# En Python
from babel import Locale
print(Locale('ca'))  # Debe funcionar sin error
```

---

## 🎯 Comandos Avanzados

### Extraer con opciones específicas

```bash
# Excluir directorios específicos
pybabel extract -F babel.cfg -o locales/messages.pot --no-location .

# Añadir comentarios automáticos
pybabel extract -F babel.cfg -o locales/messages.pot --add-comments=TRANSLATORS .

# Especificar palabras clave personalizadas
pybabel extract -F babel.cfg -k _ -k ngettext:1,2 -o locales/messages.pot .
```

### Actualizar con opciones

```bash
# Actualizar sin fuzzy matching (más conservador)
pybabel update -i locales/messages.pot -d locales --no-fuzzy-matching

# Mostrar estadísticas
pybabel update -i locales/messages.pot -d locales --statistics
```

### Compilar con verificaciones

```bash
# Compilar mostrando estadísticas
pybabel compile -d locales --statistics

# Compilar solo archivos modificados
pybabel compile -d locales --use-fuzzy
```

---

## 🔍 Herramientas de Debugging

### Verificar configuración actual

```python
# En tu aplicación Flask
from flask_babel import get_locale
print(f"Idioma actual: {get_locale()}")

# Ver configuración de Babel
print(app.config['BABEL_DEFAULT_LOCALE'])
print(app.config['LANGUAGES'])
```

### Comprobar traducciones cargadas

```python
from flask_babel import gettext as _
# En una vista o shell
print(_("Cadena de prueba"))  # Debe mostrar la traducción
```

### Script de verificación

```python
# check_translations.py
import os
from pathlib import Path

def check_translation_files():
    locales_dir = Path('locales')
    languages = ['es', 'ca']

    for lang in languages:
        po_file = locales_dir / lang / 'LC_MESSAGES' / 'messages.po'
        mo_file = locales_dir / lang / 'LC_MESSAGES' / 'messages.mo'

        print(f"\n--- {lang.upper()} ---")
        print(f"PO existe: {po_file.exists()}")
        print(f"MO existe: {mo_file.exists()}")

        if po_file.exists() and mo_file.exists():
            po_time = po_file.stat().st_mtime
            mo_time = mo_file.stat().st_mtime
            print(f"MO actualizado: {'✅' if mo_time >= po_time else '❌ Recompilar'}")

if __name__ == '__main__':
    check_translation_files()
```

---

## 📋 Checklist de Verificación

### ✅ Antes de hacer commit

- [ ] Todas las cadenas marcadas con `_()`
- [ ] `babel.cfg` configurado correctamente
- [ ] Plantilla `.pot` actualizada
- [ ] Archivos `.po` traducidos
- [ ] Archivos `.mo` compilados
- [ ] Probado en navegador con diferentes idiomas

### ✅ Para deployment

- [ ] Solo archivos `.mo` en producción (opcional: excluir `.po`)
- [ ] Variables de entorno configuradas
- [ ] Rutas de `locales` correctas en servidor

---

## 📚 Recursos Adicionales

### Editores Recomendados

- **Poedit**: Editor gráfico específico para archivos `.po`
- **VS Code**: Con extensión "gettext"
- **Lokalize**: Editor avanzado para KDE

### Referencias Online

- [Documentación oficial de Babel](https://babel.pocoo.org/)
- [Flask-Babel Documentation](https://flask-babel.tkte.ch/)
- [GNU gettext manual](https://www.gnu.org/software/gettext/manual/)

### Automatización

```bash
# Script completo de actualización
#!/bin/bash
echo "🔄 Actualizando traducciones..."
pybabel extract -F babel.cfg -o locales/messages.pot .
pybabel update -i locales/messages.pot -d locales
echo "✅ Listo para traducir. Ejecuta 'pybabel compile -d locales' después de traducir."
```

---

## 💡 Consejos Finales

1. **Automatiza el proceso**: Crea scripts para extraer, actualizar y compilar
2. **Versionado**: Incluye archivos `.po` en git, pero considera excluir `.mo`
3. **Contexto**: Añade comentarios para traducciones ambiguas
4. **Pruebas**: Siempre prueba con diferentes idiomas antes del deployment
5. **Backup**: Guarda copias de archivos `.po` antes de regeneraciones masivas

---

_Este documento debe actualizarse según evolucione tu proyecto. ¡Mantén siempre la documentación sincronizada con tu implementación!_
