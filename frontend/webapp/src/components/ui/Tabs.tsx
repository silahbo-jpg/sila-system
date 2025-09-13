import React, { Children, ReactElement, ReactNode, cloneElement, useState } from 'react';
import { cn } from '../../lib/utils';
import { useMediaQuery } from '../../hooks/useMediaQuery';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './Select';

interface TabsProps {
  children: ReactNode;
  defaultValue?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  className?: string;
  orientation?: 'horizontal' | 'vertical';
  variant?: 'default' | 'pills' | 'underline' | 'segmented';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  scrollable?: boolean;
  hideOnMobile?: boolean;
  mobileSelectLabel?: string;
  tabListClassName?: string;
  tabContentClassName?: string;
}

const Tabs = ({
  children,
  defaultValue,
  value: controlledValue,
  onValueChange,
  className,
  orientation = 'horizontal',
  variant = 'default',
  size = 'md',
  fullWidth = false,
  scrollable = false,
  hideOnMobile = true,
  mobileSelectLabel = 'Selecione uma opção',
  tabListClassName,
  tabContentClassName,
  ...props
}: TabsProps) => {
  const isMobile = useMediaQuery('(max-width: 767px)');
  const [uncontrolledValue, setUncontrolledValue] = useState(defaultValue);
  
  const isControlled = controlledValue !== undefined;
  const activeValue = isControlled ? controlledValue : uncontrolledValue;
  
  const handleValueChange = (newValue: string) => {
    if (!isControlled) {
      setUncontrolledValue(newValue);
    }
    onValueChange?.(newValue);
  };
  
  const tabs = Children.toArray(children).filter(
    (child) => React.isValidElement(child) && child.type === Tab
  ) as ReactElement<TabProps>[];
  
  const activeTab = tabs.find((tab) => tab.props.value === activeValue) || tabs[0];
  
  // If on mobile and hideOnMobile is true, render a select instead of tabs
  if (isMobile && hideOnMobile) {
    return (
      <div className={cn('w-full', className)} {...props}>
        <div className="mb-4">
          <Select
            value={activeValue}
            onValueChange={handleValueChange}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder={mobileSelectLabel} />
            </SelectTrigger>
            <SelectContent>
              {tabs.map((tab) => (
                <SelectItem
                  key={tab.props.value}
                  value={tab.props.value}
                  disabled={tab.props.disabled}
                >
                  <div className="flex items-center">
                    {tab.props.icon && <span className="mr-2">{tab.props.icon}</span>}
                    {tab.props.label || tab.props.children}
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        <div className={cn('mt-4', tabContentClassName)}>
          {activeTab?.props.children}
        </div>
      </div>
    );
  }
  
  return (
    <div
      className={cn(
        orientation === 'vertical' ? 'flex' : 'flex flex-col',
        'w-full',
        className
      )}
      {...props}
    >
      <div
        className={cn(
          'flex',
          orientation === 'vertical' ? 'flex-col items-start' : 'flex-row',
          variant === 'segmented' ? 'bg-gray-100 p-1 rounded-lg' : 'border-b border-gray-200',
          scrollable && 'overflow-x-auto hide-scrollbar',
          tabListClassName
        )}
        role="tablist"
      >
        {tabs.map((tab) => {
          const isActive = activeValue === tab.props.value;
          
          return (
            <button
              key={tab.props.value}
              type="button"
              role="tab"
              aria-selected={isActive}
              aria-controls={`tabpanel-${tab.props.value}`}
              id={`tab-${tab.props.value}`}
              disabled={tab.props.disabled}
              onClick={() => handleValueChange(tab.props.value)}
              className={cn(
                'flex items-center justify-center whitespace-nowrap font-medium transition-colors focus:outline-none',
                'disabled:opacity-50 disabled:pointer-events-none',
                {
                  // Size variants
                  'px-3 py-1.5 text-xs': size === 'sm',
                  'px-4 py-2 text-sm': size === 'md',
                  'px-5 py-2.5 text-base': size === 'lg',
                  
                  // Full width
                  'flex-1': fullWidth,
                  
                  // Default variant
                  'border-b-2': variant === 'default',
                  'text-gray-700 hover:text-gray-900 hover:border-gray-300': variant === 'default' && !isActive,
                  'text-primary-600 border-primary-500': variant === 'default' && isActive,
                  
                  // Pills variant
                  'rounded-md': variant === 'pills',
                  'text-gray-700 hover:bg-gray-100': variant === 'pills' && !isActive,
                  'bg-white shadow text-primary-700': variant === 'pills' && isActive,
                  
                  // Underline variant
                  'border-b-2 border-transparent': variant === 'underline',
                  'text-gray-500 hover:text-gray-700 hover:border-gray-300': variant === 'underline' && !isActive,
                  'text-primary-600 border-primary-500': variant === 'underline' && isActive,
                  
                  // Segmented variant
                  'rounded-md': variant === 'segmented',
                  'text-gray-600 hover:text-gray-700': variant === 'segmented' && !isActive,
                  'bg-white shadow-sm text-primary-700': variant === 'segmented' && isActive,
                }
              )}
            >
              {tab.props.icon && <span className="mr-2">{tab.props.icon}</span>}
              {tab.props.label || tab.props.children}
              {tab.props.badge && (
                <span className="ml-2 px-2 py-0.5 text-xs font-medium rounded-full bg-gray-100 text-gray-600">
                  {tab.props.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>
      
      <div
        id={`tabpanel-${activeValue}`}
        role="tabpanel"
        aria-labelledby={`tab-${activeValue}`}
        className={cn('flex-1', tabContentClassName)}
      >
        {activeTab?.props.children}
      </div>
    </div>
  );
};

interface TabProps {
  value: string;
  label?: string;
  icon?: React.ReactNode;
  badge?: string | number;
  disabled?: boolean;
  children: ReactNode;
}

const Tab: React.FC<TabProps> = ({ children }) => {
  return <>{children}</>;
};

export { Tabs, Tab };

// Utility component for tab content
interface TabContentProps {
  value: string;
  children: ReactNode;
  className?: string;
}

const TabContent: React.FC<TabContentProps> = ({ children, className }) => {
  return <div className={className}>{children}</div>;
};

export { TabContent };

