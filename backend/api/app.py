import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_babel import Babel, get_locale, gettext as _ 
from routes.record_camera import record_cam_bp
from routes.login import login_bp

app = Flask(__name__)

# --- Mongo ---
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


def select_timezone():
    return "Europe/Madrid"


babel = Babel(app, locale_selector=select_locale, timezone_selector=select_timezone)



# --- Rutas ---
@app.route("/")
def main():
    # Ejemplo: textos marcados en Python (opcional; en plantillas también puedes marcar)
    titulo = _("Panel de cámara")
    return render_template("index.html", titulo=titulo)


app.register_blueprint(record_cam_bp, url_prefix="/api/photo")
app.register_blueprint(login_bp, url_prefix="/login")

if __name__ == "__main__":
    app.run(debug=True)
