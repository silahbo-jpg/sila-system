import React from 'react';
import { Link } from 'react-router-dom';
import { cn } from '../../utils/cn';

interface HeaderProps {
  className?: string;
  sticky?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ 
  className, 
  sticky = true 
}) => {
  return (
    <header className={cn(
      'bg-angola-red border-b-2 border-angola-gold shadow-lg',
      sticky && 'sticky top-0 z-50',
      className
    )}>
      <div className="page-container">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-4">
            <Link 
              to="/" 
              className="text-xl font-bold text-white hover:text-angola-gold transition-colors duration-300 flex items-center"
            >
              <span className="mr-2 text-angola-gold">
                {/* Angola-inspired icon/emblem */}
                <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L1 12h3v9h6v-6h4v6h6v-9h3L12 2zm0 2.8L18 10v9h-2v-6h-8v6H6v-9l6-7.2z" />
                </svg>
              </span>
              SILA - HUAMBO
            </Link>
          </div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <Link 
              to="/dashboard" 
              className="text-white/90 hover:text-angola-gold font-medium px-3 py-2 rounded-md transition-colors duration-300"
            >
              Dashboard
            </Link>
            <Link 
              to="/services" 
              className="text-white/90 hover:text-angola-gold font-medium px-3 py-2 rounded-md transition-colors duration-300"
            >
              Serviços
            </Link>
            <Link 
              to="/about" 
              className="text-white/90 hover:text-angola-gold font-medium px-3 py-2 rounded-md transition-colors duration-300"
            >
              Sobre
            </Link>
          </nav>
          
          <div className="md:hidden">
            <button
              type="button"
              className="text-white hover:text-angola-gold focus:outline-none focus:ring-2 focus:ring-angola-gold p-2 rounded-md transition-colors duration-300"
              aria-label="Toggle menu"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;