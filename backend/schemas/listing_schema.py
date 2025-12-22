"""
Listing validation schemas
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class ListingSchema(Schema):
    """Listing serialization schema"""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    price = fields.Decimal(required=True, as_string=True, places=2)
    condition = fields.Str(required=True, validate=validate.OneOf([
        'New', 'Used - Like New', 'Used - Good', 'Used - Fair'
    ]))
    description = fields.Str(allow_none=True)
    category = fields.Str(allow_none=True, validate=validate.Length(max=100))
    offer_shipping = fields.Str(allow_none=True, validate=validate.OneOf(['Yes', 'No']))
    source = fields.Str(dump_only=True)
    ocr_scan_id = fields.Str(allow_none=True)
    extra_data = fields.Dict(allow_none=True)  # Renamed from metadata to avoid SQLAlchemy conflict (Rule 16)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('price')
    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise ValidationError('Price must be greater than 0')


class ListingCreateSchema(Schema):
    """Listing creation schema (also used for upsert - id is optional)"""
    id = fields.Str(allow_none=True)  # Optional: if provided, will update existing listing (upsert)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    price = fields.Decimal(required=True, as_string=True, places=2)
    condition = fields.Str(required=True, validate=validate.OneOf([
        'New', 'Used - Like New', 'Used - Good', 'Used - Fair'
    ]))
    description = fields.Str(allow_none=True)
    category = fields.Str(allow_none=True, validate=validate.Length(max=100))
    offer_shipping = fields.Str(allow_none=True, validate=validate.OneOf(['Yes', 'No']))
    source = fields.Str(allow_none=True, validate=validate.OneOf(['manual', 'ocr', 'import']))
    ocr_scan_id = fields.Str(allow_none=True)
    extra_data = fields.Dict(allow_none=True)  # Renamed from metadata to avoid SQLAlchemy conflict (Rule 16)

    @validates('price')
    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise ValidationError('Price must be greater than 0')


class ListingUpdateSchema(Schema):
    """Listing update schema (all fields optional)"""
    title = fields.Str(validate=validate.Length(min=1, max=150))
    price = fields.Decimal(as_string=True, places=2)
    condition = fields.Str(validate=validate.OneOf([
        'New', 'Used - Like New', 'Used - Good', 'Used - Fair'
    ]))
    description = fields.Str(allow_none=True)
    category = fields.Str(allow_none=True, validate=validate.Length(max=100))
    offer_shipping = fields.Str(allow_none=True, validate=validate.OneOf(['Yes', 'No']))
    extra_data = fields.Dict(allow_none=True)  # Renamed from metadata to avoid SQLAlchemy conflict (Rule 16)
    
    @validates('price')
    def validate_price(self, value):
        """Validate price is positive"""
        if value is not None and value <= 0:
            raise ValidationError('Price must be greater than 0')


class BulkListingCreateSchema(Schema):
    """Bulk listing creation schema"""
    listings = fields.List(fields.Nested(ListingCreateSchema), required=True, validate=validate.Length(min=1, max=100))


class BulkListingDeleteSchema(Schema):
    """Bulk listing deletion schema"""
    listing_ids = fields.List(fields.Str(), required=True, validate=validate.Length(min=1, max=100))

