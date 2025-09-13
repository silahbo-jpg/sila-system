import React, { ReactNode } from 'react';
import { cn } from '../../utils/cn';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  variant?: 'default' | 'outline' | 'elevated' | 'filled' | 'angola' | 'angola-service';
  hoverEffect?: 'none' | 'shadow' | 'scale' | 'translate' | 'angola-hover';
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full';
  shadow?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'inner';
  className?: string;
  as?: React.ElementType;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({
    children,
    variant = 'angola',
    hoverEffect = 'angola-hover',
    rounded = 'lg',
    shadow = 'sm',
    className,
    as: Component = 'div',
    ...props
  }, ref) => {
    const baseStyles = 'overflow-hidden transition-all duration-200';
    
    const variants = {
      default: 'bg-white border border-gray-200',
      outline: 'bg-transparent border border-gray-200',
      elevated: 'bg-white shadow-md',
      filled: 'bg-gray-50 border border-gray-100',
      // Angola institutional variants
      angola: 'bg-white border-2 border-angola-gold/30 shadow-md hover:border-angola-gold/60 transition-colors duration-300',
      'angola-service': 'bg-gradient-to-br from-white to-angola-gold-light/20 border-2 border-angola-gold/40 shadow-lg hover:shadow-xl transition-all duration-300 hover:border-angola-red/30',
    };
    
    const hoverEffects = {
      none: '',
      shadow: 'hover:shadow-md',
      scale: 'hover:scale-[1.02]',
      translate: 'hover:-translate-y-0.5',
      'angola-hover': 'hover:shadow-xl hover:-translate-y-1 hover:border-angola-red/40 transition-all duration-300 ease-out transform',
    };
    
    const borderRadius = {
      none: 'rounded-none',
      sm: 'rounded-sm',
      md: 'rounded-md',
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl',
      '3xl': 'rounded-3xl',
      full: 'rounded-full',
    };
    
    const shadowSizes = {
      none: 'shadow-none',
      sm: 'shadow-sm',
      md: 'shadow',
      lg: 'shadow-md',
      xl: 'shadow-lg',
      '2xl': 'shadow-xl',
      inner: 'shadow-inner',
    };
    
    return (
      <Component
        ref={ref}
        className={cn(
          baseStyles,
          variants[variant],
          hoverEffects[hoverEffect],
          rounded ? borderRadius[rounded] : '',
          shadow ? shadowSizes[shadow] : '',
          className
        )}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  className?: string;
  withBorder?: boolean;
}

const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ children, className, withBorder = false, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'px-4 py-5 sm:px-6',
        withBorder ? 'border-b border-gray-200' : '',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
);

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: ReactNode;
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  className?: string;
  variant?: 'default' | 'angola';
}

const CardTitle = React.forwardRef<HTMLHeadingElement, CardTitleProps>(
  ({ children, as: Component = 'h3', className, variant = 'default', ...props }, ref) => {
    const titleVariants = {
      default: 'text-lg font-medium leading-6 text-gray-900',
      angola: 'text-lg font-semibold leading-6 text-angola-black flex items-center',
    };
    
    return (
      <Component
        ref={ref}
        className={cn(titleVariants[variant], className)}
        {...props}
      >
        {variant === 'angola' && (
          <span className="mr-2 text-angola-gold">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </span>
        )}
        {children}
      </Component>
    );
  }
);

interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  children: ReactNode;
  className?: string;
}

const CardDescription = React.forwardRef<HTMLParagraphElement, CardDescriptionProps>(
  ({ children, className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('mt-1 text-sm text-gray-500', className)}
      {...props}
    >
      {children}
    </p>
  )
);

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  className?: string;
  padded?: boolean;
}

const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ children, className, padded = true, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(padded ? 'p-4 sm:p-6' : '', className)}
      {...props}
    >
      {children}
    </div>
  )
);

interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  className?: string;
  withBorder?: boolean;
}

const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ children, className, withBorder = true, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'px-4 py-4 sm:px-6',
        withBorder ? 'border-t border-gray-200' : '',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
);

// Export all components
export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
};

