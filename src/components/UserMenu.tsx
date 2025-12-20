/**
 * User Menu Component
 * Shows login status and provides logout option
 */

import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { User, LogOut, LogIn } from 'lucide-react';

interface UserMenuProps {
  onLoginClick: () => void;
}

export function UserMenu({ onLoginClick }: UserMenuProps) {
  const { user, isAuthenticated, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!isAuthenticated) {
    return (
      <button
        onClick={onLoginClick}
        className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors select-text"
      >
        <LogIn size={18} />
        <span>Login</span>
      </button>
    );
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors select-text"
      >
        <User size={18} />
        <span className="max-w-[150px] truncate">{user?.email}</span>
      </button>

      {/* Dropdown menu */}
      {isOpen && (
        <>
          {/* Backdrop to close menu */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Menu content */}
          <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-20">
            <div className="p-3 border-b border-gray-200 dark:border-gray-700">
              <p className="text-sm font-medium text-gray-900 dark:text-white truncate select-text">
                {user?.email}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 select-text">
                {user?.is_admin ? 'Admin' : 'User'}
              </p>
            </div>

            <button
              onClick={() => {
                logout();
                setIsOpen(false);
              }}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors select-text"
            >
              <LogOut size={16} />
              <span>Logout</span>
            </button>
          </div>
        </>
      )}
    </div>
  );
}

