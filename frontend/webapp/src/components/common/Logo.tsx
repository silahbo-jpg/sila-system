import React from 'react';

interface LogoProps {
  className?: string;
  variant?: 'default' | 'inverted' | 'icon' | 'text';
  size?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'h-6',
  md: 'h-8',
  lg: 'h-10',
};

const Logo: React.FC<LogoProps> = ({ 
  className = '', 
  variant = 'default',
  size = 'md',
}) => {
  const isInverted = variant === 'inverted';
  const isIconOnly = variant === 'icon';
  const isTextOnly = variant === 'text';
  
  const textColor = isInverted ? 'text-white' : 'text-angola-black';
  const iconColor = isInverted ? 'text-white' : 'text-angola-gold';
  const sizeClass = sizeClasses[size];
  
  return (
    <div className={`flex items-center ${className}`}>
      {/* Icon */}
      {!isTextOnly && (
        <div className={`${iconColor} ${sizeClass} flex-shrink-0`}>
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            fill="currentColor"
            className="w-full h-full"
          >
            <path d="M12 2L1 12h3v9h6v-6h4v6h6v-9h3L12 2zm0 2.8L18 10v9h-2v-6h-8v6H6v-9l6-7.2z" />
          </svg>
        </div>
      )}
      
      {/* Text */}
      {!isIconOnly && (
        <span className={`ml-2 ${textColor} text-xl font-bold tracking-tight`}>
          <span className="text-angola-red">SILA</span>
          <span className="text-angola-gold mx-1">-</span>
          <span className="text-angola-black">HUAMBO</span>
        </span>
      )}
    </div>
  );
};

export default Logo;

