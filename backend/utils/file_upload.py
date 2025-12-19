"""
File upload utilities
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def validate_file_size(file):
    """Validate file size"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= current_app.config['MAX_FILE_SIZE']


def save_upload_file(file, subfolder=''):
    """Save uploaded file and return path"""
    if not file:
        return None
    
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed')
    
    if not validate_file_size(file):
        raise ValueError('File size exceeds maximum allowed size')
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    # Create subfolder if needed
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_path, unique_filename)
    file.save(file_path)
    
    return file_path


def delete_upload_file(file_path):
    """Delete uploaded file"""
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    return False

