import React, { useState } from 'react';
import { AlertTriangle, X, ExternalLink, Shield, Scale, FileWarning } from 'lucide-react';

interface LegalNoticeProps {
  onAccept?: () => void;
  compact?: boolean;
}

export const LegalNotice: React.FC<LegalNoticeProps> = ({ onAccept, compact = false }) => {
  const [isExpanded, setIsExpanded] = useState(!compact);
  const [hasAccepted, setHasAccepted] = useState(() => {
    return localStorage.getItem('legalNoticeAccepted') === 'true';
  });

  const handleAccept = () => {
    localStorage.setItem('legalNoticeAccepted', 'true');
    setHasAccepted(true);
    onAccept?.();
  };

  const handleDismiss = () => {
    setIsExpanded(false);
  };

  if (hasAccepted && compact) {
    return (
      <div className="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 px-4 py-2 text-xs text-gray-600 dark:text-gray-400 text-center">
        <button
          onClick={() => setIsExpanded(true)}
          className="hover:text-blue-600 dark:hover:text-blue-400 underline"
        >
          View Legal Disclaimer
        </button>
        {' • '}
        Not affiliated with Meta Platforms, Inc. • Facebook® is a registered trademark
      </div>
    );
  }

  if (!isExpanded) return null;

  return (
    <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-6">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-6 h-6 text-yellow-600 dark:text-yellow-500 flex-shrink-0" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Important Legal Notice
          </h3>
        </div>
        {hasAccepted && (
          <button
            onClick={handleDismiss}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      <div className="space-y-4 text-sm text-gray-700 dark:text-gray-300">
        {/* Trademark Disclaimer */}
        <div className="flex gap-3">
          <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white mb-1">Trademark Disclaimer</p>
            <p>
              This software is <strong>NOT affiliated with, maintained, authorized, endorsed, or sponsored by 
              Meta Platforms, Inc.</strong> or Facebook, Inc. FACEBOOK® and the Facebook logo are registered 
              trademarks of Meta Platforms, Inc.
            </p>
          </div>
        </div>

        {/* Copyright & IP Compliance */}
        <div className="flex gap-3">
          <Scale className="w-5 h-5 text-purple-600 dark:text-purple-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white mb-1">Copyright & IP Compliance</p>
            <p>
              <strong>You are solely responsible</strong> for ensuring all listings comply with intellectual 
              property laws. <strong className="text-red-600 dark:text-red-400">NO counterfeit, replica, or 
              unauthorized items.</strong> Violations may result in legal action and account suspension.
            </p>
          </div>
        </div>

        {/* Commerce Policies */}
        <div className="flex gap-3">
          <FileWarning className="w-5 h-5 text-orange-600 dark:text-orange-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white mb-1">Facebook Commerce Policies</p>
            <p className="mb-2">
              You must comply with Meta's Commerce Policies. <strong>Prohibited items include:</strong>
            </p>
            <ul className="list-disc list-inside space-y-1 text-xs ml-2">
              <li>Alcohol, tobacco, and drugs</li>
              <li>Weapons, ammunition, and explosives</li>
              <li>Adult products and services</li>
              <li>Animals and endangered species</li>
              <li>Healthcare items (prescription drugs, medical devices)</li>
              <li>Recalled, illegal, or hazardous products</li>
              <li>Counterfeit or replica items</li>
              <li>Digital products and non-physical items</li>
            </ul>
            <a
              href="https://www.facebook.com/policies/commerce"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-blue-600 dark:text-blue-400 hover:underline mt-2"
            >
              View Full Commerce Policies <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded p-3 mt-4">
          <p className="text-xs text-red-800 dark:text-red-300 font-semibold">
            ⚠️ USE AT YOUR OWN RISK
          </p>
          <p className="text-xs text-red-700 dark:text-red-400 mt-1">
            This software is provided "AS IS" without warranty. The developers assume NO LIABILITY for 
            account suspensions, policy violations, legal consequences, or any damages arising from use 
            of this software. You are responsible for compliance with all applicable laws and platform policies.
          </p>
        </div>
      </div>

      {!hasAccepted && (
        <div className="mt-6 flex gap-3">
          <button
            onClick={handleAccept}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            I Understand and Accept
          </button>
        </div>
      )}
    </div>
  );
};

