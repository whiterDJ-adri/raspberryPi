from marshmallow import Schema, fields


class RecordCameraSchema(Schema):
    filename = fields.String(required=True)
    date = fields.String(required=True)
    path_file = fields.String(required=True)


# class UsuarioSchema(Schema):
#     id = fields.Str(dump_only=True)
#     name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
#     email = fields.Email(required=True)
#     age = fields.Int(validate=validate.Range(min=0, max=120))
#     created_at = fields.DateTime(dump_only=True)

record_camera_schema = RecordCameraSchema()
records_camera_schema = RecordCameraSchema(many=True)
