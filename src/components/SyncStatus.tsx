/**
 * Sync Status Component
 * Shows database synchronization status
 */

import { useData } from '../contexts/DataContext';
import { useAuth } from '../contexts/AuthContext';
import { Cloud, CloudOff, RefreshCw, Check, AlertCircle } from 'lucide-react';

export function SyncStatus() {
  const { isAuthenticated } = useAuth();
  const { syncStatus, lastSyncTime } = useData();

  if (!isAuthenticated) {
    return (
      <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
        <CloudOff size={14} />
        <span>Offline mode (local only)</span>
      </div>
    );
  }

  const getStatusIcon = () => {
    switch (syncStatus) {
      case 'synced':
        return <Check size={14} className="text-green-600 dark:text-green-400" />;
      case 'syncing':
        return <RefreshCw size={14} className="text-blue-600 dark:text-blue-400 animate-spin" />;
      case 'error':
        return <AlertCircle size={14} className="text-red-600 dark:text-red-400" />;
      case 'offline':
        return <CloudOff size={14} className="text-gray-500 dark:text-gray-400" />;
      default:
        return <Cloud size={14} className="text-gray-500 dark:text-gray-400" />;
    }
  };

  const getStatusText = () => {
    switch (syncStatus) {
      case 'synced':
        return lastSyncTime
          ? `Synced ${formatRelativeTime(lastSyncTime)}`
          : 'Synced';
      case 'syncing':
        return 'Syncing...';
      case 'error':
        return 'Sync failed';
      case 'offline':
        return 'Offline';
      default:
        return 'Not synced';
    }
  };

  return (
    <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400">
      {getStatusIcon()}
      <span>{getStatusText()}</span>
    </div>
  );
}

function formatRelativeTime(date: Date): string {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

