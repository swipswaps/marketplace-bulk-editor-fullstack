import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { DataTable } from './components/DataTable';
import { ExportButton } from './components/ExportButton';
import type { MarketplaceListing } from './types';
import { FileSpreadsheet, Trash2 } from 'lucide-react';

function App() {
  const [listings, setListings] = useState<MarketplaceListing[]>([]);

  const handleDataLoaded = (newData: MarketplaceListing[]) => {
    // Merge with existing data
    setListings(prev => [...prev, ...newData]);
  };

  const handleClearAll = () => {
    if (confirm('Are you sure you want to clear all listings?')) {
      setListings([]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <FileSpreadsheet className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">
              Facebook Marketplace Bulk Editor
            </h1>
          </div>
          <p className="text-gray-600">
            Upload, edit, and combine Facebook Marketplace bulk upload spreadsheets
          </p>
        </div>

        {/* File Upload Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Upload Files</h2>
          <FileUpload onDataLoaded={handleDataLoaded} />
        </div>

        {/* Data Table Section */}
        {listings.length > 0 && (
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">
                Listings ({listings.length})
              </h2>
              <div className="flex gap-3">
                <button
                  onClick={handleClearAll}
                  className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  <Trash2 size={20} />
                  Clear All
                </button>
                <ExportButton data={listings} />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <DataTable data={listings} onUpdate={setListings} />
            </div>
          </div>
        )}

        {/* Empty State */}
        {listings.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow-md">
            <FileSpreadsheet className="mx-auto h-16 w-16 text-gray-300 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No listings yet
            </h3>
            <p className="text-gray-500">
              Upload Excel files to get started
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Supports Facebook Marketplace bulk upload format • Max 50 listings per file
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
