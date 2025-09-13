import { ReactNode } from 'react';
import { useAuth, Role } from '../store/auth';
export default function RoleGuard({ allow, children }:{allow:Role|Role[];children:ReactNode}){
  const { hasRole } = useAuth();
  return hasRole(allow) ? <>{children}</> : <div className="p-6">Acesso negado</div>;
}

