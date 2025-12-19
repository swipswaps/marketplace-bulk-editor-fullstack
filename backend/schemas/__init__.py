"""
Marshmallow schemas for input validation and serialization
"""
from .user_schema import UserSchema, LoginSchema, RegisterSchema, PasswordResetSchema
from .listing_schema import ListingSchema, ListingCreateSchema, ListingUpdateSchema
from .template_schema import TemplateSchema, TemplateCreateSchema
from .ocr_schema import OCRScanSchema, OCRUploadSchema

__all__ = [
    'UserSchema',
    'LoginSchema',
    'RegisterSchema',
    'PasswordResetSchema',
    'ListingSchema',
    'ListingCreateSchema',
    'ListingUpdateSchema',
    'TemplateSchema',
    'TemplateCreateSchema',
    'OCRScanSchema',
    'OCRUploadSchema'
]

