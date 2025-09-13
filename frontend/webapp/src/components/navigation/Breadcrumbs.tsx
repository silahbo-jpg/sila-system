import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

interface BreadcrumbItem {
  name: string;
  path: string;
  current?: boolean;
}

const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);
  
  // Don't show breadcrumbs on the home page
  if (pathnames.length === 0) {
    return null;
  }
  
  // Generate breadcrumb items
  const breadcrumbItems = pathnames.reduce<BreadcrumbItem[]>((items, path, index) => {
    // Skip numeric paths (likely IDs)
    if (/^\d+$/.test(path)) {
      return items;
    }
    
    const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
    const name = path
      .split('-')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
    
    // Skip specific paths that don't need breadcrumbs
    if (['app', 'auth', 'public'].includes(path)) {
      return items;
    }
    
    return [
      ...items,
      {
        name,
        path: routeTo,
        current: index === pathnames.length - 1,
      },
    ];
  }, []);
  
  // If no valid breadcrumb items, don't render anything
  if (breadcrumbItems.length === 0) {
    return null;
  }
  
  return (
    <nav className="flex" aria-label="Breadcrumb">
      <ol role="list" className="flex items-center space-x-2 sm:space-x-3 overflow-x-auto py-2 px-1">
        <li>
          <div>
            <Link to="/" className="text-gray-400 hover:text-gray-500">
              <Home className="flex-shrink-0 h-5 w-5" aria-hidden="true" />
              <span className="sr-only">Início</span>
            </Link>
          </div>
        </li>
        
        {breadcrumbItems.map((item, index) => (
          <li key={item.path} className="flex items-center">
            <ChevronRight className="flex-shrink-0 h-5 w-5 text-gray-400" aria-hidden="true" />
            {item.current ? (
              <span className="ml-2 sm:ml-3 text-sm font-medium text-gray-500 truncate max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl">
                {item.name}
              </span>
            ) : (
              <Link
                to={item.path}
                className="ml-2 sm:ml-3 text-sm font-medium text-gray-500 hover:text-gray-700 truncate max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl"
              >
                {item.name}
              </Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};

export default Breadcrumbs;

