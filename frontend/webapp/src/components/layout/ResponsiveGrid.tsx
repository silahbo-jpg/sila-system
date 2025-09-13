import React from 'react';
import clsx from 'clsx';

interface ResponsiveGridProps {
  children: React.ReactNode;
  className?: string;
  cols?: {
    xs?: number;
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    '2xl'?: number;
  };
  gap?: 'none' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  as?: React.ElementType;
}

const gapClasses = {
  none: 'gap-0',
  xs: 'gap-1 sm:gap-2',
  sm: 'gap-2 sm:gap-3',
  md: 'gap-3 sm:gap-4',
  lg: 'gap-4 sm:gap-6',
  xl: 'gap-6 sm:gap-8',
  '2xl': 'gap-8 sm:gap-10',
};

const ResponsiveGrid: React.FC<ResponsiveGridProps> = ({
  children,
  className = '',
  cols = { xs: 1, sm: 2, md: 3, lg: 4, xl: 4, '2xl': 5 },
  gap = 'md',
  as: Component = 'div',
  ...props
}) => {
  const gridCols = {
    xs: `grid-cols-${cols.xs || 1}`,
    sm: `sm:grid-cols-${cols.sm || cols.xs || 2}`,
    md: `md:grid-cols-${cols.md || cols.sm || 3}`,
    lg: `lg:grid-cols-${cols.lg || cols.md || 4}`,
    xl: `xl:grid-cols-${cols.xl || cols.lg || 5}`,
    '2xl': `2xl:grid-cols-${cols['2xl'] || cols.xl || 6}`,
  };

  const gridClasses = clsx(
    'grid',
    gapClasses[gap],
    gridCols.xs,
    gridCols.sm,
    gridCols.md,
    gridCols.lg,
    gridCols.xl,
    gridCols['2xl'],
    className
  );

  return (
    <Component className={gridClasses} {...props}>
      {children}
    </Component>
  );
};

export default ResponsiveGrid;

