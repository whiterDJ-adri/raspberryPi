from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    nombre = fields.String(required=True)
    edad = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

class RecordCamera(Schema):
    codigo = fields.String(Required=True)
    date = fields.String(required=True)
    type = fields.String(required=True)
    url_img = fields.String(required=True)
    personal = fields.String(required=True)
