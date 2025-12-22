"""
OCR Processing Utilities
Enhanced with PaddleOCR + Tesseract fallback, optimized sharpening, multi-resolution testing
"""

import os
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

logger = logging.getLogger(__name__)

# Try to import PaddleOCR (optional dependency)
try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
    logger.info("PaddleOCR is available")
except ImportError:
    PADDLE_AVAILABLE = False
    logger.warning("PaddleOCR not available, will use Tesseract fallback")

# Try to import pytesseract (fallback)
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    logger.info("Tesseract is available")
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.error("Neither PaddleOCR nor Tesseract is available!")


def preprocess_image_enhanced(image_path: str, output_dir: str) -> List[str]:
    """
    Enhanced image preprocessing with multiple techniques:
    1. Original (baseline)
    2. Sharpened (PIL ImageFilter.SHARPEN - Rule 7)
    3. Multi-resolution (test at 150%, 200% for small text)
    4. Enhanced contrast + sharpening
    
    Returns list of preprocessed image paths to test
    """
    img = Image.open(image_path)
    
    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    preprocessed_paths = []
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # 1. Original (baseline)
    original_path = os.path.join(output_dir, f"{base_name}_original.png")
    img.save(original_path)
    preprocessed_paths.append(('original', original_path))
    
    # 2. Sharpened (Rule 7: OCR Best Practices)
    sharpened = img.filter(ImageFilter.SHARPEN)
    sharpened_path = os.path.join(output_dir, f"{base_name}_sharpened.png")
    sharpened.save(sharpened_path)
    preprocessed_paths.append(('sharpened', sharpened_path))
    
    # 3. Enhanced sharpening (apply SHARPEN twice for better results)
    enhanced_sharp = img.filter(ImageFilter.SHARPEN).filter(ImageFilter.SHARPEN)
    enhanced_sharp_path = os.path.join(output_dir, f"{base_name}_enhanced_sharp.png")
    enhanced_sharp.save(enhanced_sharp_path)
    preprocessed_paths.append(('enhanced_sharp', enhanced_sharp_path))
    
    # 4. Contrast + Sharpening
    enhancer = ImageEnhance.Contrast(img)
    contrasted = enhancer.enhance(1.5)
    contrast_sharp = contrasted.filter(ImageFilter.SHARPEN)
    contrast_sharp_path = os.path.join(output_dir, f"{base_name}_contrast_sharp.png")
    contrast_sharp.save(contrast_sharp_path)
    preprocessed_paths.append(('contrast_sharp', contrast_sharp_path))
    
    # 5. Multi-resolution: 150% (for small text)
    width, height = img.size
    if width < 2000 or height < 2000:  # Only upscale if image is small
        upscaled_150 = img.resize((int(width * 1.5), int(height * 1.5)), Image.Resampling.LANCZOS)
        upscaled_150_sharp = upscaled_150.filter(ImageFilter.SHARPEN)
        upscaled_150_path = os.path.join(output_dir, f"{base_name}_150pct_sharp.png")
        upscaled_150_sharp.save(upscaled_150_path)
        preprocessed_paths.append(('150pct_sharp', upscaled_150_path))
    
    # 6. Multi-resolution: 200% (for very small text)
    if width < 1500 or height < 1500:  # Only upscale if image is very small
        upscaled_200 = img.resize((int(width * 2.0), int(height * 2.0)), Image.Resampling.LANCZOS)
        upscaled_200_sharp = upscaled_200.filter(ImageFilter.SHARPEN)
        upscaled_200_path = os.path.join(output_dir, f"{base_name}_200pct_sharp.png")
        upscaled_200_sharp.save(upscaled_200_path)
        preprocessed_paths.append(('200pct_sharp', upscaled_200_path))
    
    logger.info(f"Created {len(preprocessed_paths)} preprocessed versions for testing")
    return preprocessed_paths


def process_with_paddleocr(image_path: str) -> Tuple[str, float, List[Dict[str, Any]]]:
    """
    Process image with PaddleOCR (using receipts-ocr's working code)
    Returns: (raw_text, confidence, blocks)
    """
    if not PADDLE_AVAILABLE:
        raise RuntimeError("PaddleOCR is not available")

    # Initialize PaddleOCR (receipts-ocr pattern)
    ocr = PaddleOCR(
        lang="en",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        text_det_limit_side_len=2560,
        text_det_limit_type="max",
        text_det_thresh=0.3,
        text_det_box_thresh=0.5,
    )

    # Read image with OpenCV (receipts-ocr pattern)
    import cv2
    img = cv2.imread(image_path)
    if img is None:
        return "", 0.0, []

    # Run OCR (receipts-ocr pattern - uses predict(), not ocr())
    result = ocr.predict(img)

    if not result or len(result) == 0:
        return "", 0.0, []

    # Extract results from PaddleOCR predict() response (receipts-ocr pattern)
    ocr_result = result[0]
    rec_texts = ocr_result.get("rec_texts", [])
    rec_scores = ocr_result.get("rec_scores", [])
    dt_polys = ocr_result.get("dt_polys", [])

    if not rec_texts:
        return "", 0.0, []

    # Build blocks (receipts-ocr pattern)
    lines = []
    blocks = []
    total_confidence = 0.0

    for i, text in enumerate(rec_texts):
        confidence = rec_scores[i] if i < len(rec_scores) else 0.0
        box = dt_polys[i].tolist() if i < len(dt_polys) else []

        lines.append(text)
        blocks.append({
            'text': text,
            'confidence': float(confidence),
            'box': box
        })
        total_confidence += confidence

    raw_text = '\n'.join(lines)
    avg_confidence = total_confidence / len(rec_texts) if rec_texts else 0.0

    return raw_text, float(avg_confidence), blocks


def process_with_tesseract(image_path: str) -> Tuple[str, float]:
    """
    Process image with Tesseract
    Returns: (raw_text, confidence)
    """
    if not TESSERACT_AVAILABLE:
        raise RuntimeError("Tesseract is not available")
    
    img = Image.open(image_path)
    raw_text = pytesseract.image_to_string(img)
    
    # Get confidence from Tesseract
    try:
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        confidences = [c for c in data['conf'] if c != -1]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    except:
        avg_confidence = 0.0
    
    return raw_text, avg_confidence / 100.0  # Normalize to 0-1


def process_image_multi_method(image_path: str, temp_dir: str) -> Dict[str, Any]:
    """
    Process image with multiple preprocessing methods and choose best result
    
    Strategy:
    1. Try PaddleOCR on all preprocessed versions
    2. If PaddleOCR fails, fall back to Tesseract
    3. Choose result with highest confidence and most text
    """
    start_time = time.time()
    
    # Create preprocessed versions
    preprocessed_images = preprocess_image_enhanced(image_path, temp_dir)
    
    best_result = None
    best_score = 0.0
    method_used = None
    
    # Try PaddleOCR first
    if PADDLE_AVAILABLE:
        for method_name, prep_path in preprocessed_images:
            try:
                raw_text, confidence, blocks = process_with_paddleocr(prep_path)
                # Score = confidence * text_length (prefer more text with good confidence)
                score = confidence * len(raw_text)
                
                logger.info(f"PaddleOCR ({method_name}): confidence={confidence:.2f}, text_len={len(raw_text)}, score={score:.2f}")
                
                if score > best_score:
                    best_score = score
                    best_result = {
                        'raw_text': raw_text,
                        'confidence': confidence,
                        'blocks': blocks,
                        'method': f'paddleocr_{method_name}'
                    }
                    method_used = f'paddleocr_{method_name}'
            except Exception as e:
                logger.warning(f"PaddleOCR failed on {method_name}: {e}")
    
    # Fall back to Tesseract if PaddleOCR failed or not available
    if best_result is None and TESSERACT_AVAILABLE:
        for method_name, prep_path in preprocessed_images:
            try:
                raw_text, confidence = process_with_tesseract(prep_path)
                score = confidence * len(raw_text)
                
                logger.info(f"Tesseract ({method_name}): confidence={confidence:.2f}, text_len={len(raw_text)}, score={score:.2f}")
                
                if score > best_score:
                    best_score = score
                    best_result = {
                        'raw_text': raw_text,
                        'confidence': confidence,
                        'blocks': [],
                        'method': f'tesseract_{method_name}'
                    }
                    method_used = f'tesseract_{method_name}'
            except Exception as e:
                logger.warning(f"Tesseract failed on {method_name}: {e}")
    
    processing_time = time.time() - start_time
    
    if best_result is None:
        raise RuntimeError("All OCR methods failed")
    
    best_result['processing_time'] = processing_time
    best_result['method_used'] = method_used
    
    logger.info(f"Best result: {method_used} (score={best_score:.2f}, time={processing_time:.2f}s)")

    return best_result


def parse_product_catalog(raw_text: str) -> List[Dict[str, Any]]:
    """
    Parse product catalog from OCR text
    Extracts product information for marketplace listings
    """
    import re

    products = []
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]

    price_pattern = r'\$?\d+[.,]\d{2}'

    for line in lines:
        # Skip very short lines
        if len(line) < 3:
            continue

        # Extract price if present
        price_match = re.search(price_pattern, line)
        price = None
        if price_match:
            price_str = price_match.group().replace('$', '').replace(',', '')
            try:
                price = float(price_str)
            except:
                pass

        # Extract product name (remove price from line)
        name = re.sub(price_pattern, '', line).strip()

        if name and len(name) >= 3:
            product = {
                'name': name,
                'price': price,
                'description': line,
                'condition': 'New',  # Default
                'category': ''  # To be filled by user
            }
            products.append(product)

    return products

