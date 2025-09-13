import React from 'react';
import { cn } from '../../utils/cn';

type ButtonVariant = 
  | 'primary'
  | 'secondary'
  | 'angola-primary'   // Angola red primary
  | 'angola-secondary' // Angola black secondary
  | 'angola-gold'      // Angola gold accent
  | 'success'
  | 'danger'
  | 'warning'
  | 'info'
  | 'light'
  | 'dark'
  | 'outline'
  | 'ghost';

type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

type ButtonProps = {
  children: React.ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  type?: 'button' | 'submit' | 'reset';
  isLoading?: boolean;
  disabled?: boolean;
  className?: string;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  block?: boolean; // Changed from fullWidth for consistency with Tailwind's 'block'
  rounded?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  active?: boolean;
} & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'size'>;


const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'angola-primary',
  size = 'md',
  type = 'button',
  isLoading = false,
  disabled = false,
  className = '',
  onClick,
  block = false,
  rounded = false,
  leftIcon,
  rightIcon,
  active = false,
  ...props
}) => {
  const baseStyles =
    'inline-flex items-center justify-center font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 ease-in-out disabled:opacity-70 disabled:cursor-not-allowed shadow-sm';

  const variants: Record<ButtonVariant, string> = {
    // Angola institutional colors
    'angola-primary': 'bg-angola-red text-white hover:bg-angola-red-dark focus:ring-angola-red focus:ring-offset-2 active:bg-angola-red-dark shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300',
    'angola-secondary': 'bg-angola-black text-white hover:bg-gray-800 focus:ring-angola-gold focus:ring-offset-2 active:bg-gray-800 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300',
    'angola-gold': 'bg-angola-gold text-angola-black hover:bg-angola-gold-dark focus:ring-angola-red focus:ring-offset-2 active:bg-angola-gold-dark shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 font-semibold',
    // Standard colors
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500 active:bg-primary-800',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500 active:bg-gray-800',
    success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500 active:bg-green-800',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 active:bg-red-800',
    warning: 'bg-yellow-500 text-white hover:bg-yellow-600 focus:ring-yellow-400 active:bg-yellow-700',
    info: 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-400 active:bg-blue-700',
    light: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400 active:bg-gray-400',
    dark: 'bg-gray-800 text-white hover:bg-gray-900 focus:ring-gray-700 active:bg-gray-900',
    outline: 'bg-transparent border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500 active:bg-gray-100',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-500 active:bg-gray-200 shadow-none',
  };

  const sizes: Record<ButtonSize, string> = {
    xs: 'px-2 py-1 text-xs rounded',
    sm: 'px-3 py-1.5 text-sm rounded-md',
    md: 'px-4 py-2 text-sm rounded-md',
    lg: 'px-5 py-2.5 text-base rounded-lg',
    xl: 'px-6 py-3 text-lg rounded-lg',
  };

  const activeClass = active ? 'ring-2 ring-offset-2 ring-offset-white ' + variants[variant].split(' ').find(c => c.startsWith('focus:ring-')) : '';
  const roundedClass = rounded ? 'rounded-full' : '';

  return (
    <button
      type={type}
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        block ? 'w-full' : '',
        roundedClass,
        activeClass,
        className
      )}
      disabled={disabled || isLoading}
      onClick={onClick}
      {...props}
    >
      {isLoading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {leftIcon && <span className={`mr-2 ${isLoading ? 'opacity-0' : ''}`}>{leftIcon}</span>}
      {children}
      {rightIcon && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
};

export default Button;
