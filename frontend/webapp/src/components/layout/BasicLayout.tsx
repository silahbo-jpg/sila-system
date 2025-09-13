import React from 'react';
import { cn } from '../../utils/cn';
import Header from './Header';
import Footer from './Footer';

interface BasicLayoutProps {
  children: React.ReactNode;
  className?: string;
  showHeader?: boolean;
  showFooter?: boolean;
  fullHeight?: boolean;
}

export const BasicLayout: React.FC<BasicLayoutProps> = ({
  children,
  className,
  showHeader = true,
  showFooter = true,
  fullHeight = true,
}) => {
  return (
    <div className={cn(
      'flex flex-col',
      fullHeight && 'min-h-screen',
      className
    )}>
      {showHeader && <Header />}
      
      <main className="flex-1 bg-gray-50">
        {children}
      </main>
      
      {showFooter && <Footer />}
    </div>
  );
};

export default BasicLayout;