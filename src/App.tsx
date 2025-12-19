import { useState, useEffect, useCallback } from 'react';
import { FileUpload } from './components/FileUpload';
import { DataTable } from './components/DataTable';
import { ExportButton } from './components/ExportButton';
import { SettingsModal } from './components/SettingsModal';
import { BackendStatus } from './components/BackendStatus';
import { AuthModal } from './components/AuthModal';
import { UserMenu } from './components/UserMenu';
import { SyncStatus } from './components/SyncStatus';
import { Settings, Download, Upload } from 'lucide-react';
import type { MarketplaceListing, TemplateMetadata } from './types';
import { FileSpreadsheet, Trash2 } from 'lucide-react';
import { useAuth } from './contexts/AuthContext';
import { useData } from './contexts/DataContext';

type SortField = keyof MarketplaceListing | null;
type SortDirection = 'asc' | 'desc' | null;

function App() {
  const { isAuthenticated } = useAuth();
  const { listings: dataListings, setListings: setDataListings, saveToDatabase, loadFromDatabase, isSyncing } = useData();

  const [listings, setListings] = useState<MarketplaceListing[]>([]);
  const [sortField, setSortField] = useState<SortField>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });
  const [template, setTemplate] = useState<TemplateMetadata | null>(() => {
    const saved = localStorage.getItem('fbTemplate');
    return saved ? JSON.parse(saved) : null;
  });
  const [showSettings, setShowSettings] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [exportPreviewContent, setExportPreviewContent] = useState<React.ReactNode | null>(null);
  const [hasUploadedFile, setHasUploadedFile] = useState(() => {
    return localStorage.getItem('hasUploadedFile') === 'true';
  });

  // Undo/Redo state
  const [history, setHistory] = useState<MarketplaceListing[][]>([]);
  const [historyIndex, setHistoryIndex] = useState<number>(-1);

  // Sync local listings with DataContext
  useEffect(() => {
    if (dataListings.length > 0 && listings.length === 0) {
      // Load from DataContext on mount
      setListings(dataListings);
    }
  }, [dataListings, listings.length]);

  // Update DataContext when listings change
  useEffect(() => {
    if (listings.length > 0) {
      setDataListings(listings);
    }
  }, [listings, setDataListings]);

  // Apply dark mode class to document
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  // Save template to localStorage
  useEffect(() => {
    if (template) {
      localStorage.setItem('fbTemplate', JSON.stringify(template));
    } else {
      localStorage.removeItem('fbTemplate');
    }
  }, [template]);

  const handleTemplateLoad = (newTemplate: TemplateMetadata, isPreload = false) => {
    setTemplate(newTemplate);

    // Show settings modal on first template preload (same as first file upload)
    if (isPreload && !hasUploadedFile) {
      setHasUploadedFile(true);
      localStorage.setItem('hasUploadedFile', 'true');
      setShowSettings(true);
    }
  };

  const handleTemplateDetected = (template: TemplateMetadata, _sampleData: MarketplaceListing[]) => {
    // Save the template structure
    setTemplate(template);

    // Show settings modal on first template detection
    if (!hasUploadedFile) {
      setHasUploadedFile(true);
      localStorage.setItem('hasUploadedFile', 'true');
      setShowSettings(true);
    }
  };

  const handleDataLoaded = (newData: MarketplaceListing[]) => {
    // Merge with existing data
    const updatedListings = [...listings, ...newData];
    console.log(`📊 Data loaded: ${newData.length} new listings + ${listings.length} existing = ${updatedListings.length} total`);
    updateListingsWithHistory(updatedListings);

    // Show settings modal on first file upload
    if (!hasUploadedFile) {
      setHasUploadedFile(true);
      localStorage.setItem('hasUploadedFile', 'true');
      setShowSettings(true);
    }
  };

  const handleClearAll = () => {
    if (confirm('Are you sure you want to clear all listings?')) {
      updateListingsWithHistory([]);
    }
  };

  // Update listings and add to history
  const updateListingsWithHistory = (newListings: MarketplaceListing[]) => {
    // Truncate history if we're not at the end
    const newHistory = history.slice(0, historyIndex + 1);

    // Add new state to history (keep last 50 states)
    newHistory.push(newListings);
    if (newHistory.length > 50) {
      newHistory.shift();
    }

    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
    setListings(newListings);
  };

  // Undo handler
  const handleUndo = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setListings(history[newIndex]);
    }
  }, [historyIndex, history]);

  // Redo handler
  const handleRedo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setListings(history[newIndex]);
    }
  }, [historyIndex, history]);

  // Keyboard shortcuts for undo/redo
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        handleUndo();
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
        e.preventDefault();
        handleRedo();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [historyIndex, history, handleUndo, handleRedo]);

  // Save to Database handler
  const handleSaveToDatabase = async () => {
    if (!isAuthenticated) {
      alert('Please login to save to database');
      return;
    }

    try {
      await saveToDatabase(listings);
      alert('✅ Listings saved to database successfully!');
    } catch (error) {
      console.error('Failed to save to database:', error);
      alert('❌ Failed to save to database. Please try again.');
    }
  };

  // Load from Database handler
  const handleLoadFromDatabase = async () => {
    if (!isAuthenticated) {
      alert('Please login to load from database');
      return;
    }

    try {
      const loadedListings = await loadFromDatabase();
      if (loadedListings && loadedListings.length > 0) {
        updateListingsWithHistory(loadedListings);
        alert(`✅ Loaded ${loadedListings.length} listings from database!`);
      } else {
        alert('No listings found in database');
      }
    } catch (error) {
      console.error('Failed to load from database:', error);
      alert('❌ Failed to load from database. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-10 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="flex items-center justify-between gap-4">
            {/* Left: Logo and Title */}
            <div className="flex items-center gap-2">
              <div className="bg-blue-600 dark:bg-blue-500 p-2 rounded-lg text-white">
                <FileSpreadsheet size={20} />
              </div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
                Marketplace Bulk Editor
              </h1>
            </div>

            {/* Center: Backend Status and Sync Status */}
            <div className="flex-1 max-w-2xl flex items-center gap-4">
              <BackendStatus />
              {isAuthenticated && <SyncStatus />}
            </div>

            {/* Right: Controls */}
            <div className="flex items-center gap-3">
            {/* User Menu */}
            <UserMenu onLoginClick={() => setShowAuthModal(true)} />

            {/* Undo/Redo Buttons */}
            <div className="flex items-center gap-1 border-r border-gray-300 dark:border-gray-600 pr-3">
              <button
                onClick={handleUndo}
                disabled={historyIndex <= 0}
                className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                title="Undo (Ctrl+Z)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 7v6h6"/>
                  <path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/>
                </svg>
              </button>
              <button
                onClick={handleRedo}
                disabled={historyIndex >= history.length - 1}
                className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                title="Redo (Ctrl+Y)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 7v6h-6"/>
                  <path d="M3 17a9 9 0 0 1 9-9 9 9 0 0 1 6 2.3l3 2.7"/>
                </svg>
              </button>
            </div>

            {/* Settings Button */}
            <button
              onClick={() => setShowSettings(true)}
              className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title="Settings & Legal Notice"
            >
              <Settings size={20} />
            </button>

            {/* Database Buttons (only when authenticated) */}
            {isAuthenticated && (
              <>
                <button
                  onClick={handleSaveToDatabase}
                  disabled={isSyncing || listings.length === 0}
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:bg-green-400 disabled:cursor-not-allowed rounded-lg transition-colors"
                  title="Save all listings to database"
                >
                  <Upload size={16} />
                  {isSyncing ? 'Saving...' : 'Save to DB'}
                </button>
                <button
                  onClick={handleLoadFromDatabase}
                  disabled={isSyncing}
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed rounded-lg transition-colors"
                  title="Load listings from database"
                >
                  <Download size={16} />
                  {isSyncing ? 'Loading...' : 'Load from DB'}
                </button>
              </>
            )}

            {listings.length > 0 && (
              <>
                <button
                  onClick={handleClearAll}
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                >
                  <Trash2 size={16} />
                  Clear All
                </button>
                <ExportButton
                  data={listings}
                  sortField={sortField}
                  sortDirection={sortDirection}
                  template={template}
                  onPreviewRender={setExportPreviewContent}
                />
              </>
            )}
            </div>
          </div>
        </div>
      </header>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        darkMode={darkMode}
        onDarkModeToggle={() => setDarkMode(!darkMode)}
      />

      {/* Auth Modal */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
      />

      {/* Main Content */}
      <main className="flex-1 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Data Table Section - Show when we have data */}
          {listings.length > 0 ? (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Listings</h2>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {listings.length} {listings.length === 1 ? 'item' : 'items'}
                    {template && template.columnHeaders.length > 0 && (
                      <span className="ml-2 text-xs text-green-600 dark:text-green-400">
                        • Template: {template.sheetName}
                      </span>
                    )}
                  </p>
                </div>

                {/* Compact upload button when data exists */}
                <FileUpload
                  onDataLoaded={handleDataLoaded}
                  onTemplateDetected={handleTemplateDetected}
                  currentTemplate={template}
                  onTemplateLoad={handleTemplateLoad}
                  compact={true}
                />
              </div>

              {/* Show export preview if active, otherwise show DataTable */}
              {exportPreviewContent ? (
                exportPreviewContent
              ) : (
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
                  <div className="p-6">
                    <DataTable
                      data={listings}
                      onUpdate={updateListingsWithHistory}
                      sortField={sortField}
                      sortDirection={sortDirection}
                      onSortChange={(field, direction) => {
                        setSortField(field);
                        setSortDirection(direction);
                      }}
                    />
                  </div>
                </div>
              )}
            </div>
          ) : (
            /* Empty State with integrated upload */
            <FileUpload
              onDataLoaded={handleDataLoaded}
              onTemplateDetected={handleTemplateDetected}
              currentTemplate={template}
              onTemplateLoad={handleTemplateLoad}
              compact={false}
            />
          )}

          {/* Footer Info */}
          <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
            <p className="mb-2">
              Supports Facebook Marketplace bulk upload format • Max 50 listings per file
            </p>
            <p className="text-xs">
              Not affiliated with Meta Platforms, Inc. • Facebook® is a registered trademark of Meta Platforms, Inc.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
