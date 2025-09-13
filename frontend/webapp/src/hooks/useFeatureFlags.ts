import { useState, useEffect, useCallback } from 'react';

// Default feature flags - these would typically come from an API or config
const DEFAULT_FEATURE_FLAGS: Record<string, boolean> = {
  // Core features
  'auth': true,
  'notifications': true,
  'profile': true,
  
  // Module flags
  'module.citizenship': true,
  'module.education': true,
  'module.health': false,  // Coming soon
  'module.urbanism': false, // Coming soon
  'module.commerce': false, // Coming soon
  'module.sanitation': false, // Coming soon
  
  // Experimental features
  'feature.dark_mode': true,
  'feature.biometric_auth': false,
  'feature.family_accounts': false,
};

// Type for feature flags
type FeatureFlag = keyof typeof DEFAULT_FEATURE_FLAGS;

/**
 * Hook to manage feature flags
 * In a real app, this would fetch flags from a server
 */
export const useFeatureFlags = () => {
  const [flags, setFlags] = useState<Record<string, boolean>>(DEFAULT_FEATURE_FLAGS);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  // Load feature flags from API or local storage
  const loadFeatureFlags = useCallback(async () => {
    try {
      setIsLoading(true);
      
      // In a real app, this would be an API call:
      // const response = await fetch('/api/feature-flags');
      // const data = await response.json();
      // setFlags(data);
      
      // For now, use local storage or default flags
      const storedFlags = localStorage.getItem('featureFlags');
      if (storedFlags) {
        setFlags(JSON.parse(storedFlags));
      } else {
        setFlags(DEFAULT_FEATURE_FLAGS);
      }
    } catch (err) {
      console.error('Failed to load feature flags:', err);
      setError(err instanceof Error ? err : new Error('Failed to load feature flags'));
      // Fall back to default flags on error
      setFlags(DEFAULT_FEATURE_FLAGS);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Save feature flags (admin only)
  const updateFeatureFlags = useCallback(async (newFlags: Record<string, boolean>) => {
    try {
      setIsLoading(true);
      
      // In a real app, this would be an API call:
      // await fetch('/api/feature-flags', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(newFlags),
      // });
      
      // For now, just update local storage
      localStorage.setItem('featureFlags', JSON.stringify(newFlags));
      setFlags(newFlags);
      return true;
    } catch (err) {
      console.error('Failed to update feature flags:', err);
      setError(err instanceof Error ? err : new Error('Failed to update feature flags'));
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Check if a feature is enabled
  const isFeatureEnabled = useCallback((feature: string): boolean => {
    return flags[feature] || false;
  }, [flags]);

  // Check if all features in a list are enabled
  const areFeaturesEnabled = useCallback((features: string[]): boolean => {
    return features.every(feature => flags[feature]);
  }, [flags]);

  // Check if any feature in a list is enabled
  const isAnyFeatureEnabled = useCallback((features: string[]): boolean => {
    return features.some(feature => flags[feature]);
  }, [flags]);

  // Load flags on mount
  useEffect(() => {
    loadFeatureFlags();
  }, [loadFeatureFlags]);

  return {
    flags,
    isLoading,
    error,
    isFeatureEnabled,
    areFeaturesEnabled,
    isAnyFeatureEnabled,
    updateFeatureFlags,
    refresh: loadFeatureFlags,
  };
};

// Helper hook for a single feature flag
export const useFeatureFlag = (feature: string, defaultValue = false) => {
  const { isFeatureEnabled, isLoading, error } = useFeatureFlags();
  
  return {
    isEnabled: isFeatureEnabled(feature) || defaultValue,
    isLoading,
    error,
  };
};

export default useFeatureFlags;

