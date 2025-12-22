/**
 * OCR Upload Component
 * Upload images for OCR processing with PaddleOCR + Tesseract fallback
 */

import { useState } from 'react';
import { FileImage, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useData } from '../contexts/DataContext';
import { processWithPaddleOCR, processWithTesseract, checkBackendHealth } from '../services/ocrService';
import type { ParsedProduct } from '../types/ocr';
import type { MarketplaceListing } from '../types';

interface OCRUploadProps {
  onProductsExtracted?: (products: ParsedProduct[]) => void;
}

export function OCRUpload({ onProductsExtracted }: OCRUploadProps) {
  const { isAuthenticated, accessToken } = useAuth();
  const { setListings } = useData();
  const [processing, setProcessing] = useState(false);
  const [logs, setLogs] = useState<Array<{ message: string; level: string }>>([]);
  const [preview, setPreview] = useState<string | null>(null);

  const addLog = (message: string, level: 'info' | 'success' | 'warn' | 'error') => {
    setLogs(prev => [...prev, { message, level }]);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(file);

    setProcessing(true);
    setLogs([]);
    addLog(`Processing ${file.name}...`, 'info');

    try {
      let result;

      // Try PaddleOCR backend first if authenticated
      if (isAuthenticated && accessToken) {
        const backendHealthy = await checkBackendHealth();
        
        if (backendHealthy) {
          addLog('Using PaddleOCR backend...', 'info');
          result = await processWithPaddleOCR(file, accessToken, addLog);
        } else {
          addLog('Backend unavailable, using Tesseract.js fallback...', 'warn');
          result = await processWithTesseract(file, addLog);
        }
      } else {
        addLog('Not authenticated, using Tesseract.js...', 'info');
        result = await processWithTesseract(file, addLog);
      }

      if (result.success && result.parsed.products.length > 0) {
        addLog(`Extracted ${result.parsed.products.length} products`, 'success');

        // Convert to listings format (MarketplaceListing type)
        const newListings: MarketplaceListing[] = result.parsed.products.map(product => ({
          id: crypto.randomUUID(),
          TITLE: product.name,
          PRICE: product.price || 0,
          CONDITION: (product.condition || 'New') as 'New' | 'Used - Like New' | 'Used - Good' | 'Used - Fair',
          DESCRIPTION: product.description || product.name,
          CATEGORY: product.category || '',
          'OFFER SHIPPING': 'Yes' as 'Yes' | 'No'
        }));

        // Add to data table (append to existing listings)
        // Use functional update to avoid stale closure
        setListings((prevListings: MarketplaceListing[]) => [...prevListings, ...newListings]);

        // Notify parent
        onProductsExtracted?.(result.parsed.products);

        addLog(`${newListings.length} products added to table`, 'success');
      } else {
        addLog('No products found in image', 'warn');
      }
    } catch (error) {
      addLog(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6">
        <label className="flex flex-col items-center cursor-pointer">
          <FileImage size={48} className="text-gray-400 dark:text-gray-500 mb-2" />
          <span className="text-sm text-gray-600 dark:text-gray-400 mb-2">
            Upload product catalog image
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-500">
            Supports: JPG, PNG, PDF
          </span>
          <input
            type="file"
            accept="image/*,.pdf"
            onChange={handleFileSelect}
            disabled={processing}
            className="hidden"
          />
          {processing && (
            <div className="mt-4 flex items-center gap-2 text-blue-600 dark:text-blue-400">
              <Loader size={16} className="animate-spin" />
              <span className="text-sm">Processing...</span>
            </div>
          )}
        </label>
      </div>

      {/* Preview */}
      {preview && (
        <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-4">
          <h3 className="text-sm font-medium mb-2">Preview</h3>
          <img src={preview} alt="Preview" className="max-h-64 mx-auto" />
        </div>
      )}

      {/* Logs */}
      {logs.length > 0 && (
        <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-4 max-h-64 overflow-y-auto">
          <h3 className="text-sm font-medium mb-2">Processing Log</h3>
          <div className="space-y-1 text-xs font-mono">
            {logs.map((log, idx) => (
              <div key={idx} className={`flex items-start gap-2 ${
                log.level === 'error' ? 'text-red-600 dark:text-red-400' :
                log.level === 'warn' ? 'text-yellow-600 dark:text-yellow-400' :
                log.level === 'success' ? 'text-green-600 dark:text-green-400' :
                'text-gray-600 dark:text-gray-400'
              }`}>
                {log.level === 'error' && <AlertCircle size={14} className="mt-0.5 flex-shrink-0" />}
                {log.level === 'success' && <CheckCircle size={14} className="mt-0.5 flex-shrink-0" />}
                <span>{log.message}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

