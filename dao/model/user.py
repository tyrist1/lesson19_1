from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

class UserSchema(Schema):
    id = fields.Int(required=True)
    password = fields.Str(required=True)
    role = fields.Int()
    username = fields.Str()

