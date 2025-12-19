"""
Template validation schemas
"""
from marshmallow import Schema, fields, validate


class TemplateSchema(Schema):
    """Template serialization schema"""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    template_data = fields.Dict(required=True)
    is_public = fields.Bool()
    use_count = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TemplateCreateSchema(Schema):
    """Template creation schema"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    template_data = fields.Dict(required=True)
    is_public = fields.Bool(missing=False)


class TemplateUpdateSchema(Schema):
    """Template update schema (all fields optional)"""
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    template_data = fields.Dict()
    is_public = fields.Bool()

