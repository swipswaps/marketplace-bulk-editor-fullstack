"""
OCR routes
"""
import time
from datetime import datetime
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.user import db
from models.ocr_scan import OCRScan
from schemas.ocr_schema import OCRScanSchema, OCRUploadSchema, OCRCorrectionSchema
from utils.auth import token_required
from utils.file_upload import save_upload_file, delete_upload_file
from utils.audit import log_action

ocr_bp = Blueprint('ocr', __name__)

ocr_scan_schema = OCRScanSchema()
ocr_scans_schema = OCRScanSchema(many=True)
ocr_upload_schema = OCRUploadSchema()
ocr_correction_schema = OCRCorrectionSchema()


@ocr_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    """Upload file for OCR processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save file
        file_path = save_upload_file(file, 'ocr')
        file_size = file.tell()
        
        # Create OCR scan record
        ocr_scan = OCRScan(
            user_id=current_user.id,
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type,
            status='pending'
        )
        
        db.session.add(ocr_scan)
        db.session.commit()
        
        log_action(current_user.id, 'upload_ocr_file', 'ocr_scan', ocr_scan.id, 201)
        
        # TODO: Queue OCR processing task (implement in Phase 3)
        # For now, return pending status
        
        return jsonify({
            'message': 'File uploaded successfully',
            'ocr_scan': ocr_scan_schema.dump(ocr_scan)
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Upload failed', 'details': str(e)}), 500


@ocr_bp.route('/scans', methods=['GET'])
@token_required
def get_scans(current_user):
    """Get OCR scan history"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    per_page = min(per_page, 100)
    
    pagination = OCRScan.query.filter_by(user_id=current_user.id).order_by(
        OCRScan.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'scans': ocr_scans_schema.dump(pagination.items),
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200


@ocr_bp.route('/scans/<scan_id>', methods=['GET'])
@token_required
def get_scan(current_user, scan_id):
    """Get OCR scan by ID"""
    ocr_scan = OCRScan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    
    if not ocr_scan:
        return jsonify({'error': 'OCR scan not found'}), 404
    
    return jsonify(ocr_scan_schema.dump(ocr_scan)), 200


@ocr_bp.route('/scans/<scan_id>/correct', methods=['POST'])
@token_required
def correct_scan(current_user, scan_id):
    """Manually correct OCR results"""
    ocr_scan = OCRScan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    
    if not ocr_scan:
        return jsonify({'error': 'OCR scan not found'}), 404
    
    try:
        data = ocr_correction_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    try:
        ocr_scan.extracted_data = data['corrected_data']
        ocr_scan.status = 'corrected'
        db.session.commit()
        
        log_action(current_user.id, 'correct_ocr_scan', 'ocr_scan', scan_id, 200)
        
        return jsonify({
            'message': 'OCR scan corrected successfully',
            'ocr_scan': ocr_scan_schema.dump(ocr_scan)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Correction failed', 'details': str(e)}), 500


@ocr_bp.route('/scans/<scan_id>', methods=['DELETE'])
@token_required
def delete_scan(current_user, scan_id):
    """Delete OCR scan"""
    ocr_scan = OCRScan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    
    if not ocr_scan:
        return jsonify({'error': 'OCR scan not found'}), 404
    
    try:
        # Delete file
        if ocr_scan.file_path:
            delete_upload_file(ocr_scan.file_path)
        
        db.session.delete(ocr_scan)
        db.session.commit()
        
        log_action(current_user.id, 'delete_ocr_scan', 'ocr_scan', scan_id, 200)
        
        return jsonify({'message': 'OCR scan deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Deletion failed', 'details': str(e)}), 500

