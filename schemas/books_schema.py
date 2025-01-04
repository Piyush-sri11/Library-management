from marshmallow import Schema, fields

class BookSchema(Schema):
    book_id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    genre = fields.Str(required=True)
    quantity = fields.Int()
    late_fee = fields.Float(required=True)  # Late fee per day