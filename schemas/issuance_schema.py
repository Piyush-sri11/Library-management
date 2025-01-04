from marshmallow import Schema, fields

class IssueSchema(Schema):
    issue_id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    issue_date = fields.Date(required=True)
    return_date = fields.Date(required=True)
    actual_return_date = fields.Date()
    #set late_fine at time of isuuance
    late_fine = fields.Float()
    status = fields.Str(required=True, validate=lambda s: s in ["issued", "returned", "overdue"])