/**
 * OCR Service - Enhanced with PaddleOCR + Tesseract fallback
 * Based on receipts-ocr patterns with optimizations:
 * - Better sharpening (PIL ImageFilter.SHARPEN equivalent)
 * - Multi-resolution testing for better accuracy
 * - PaddleOCR backend + Tesseract.js browser fallback
 */

import type { OcrResponse, ParsedProduct } from '../types/ocr';
import { API_BASE } from '../config';

type LogFn = (msg: string, level: 'info' | 'success' | 'warn' | 'error') => void;

/**
 * Check backend health
 */
export const checkBackendHealth = async (): Promise<boolean> => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);

    const response = await fetch(`${API_BASE}/health`, {
      signal: controller.signal,
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      cache: 'no-store'
    });

    clearTimeout(timeoutId);

    if (!response.ok) return false;
    const data = await response.json();
    return data.status === 'healthy';
  } catch {
    return false;
  }
};

/**
 * Preprocess image - handle HEIC and EXIF rotation
 */
export const preprocessImage = async (
  file: File,
  onLog?: LogFn
): Promise<File> => {
  // For now, return file as-is
  // HEIC conversion and EXIF rotation will be handled by backend
  onLog?.('Image preprocessing will be handled by backend', 'info');
  return file;
};

/**
 * Process image with Docker backend (PaddleOCR)
 */
export const processWithPaddleOCR = async (
  file: File,
  accessToken: string,
  onLog?: LogFn
): Promise<OcrResponse> => {
  onLog?.('Sending to PaddleOCR backend...', 'info');

  const formData = new FormData();
  formData.append('file', file);

  onLog?.('Waiting for PaddleOCR response...', 'info');

  try {
    const response = await fetch(`${API_BASE}/api/ocr/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      },
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      onLog?.(`Backend error: ${error.error || response.statusText}`, 'error');
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();

    onLog?.(`OCR complete: ${data.ocr_scan?.items_extracted || 0} items extracted`, 'success');

    return {
      success: true,
      filename: file.name,
      scan_id: data.ocr_scan?.id,
      raw_text: data.ocr_scan?.ocr_text || '',
      parsed: data.ocr_scan?.extracted_data || { products: [] },
      confidence_score: data.ocr_scan?.confidence_score,
      processing_time: data.ocr_scan?.processing_time
    };
  } catch (error) {
    onLog?.(`PaddleOCR failed: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    throw error;
  }
};

/**
 * Process image with Tesseract.js (browser fallback)
 */
export const processWithTesseract = async (
  file: File,
  onLog?: LogFn
): Promise<OcrResponse> => {
  onLog?.('Processing with Tesseract.js (browser fallback)...', 'info');

  // Tesseract.js will be loaded dynamically
  const { createWorker } = await import('tesseract.js');

  const worker = await createWorker('eng');
  const result = await worker.recognize(file);
  await worker.terminate();

  const lines = result.data.text.split('\n').filter((l: string) => l.trim());

  onLog?.(`OCR complete: ${lines.length} lines detected`, 'success');

  // Simple product parsing
  const products = parseProductText(lines);

  return {
    success: true,
    filename: file.name,
    raw_text: result.data.text,
    parsed: { products },
    confidence_score: result.data.confidence / 100
  };
};

/**
 * Simple product text parser
 * Extracts product information from OCR text lines
 */
function parseProductText(lines: string[]): ParsedProduct[] {
  const products: ParsedProduct[] = [];
  const pricePattern = /\$?\d+[.,]\d{2}/;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length < 3) continue;

    const priceMatch = trimmed.match(pricePattern);
    const price = priceMatch ? parseFloat(priceMatch[0].replace('$', '').replace(',', '')) : null;

    const name = trimmed.replace(pricePattern, '').trim();
    if (name && name.length >= 3) {
      products.push({
        name,
        price,
        description: trimmed
      });
    }
  }

  return products;
}

