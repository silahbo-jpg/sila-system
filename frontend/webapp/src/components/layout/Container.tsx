import React from 'react';
import clsx from 'clsx';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  as?: React.ElementType;
}

const maxWidthClasses = {
  sm: 'max-w-screen-sm',
  md: 'max-w-screen-md',
  lg: 'max-w-screen-lg',
  xl: 'max-w-screen-xl',
  full: 'max-w-full',
};

const paddingClasses = {
  none: 'p-0',
  sm: 'p-4 sm:p-6',
  md: 'p-6 sm:p-8',
  lg: 'p-8 sm:p-10',
  xl: 'p-10 sm:p-12',
};

const Container: React.FC<ContainerProps> = ({
  children,
  className = '',
  size = 'xl',
  padding = 'md',
  as: Component = 'div',
  ...props
}) => {
  const containerClasses = clsx(
    'w-full mx-auto',
    maxWidthClasses[size],
    paddingClasses[padding],
    className
  );

  return (
    <Component className={containerClasses} {...props}>
      {children}
    </Component>
  );
};

export default Container;

