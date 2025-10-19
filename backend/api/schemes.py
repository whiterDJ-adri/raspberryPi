from marshmallow import Schema, fields, validate


# FALTA: Validaciones más específicas en el esquema
# - Validar formato de fecha más estrictamente
# - Validar extensiones de archivo permitidas
# - Validar que el path del archivo sea seguro
class RecordCameraSchema(Schema):
    filename = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "El nombre del archivo es requerido"},
    )
    date = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "La fecha es requerida"},
    )
    file_path = fields.String(
        required=True,
        validate=validate.Length(min=1, max=500),
        error_messages={"required": "La ruta del archivo es requerida"},
    )


# FALTA: Validaciones de seguridad en contraseñas
# - Validar complejidad de contraseña (mayúsculas, números, etc.)
# - Validar que el nombre no contenga caracteres especiales peligrosos
class UserSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "El nombre es requerido"},
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El email es requerido",
            "invalid": "Formato de email inválido",
        },
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=24),
        error_messages={
            "required": "La contraseña es requerida",
            "length": "La contraseña debe tener entre 8 y 24 caracteres",
        },
    )
    isAdmin = fields.Boolean(
        required=True, error_messages={"required": "El campo isAdmin es requerido"}
    )


record_camera_schema = RecordCameraSchema()
records_camera_schema = RecordCameraSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
