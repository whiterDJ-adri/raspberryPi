# Documentación de internacionalización (pybabel)

## Resumen rápido

Comandos frecuentes:

```bash
pybabel extract -F babel.cfg -o locales/messages.pot .
pybabel update -i locales/messages.pot -d locales
pybabel compile -d locales
```

## Objetivo

Describir un flujo de trabajo completo para extraer cadenas, gestionar archivos de traducción y generar archivos binarios utilizables en tiempo de ejecución utilizando pybabel.

## Requisitos previos

- Tener instalado Babel (pybabel): `pip install Babel`
- Código marcado con las funciones/keywords de traducción (por ejemplo `gettext`: `_("texto")`).
- Un fichero de configuración `babel.cfg` que indique qué archivos escanear y qué marcadores usar.

## Estructura recomendada de directorios

Ejemplo:

```Bash
locales/            # contenedor de PO/MO y plantillas
    messages.pot    # plantilla extraída (PO template)
    es/LC_MESSAGES/
        messages.po
        messages.mo
    fr/LC_MESSAGES/
        messages.po
        messages.mo
src/                # código fuente que contiene llamadas a gettext
```

## Ejemplo de `babel.cfg`

```ini
[python: **.py]
[jinja2: templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

Ajusta los patrones según tu proyecto (scripts, plantillas, rutas).

## Flujo de trabajo típico

1. Extraer cadenas a una plantilla (.pot).
2. Inicializar un nuevo idioma (si es necesario).
3. Actualizar los archivos `.po` existentes con cambios de la plantilla.
4. Compilar los `.po` a `.mo` para que el software los use.

## Inicializar un nuevo idioma

Después de extraer la plantilla, crea el archivo `.po` inicial de un idioma:

```bash
pybabel init -i locales/messages.pot -d locales -l es
```

Esto crea `locales/es/LC_MESSAGES/messages.po` para que los traductores empiecen a trabajar.

## Actualizar traducciones existentes

Cuando cambie el código y vuelvas a extraer cadenas, aplica los cambios a los `.po` existentes:

```bash
pybabel update -i locales/messages.pot -d locales
```

Esto añade nuevas cadenas y marca como obsoletas las que ya no existen.

## Compilar traducciones

Para que la aplicación cargue las traducciones en tiempo de ejecución, compila los `.po` a `.mo`:

```bash
pybabel compile -d locales
```

Los archivos `.mo` resultantes son los que usan las librerías de i18n en tiempo de ejecución.

## Edición de archivos .po

- Editores recomendados: Poedit (GUI) o editores de texto (vim/emacs/VS Code).
- Cada entrada contiene `msgid` (original) y `msgstr` (traducción). Mantén el contexto y comentarios para aclarar significados.

## Integración rápida en la aplicación

- Asegúrate de cargar las traducciones según tu framework (Flask-Babel, Django o `gettext` directo).
- Ejemplo conceptual:
  - Marcar cadenas en código: `_("Hello world")`
    - Configurar el cargador de idiomas para que busque en `locales/`.

## Buenas prácticas

- Extrae frecuentemente durante el desarrollo para mantener la plantilla actualizada.
- Mantén una convención de nombres clara para los dominios y plantillas (por ejemplo `messages`).
- Versiona los archivos `.po` en el control de código; normalmente se ignoran los `.mo` (añadir a `.gitignore`).
- Añade comentarios de contexto en el código cuando la traducción pueda ser ambigua: `# TRANSLATORS: explicación`

## Solución de problemas comunes

- **"No aparecen nuevas cadenas en .po"**: comprueba que `babel.cfg` cubre los archivos que contienen las cadenas y que usas las funciones/keywords correctas.
- **"Cadena marcada como obsoleta"**: fue removida o cambiada en el código; revisa si debe restaurarse o eliminarse.
- **"Archivos .mo no actualizados"**: asegúrate de ejecutar la compilación y de que la ruta de `locales/` es la misma que usa tu app.
- **Problemas de encoding**: los archivos `.po` están en UTF-8 por defecto; verifica la configuración del editor.

## Consejos adicionales

- Automatiza extracción/actualización/compilación con scripts o tareas de CI antes del despliegue.
- Usa `pybabel extract --help` y `pybabel <comando> --help` para ver opciones avanzadas (excluir directorios, cambiar dominio, etc.).
- Para proyectos grandes, considera dividir dominios de mensajes por componente o módulo.

## Referencias

- Documentación oficial de Babel: <https://babel.pocoo.org/>
- Herramientas de edición: Poedit, Lokalise, Weblate

Mantén este documento actualizado según cambien las rutas y convenciones de tu proyecto.
