# FALTA: Control de errores en la aplicación principal
# - Verificar que las variables de entorno estén configuradas
# - Manejar errores de conexión a MongoDB al inicio
# - Logging para errores de producción
# - Configuración de error handlers globales

# from flask_babel import Babel, gettext as _
import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_babel import Babel

from routes.record_camera import record_cam_bp
from routes.login import login_bp
from routes.dashboard import dashboard_bp

from services.remove_photos import detect_photos_exists

app = Flask(__name__)

# --- Verificar variables de entorno requeridas ---
required_env_vars = ["URL_MONGO", "WEBHOOK_DISCORD"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Error: Variables de entorno faltantes: {missing_vars}")
    exit(1)

# --- Mongo ---
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "tu-clave-secreta-temporal")
app.config["MONGO_URI"] = os.getenv("URL_MONGO")

try:
    mongo = PyMongo(app)
    app.mongo = mongo
    # Verificar conexión a MongoDB con múltiples métodos
    try:
        # Método 1: comando ping
        mongo.db.command("ping")
        print("✅ Conexión a MongoDB exitosa")
    except Exception:
        # Método 2: verificación alternativa listando collections
        try:
            list(mongo.db.list_collection_names(limit=1))
            print("✅ Conexión a MongoDB exitosa (método alternativo)")
        except Exception:
            raise Exception("No se pudo verificar la conexión a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    print("Verifica que:")
    print("   - La variable URL_MONGO esté configurada correctamente")
    print("   - MongoDB esté ejecutándose")
    print("   - Las credenciales sean correctas")
    exit(1)


# --- Config i18n ---
app.config.update(
    BABEL_DEFAULT_LOCALE="es",
    BABEL_DEFAULT_TIMEZONE="Europe/Madrid",
    LANGUAGES=["es", "ca"],
    BABEL_TRANSLATION_DIRECTORIES="locales",
)


# Selectores (Flask-Babel 4.x)
def select_locale():
    return (
        request.args.get("lang")
        or request.accept_languages.best_match(app.config["LANGUAGES"])
        or "es"
    )


babel = Babel(app, locale_selector=select_locale, timezone_selector="Europe/Madrid")


# --- Rutas ---
# FALTA: Error handler para la ruta principal
# - Manejar errores en detect_photos_exists que podrían fallar
@app.route("/")
def main():
    try:
        detect_photos_exists()
    except Exception as e:
        print(f"Error al detectar fotos: {e}")
        # No fallar la página principal por esto
    return render_template("index.html")


# FALTA: Error handlers globales para la aplicación
# - Handler para errores 404, 500, etc.
# - Logging estructurado de errores
# - ACTUALIZADO: Ahora usa traducciones desde el template
@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html", error_code=404), 404


@app.errorhandler(500)
def internal_error(error):
    print(f"Error interno del servidor: {error}")
    return render_template("error.html", error_code=500), 500


@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Error no manejado: {e}")
    return render_template("error.html", error_code=500), 500


app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(record_cam_bp, url_prefix="/api/photo")

if __name__ == "__main__":
    app.run(debug=True)
