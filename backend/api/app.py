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

# --- Mongo ---
app.config["SECRET_KEY"] = "tu-clave-secreta"
app.config["MONGO_URI"] = os.getenv("URL_MONGO")
mongo = PyMongo(app)
app.mongo = mongo


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
@app.route("/")
def main():
    detect_photos_exists()
    return render_template("index.html")


app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(record_cam_bp, url_prefix="/api/photo")

if __name__ == "__main__":
    app.run(debug=True)
