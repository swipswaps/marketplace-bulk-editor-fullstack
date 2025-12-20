import { AlertCircle, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import type { ImportValidationResult } from '../types';

interface ImportValidationModalProps {
  validationResult: ImportValidationResult;
  onImportAll: () => void;
  onImportValidOnly: () => void;
  onCancel: () => void;
}

export function ImportValidationModal({
  validationResult,
  onImportAll,
  onImportValidOnly,
  onCancel
}: ImportValidationModalProps) {
  const { validCount, autoFilledCount, rejectedCount, totalRows, autoFilled, rejected } = validationResult;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-start gap-3 p-6 border-b border-gray-200 dark:border-gray-700">
          <AlertCircle className="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" size={24} />
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Import Validation Report
            </h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              Imported <strong>{totalRows}</strong> row(s) from file
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {/* Valid rows */}
          {validCount > 0 && (
            <div className="flex items-start gap-3 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <CheckCircle className="text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" size={20} />
              <div>
                <p className="font-medium text-green-900 dark:text-green-100">
                  ✅ {validCount} row(s) valid
                </p>
                <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                  All required fields (TITLE, PRICE, CONDITION) are filled
                </p>
              </div>
            </div>
          )}

          {/* Auto-filled rows */}
          {autoFilledCount > 0 && (
            <div className="flex items-start gap-3 p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
              <AlertTriangle className="text-orange-600 dark:text-orange-400 flex-shrink-0 mt-0.5" size={20} />
              <div className="flex-1">
                <p className="font-medium text-orange-900 dark:text-orange-100">
                  ⚠️ {autoFilledCount} row(s) with auto-filled fields
                </p>
                <p className="text-sm text-orange-700 dark:text-orange-300 mt-1 mb-3">
                  These rows had missing fields that were filled with default values. Please review.
                </p>
                
                {/* Show details for first 5 auto-filled rows */}
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {autoFilled.slice(0, 5).map((listing, idx) => (
                    <div key={listing.id} className="text-xs bg-white dark:bg-gray-800 p-2 rounded border border-orange-200 dark:border-orange-700">
                      <p className="font-medium text-gray-900 dark:text-gray-100">
                        Row {idx + 1}: {listing.TITLE || '(No title)'}
                      </p>
                      {listing._autoFilled?.map((field, fieldIdx) => (
                        <p key={fieldIdx} className="text-orange-700 dark:text-orange-300 ml-2">
                          • {String(field.field)}: {field.reason}
                        </p>
                      ))}
                    </div>
                  ))}
                  {autoFilled.length > 5 && (
                    <p className="text-xs text-orange-600 dark:text-orange-400 italic">
                      ... and {autoFilled.length - 5} more row(s)
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Rejected rows */}
          {rejectedCount > 0 && (
            <div className="flex items-start gap-3 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
              <XCircle className="text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" size={20} />
              <div className="flex-1">
                <p className="font-medium text-red-900 dark:text-red-100">
                  ❌ {rejectedCount} row(s) rejected
                </p>
                <p className="text-sm text-red-700 dark:text-red-300 mt-1 mb-3">
                  These rows are missing TITLE (required field) and cannot be imported
                </p>
                
                {/* Show details for first 5 rejected rows */}
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {rejected.slice(0, 5).map((listing, idx) => (
                    <div key={listing.id} className="text-xs bg-white dark:bg-gray-800 p-2 rounded border border-red-200 dark:border-red-700">
                      <p className="font-medium text-gray-900 dark:text-gray-100">
                        Row {idx + 1}: (No title)
                      </p>
                      <p className="text-red-700 dark:text-red-300 ml-2">
                        • Missing required field: TITLE
                      </p>
                    </div>
                  ))}
                  {rejected.length > 5 && (
                    <p className="text-xs text-red-600 dark:text-red-400 italic">
                      ... and {rejected.length - 5} more row(s)
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
          >
            Cancel
          </button>
          
          {(validCount > 0 || autoFilledCount > 0) && (
            <button
              onClick={onImportValidOnly}
              className="px-4 py-2 text-sm font-medium text-white bg-green-600 dark:bg-green-700 rounded-md hover:bg-green-700 dark:hover:bg-green-600 transition-colors"
            >
              Import Valid Only ({validCount})
            </button>
          )}
          
          {autoFilledCount > 0 && (
            <button
              onClick={onImportAll}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 dark:bg-blue-700 rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors"
            >
              Import & Review ({validCount + autoFilledCount})
            </button>
          )}
          
          {autoFilledCount === 0 && validCount > 0 && (
            <button
              onClick={onImportAll}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 dark:bg-blue-700 rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors"
            >
              Import All ({validCount})
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

