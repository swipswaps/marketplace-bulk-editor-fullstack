"""
OCR validation schemas
"""
from marshmallow import Schema, fields, validate


class OCRScanSchema(Schema):
    """OCR scan serialization schema"""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    filename = fields.Str(required=True)
    file_size = fields.Int()
    file_type = fields.Str()
    status = fields.Str(dump_only=True)
    ocr_text = fields.Str(dump_only=True)
    extracted_data = fields.Dict(dump_only=True)
    error_message = fields.Str(dump_only=True)
    processing_time = fields.Float(dump_only=True)
    items_extracted = fields.Int(dump_only=True)
    confidence_score = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(dump_only=True)


class OCRUploadSchema(Schema):
    """OCR upload validation schema"""
    # File will be validated separately in the route
    process_immediately = fields.Bool(missing=True)


class OCRCorrectionSchema(Schema):
    """OCR correction schema"""
    corrected_data = fields.Dict(required=True)

