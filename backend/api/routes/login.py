from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    render_template,
    session,
    redirect,
    url_for,
)
from schemes import user_schema
from controllers.login_bd import LoginController

login_bp = Blueprint("login", __name__)


def get_login_controller():
    return LoginController(current_app.mongo)


@login_bp.route("/", methods=["GET"])
def show_page_login():
    if "email" in session:
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


# FALTA: Control de errores más robusto
# - Validar que los datos JSON existen y tienen el formato correcto
# - Manejar errores de base de datos (conexión, timeouts)
# - Validar que email y password no estén vacíos
# - Logs para auditoría de intentos de login
@login_bp.route("/login", methods=["POST"])
def login():
    try:
        # Verificar que el request tiene contenido JSON
        if not request.is_json:
            return jsonify({"message": "Content-Type debe ser application/json"}), 400

        data = request.json
        if not data:
            return jsonify({"message": "No se recibieron datos"}), 400

        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        # Validar que los campos no estén vacíos
        if not email or not password:
            return jsonify({"message": "Email y contraseña son requeridos"}), 400

        controller = get_login_controller()

        try:
            user = controller.get_user(email)
        except Exception as e:
            print(f"Error al consultar usuario: {e}")
            return jsonify({"message": "Error interno del servidor"}), 500

        if user is None:
            return jsonify({"message": "Invalid credentials"}), 401

        if user.get("password") != password:
            return jsonify({"message": "Invalid credentials"}), 401

        session["email"] = email
        session["isAdmin"] = user.get("isAdmin", False)

        return jsonify(
            {
                "message": "Log in successful",
                "redirect": url_for("dashboard.dashboard"),
                "status": 200,
            }
        )

    except Exception as e:
        print(f"Error inesperado en login: {e}")
        return jsonify({"message": "Error interno del servidor"}), 500


# FALTA: Control de errores en validación de datos
# - Manejar errores de validación de Marshmallow más específicamente
# - Verificar errores de base de datos al crear usuario
# - Logs para auditoría de creación de usuarios
@login_bp.route("/signup", methods=["POST"])
def signup():
    try:
        if not request.is_json:
            return jsonify({"message": "Content-Type debe ser application/json"}), 400

        data = request.json
        if not data:
            return jsonify({"message": "No se recibieron datos"}), 400

        try:
            validated_data = user_schema.load(data)
        except Exception as e:
            return jsonify({"message": f"Datos inválidos: {str(e)}"}), 400

        data_email = validated_data.get("email")

        login_controller = get_login_controller()

        try:
            existing_user = login_controller.get_user(data_email)
        except Exception as e:
            print(f"Error al verificar usuario existente: {e}")
            return jsonify({"message": "Error interno del servidor"}), 500

        if existing_user is not None:
            return jsonify({"message": "User already exists"}), 400

        try:
            login_controller.create_user(validated_data)
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return jsonify({"message": "Error al crear usuario"}), 500

        return jsonify(
            {
                "message": "User created succesfully",
                "redirect": url_for("login.show_page_login"),
                "status": 201,
            }
        )

    except Exception as e:
        print(f"Error inesperado en signup: {e}")
        return jsonify({"message": "Error interno del servidor"}), 500


@login_bp.route("/logout")
def logout():
    session.clear()
    return jsonify(
        {
            "message": "Logout successfully",
            "redirect": url_for("login.show_page_login"),
            "status": 200,
        }
    )


# FALTA: Control de errores más específico
# - Manejar errores de base de datos al eliminar usuario
# - Validar formato del email antes de procesar
@login_bp.route("/delete", methods=["POST"])
def delete_use():
    try:
        if not request.is_json:
            return jsonify({"message": "Content-Type debe ser application/json"}), 400

        data = request.json
        if not data:
            return jsonify({"message": "No se recibieron datos"}), 400

        email = data.get("email", "").strip()

        if not email:
            return jsonify({"message": "Email es requerido"}), 400

        # Verifica si hay sesión activa
        current_email = session.get("email")
        if not current_email:
            return jsonify({"message": "Sesión no iniciada."}), 401

        # Impide que un admin se elimine a sí mismo
        if email == current_email:
            return jsonify({"message": "No puedes eliminar tu propio usuario."}), 403

        login_controller = get_login_controller()

        try:
            # Verificar que el usuario existe antes de eliminarlo
            user_to_delete = login_controller.get_user(email)
            if not user_to_delete:
                return jsonify({"message": "Usuario no encontrado"}), 404

            login_controller.delete_user(email)
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return jsonify({"message": "Error al eliminar usuario"}), 500

        return jsonify({"message": "User deleted succefully", "status": 200})

    except Exception as e:
        print(f"Error inesperado en delete_user: {e}")
        return jsonify({"message": "Error interno del servidor"}), 500


# FALTA: Control de errores en consulta de usuarios
# - Manejar errores de base de datos al obtener lista de usuarios
@login_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        login_controller = get_login_controller()

        try:
            users = login_controller.get_all_users()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return jsonify({"message": "Error al obtener lista de usuarios"}), 500

        user_list = [
            {
                "name": user.get("name", "Sin nombre"),
                "email": user.get("email"),
                "isAdmin": user.get("isAdmin", False),
            }
            for user in users
        ]

        return jsonify(user_list)

    except Exception as e:
        print(f"Error inesperado en get_all_users: {e}")
        return jsonify({"message": "Error interno del servidor"}), 500
