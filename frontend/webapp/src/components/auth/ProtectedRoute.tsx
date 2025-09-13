import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-hot-toast';

type UserRole = 'citizen' | 'admin' | 'manager' | 'auditor' | null;

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: UserRole[];
  requiredPermissions?: string[];
  requireAllPermissions?: boolean;
  redirectTo?: string;
}

/**
 * A component that protects routes based on authentication status, roles, and permissions.
 * 
 * @param children - The child components to render if access is granted
 * @param allowedRoles - Array of user roles that are allowed to access the route
 * @param requiredPermissions - Array of permissions required to access the route
 * @param requireAllPermissions - If true, user must have all required permissions. If false, any permission is sufficient.
 * @param redirectTo - The path to redirect to if access is denied
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles = [],
  requiredPermissions = [],
  requireAllPermissions = true,
  redirectTo = '/unauthorized',
}) => {
  const { isAuthenticated, user, isLoading } = useAuth();
  const location = useLocation();

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check if user has required role
  const hasRequiredRole = allowedRoles.length === 0 || (user?.role && allowedRoles.includes(user.role));
  
  // Check permissions
  let hasRequiredPermissions = true;
  if (requiredPermissions.length > 0) {
    if (requireAllPermissions) {
      hasRequiredPermissions = requiredPermissions.every(permission => 
        user?.permissions?.includes(permission)
      );
    } else {
      hasRequiredPermissions = requiredPermissions.some(permission =>
        user?.permissions?.includes(permission)
      );
    }
  }

  // Redirect if user doesn't have required role or permissions
  if (!hasRequiredRole || !hasRequiredPermissions) {
    // Show error message only if we're not already on the unauthorized page
    if (location.pathname !== '/unauthorized') {
      toast.error('Você não tem permissão para acessar esta página');
    }
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;

