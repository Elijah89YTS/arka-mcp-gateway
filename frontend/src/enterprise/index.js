/**
 * Enterprise features module stub.
 * Real implementation is only in the enterprise edition.
 */

export const __enterprise__ = false;  // Marker: False = Community Edition
export const isEnterprise = false;

export const enterpriseConfig = {
  azureSSOEnabled: false,
  auditLogsEnabled: false,
  teamsEnabled: false,
};

// Stub components
export { default as AzureSSOButton } from './components/AzureSSOButton';
