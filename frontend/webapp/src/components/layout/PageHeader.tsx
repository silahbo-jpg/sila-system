import React, { ReactNode } from 'react';
import { Button } from '../ui/Button';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '../../lib/utils';

interface PageHeaderProps {
  title: string;
  description?: string | ReactNode;
  backButton?: boolean;
  backButtonLabel?: string;
  backButtonHref?: string;
  actions?: ReactNode;
  breadcrumbs?: boolean;
  className?: string;
  titleClassName?: string;
  descriptionClassName?: string;
  headerClassName?: string;
  children?: ReactNode;
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  backButton = false,
  backButtonLabel = 'Voltar',
  backButtonHref,
  actions,
  breadcrumbs = true,
  className = '',
  titleClassName = '',
  descriptionClassName = '',
  headerClassName = '',
  children,
}) => {
  const navigate = useNavigate();
  
  const handleBack = () => {
    if (backButtonHref) {
      navigate(backButtonHref);
    } else {
      navigate(-1);
    }
  };

  return (
    <div className={cn('bg-white', className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {breadcrumbs && (
          <div className="py-4">
            <Breadcrumbs />
          </div>
        )}
        
        <div className={cn('py-6 md:flex md:items-center md:justify-between', headerClassName)}>
          <div className="min-w-0 flex-1">
            {backButton && (
              <Button
                variant="ghost"
                size="sm"
                onClick={handleBack}
                className="mb-4 -ml-3 px-3"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                {backButtonLabel}
              </Button>
            )}
            
            <h1 className={cn(
              'text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight',
              titleClassName
            )}>
              {title}
            </h1>
            
            {description && (
              <p className={cn(
                'mt-2 max-w-4xl text-sm text-gray-500',
                descriptionClassName
              )}>
                {description}
              </p>
            )}
            
            {children && (
              <div className="mt-4">
                {children}
              </div>
            )}
          </div>
          
          {actions && (
            <div className="mt-4 flex-shrink-0 flex flex-wrap gap-3 md:mt-0 md:ml-4">
              {Array.isArray(actions) ? (
                actions.map((action, index) => (
                  <div key={index} className="flex-shrink-0">
                    {action}
                  </div>
                ))
              ) : (
                <div className="flex-shrink-0">
                  {actions}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PageHeader;

