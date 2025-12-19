/**
 * Data Sync Context
 * Manages synchronization between localStorage and database
 * Implements offline-first with progressive enhancement
 */

import { createContext, useContext, useState, useEffect, type ReactNode, useCallback } from 'react';
import { apiClient, type ApiError } from '../utils/api';
import { useAuth } from './AuthContext';
import type { MarketplaceListing } from '../types';

type SyncStatus = 'idle' | 'syncing' | 'synced' | 'error' | 'offline';

interface DataContextType {
  listings: MarketplaceListing[];
  syncStatus: SyncStatus;
  lastSyncTime: Date | null;
  error: string | null;
  isSyncing: boolean;
  setListings: (listings: MarketplaceListing[]) => void;
  saveToDatabase: (listingsToSave: MarketplaceListing[]) => Promise<void>;
  loadFromDatabase: () => Promise<MarketplaceListing[]>;
  syncWithDatabase: () => Promise<void>;
  clearError: () => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export function DataProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  const [listings, setListingsState] = useState<MarketplaceListing[]>([]);
  const [syncStatus, setSyncStatus] = useState<SyncStatus>('idle');
  const [lastSyncTime, setLastSyncTime] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('listings');
    if (stored) {
      try {
        setListingsState(JSON.parse(stored));
      } catch (err) {
        console.error('Failed to parse stored listings:', err);
      }
    }
  }, []);

  // Save to localStorage whenever listings change
  const setListings = useCallback((newListings: MarketplaceListing[]) => {
    setListingsState(newListings);
    localStorage.setItem('listings', JSON.stringify(newListings));
  }, []);

  // Auto-sync every 30 seconds if authenticated
  useEffect(() => {
    if (!isAuthenticated) return;

    const interval = setInterval(() => {
      syncWithDatabase();
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [isAuthenticated]);

  const saveToDatabase = async (listingsToSave: MarketplaceListing[]) => {
    if (!isAuthenticated) {
      setError('Please login to save to database');
      return;
    }

    setSyncStatus('syncing');
    setError(null);

    try {
      // Transform frontend format (UPPERCASE) to backend format (lowercase)
      const backendListings = listingsToSave.map(listing => ({
        title: listing.TITLE,
        price: listing.PRICE.toString(),
        condition: listing.CONDITION,
        description: listing.DESCRIPTION || '',
        category: listing.CATEGORY || '',
        offer_shipping: listing['OFFER SHIPPING'] || 'No',
        source: 'manual',
      }));

      // Send all listings to backend
      await apiClient.post('/api/listings/bulk', { listings: backendListings });
      setSyncStatus('synced');
      setLastSyncTime(new Date());
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to save to database');
      setSyncStatus('error');
      throw err;
    }
  };

  const loadFromDatabase = async (): Promise<MarketplaceListing[]> => {
    if (!isAuthenticated) {
      setError('Please login to load from database');
      return [];
    }

    setSyncStatus('syncing');
    setError(null);

    try {
      // Backend returns lowercase field names, need to transform to frontend format
      interface BackendListing {
        id: string;
        title: string;
        price: string;
        condition: string;
        description?: string;
        category?: string;
        offer_shipping?: string;
      }

      const response = await apiClient.get<{ listings: BackendListing[] }>('/api/listings');

      // Transform backend format (lowercase) to frontend format (UPPERCASE)
      const dbListings: MarketplaceListing[] = response.listings.map(listing => ({
        id: listing.id,
        TITLE: listing.title,
        PRICE: parseFloat(listing.price),
        CONDITION: listing.condition,
        DESCRIPTION: listing.description || '',
        CATEGORY: listing.category || '',
        'OFFER SHIPPING': listing.offer_shipping || 'No',
      }));

      // Check for conflicts with local data
      if (listings.length > 0 && dbListings.length > 0) {
        // For now, merge both (keep all unique listings)
        const merged = mergeListings(listings, dbListings);
        setListings(merged);
        setSyncStatus('synced');
        setLastSyncTime(new Date());
        return merged;
      } else if (dbListings.length > 0) {
        setListings(dbListings);
        setSyncStatus('synced');
        setLastSyncTime(new Date());
        return dbListings;
      }

      setSyncStatus('synced');
      setLastSyncTime(new Date());
      return [];
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to load from database');
      setSyncStatus('error');
      throw err;
    }
  };

  const syncWithDatabase = async () => {
    if (!isAuthenticated) {
      setSyncStatus('offline');
      return;
    }

    // Silent sync - don't show loading state
    try {
      const response = await apiClient.get<{ listings: MarketplaceListing[] }>('/api/listings');
      const dbListings = response.listings;

      // Only update if database has newer data
      if (dbListings.length > 0) {
        const merged = mergeListings(listings, dbListings);
        if (JSON.stringify(merged) !== JSON.stringify(listings)) {
          setListings(merged);
        }
      }

      setSyncStatus('synced');
      setLastSyncTime(new Date());
    } catch {
      setSyncStatus('offline');
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value: DataContextType = {
    listings,
    syncStatus,
    lastSyncTime,
    error,
    isSyncing: syncStatus === 'syncing',
    setListings,
    saveToDatabase,
    loadFromDatabase,
    syncWithDatabase,
    clearError,
  };

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
}

export function useData() {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
}

// Helper function to merge listings (keep unique by ID)
function mergeListings(
  local: MarketplaceListing[],
  remote: MarketplaceListing[]
): MarketplaceListing[] {
  const map = new Map<string, MarketplaceListing>();

  // Add local listings
  local.forEach(listing => {
    if (listing.id) {
      map.set(listing.id, listing);
    }
  });

  // Add/update with remote listings (remote takes precedence)
  remote.forEach(listing => {
    if (listing.id) {
      map.set(listing.id, listing);
    }
  });

  return Array.from(map.values());
}

