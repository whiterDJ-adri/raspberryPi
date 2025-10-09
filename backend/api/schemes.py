from marshmallow import Schema, fields, validate


class RecordCameraSchema(Schema):
    filename = fields.String(required=True)
    date = fields.String(required=True)
    file_path = fields.String(required=True)


class UserSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=24))

record_camera_schema = RecordCameraSchema()
records_camera_schema = RecordCameraSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)