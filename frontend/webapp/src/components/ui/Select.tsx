import React, { SelectHTMLAttributes } from 'react';

type Option = {
  value: string | number;
  label: string;
};

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  options: Option[];
  label?: string;
  error?: string;
  className?: string;
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ options, label, error, className = '', ...props }, ref) => {
    const baseStyles = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500';
    const errorStyles = 'border-red-500 focus:border-red-500 focus:ring-red-500 dark:border-red-500 dark:focus:border-red-500 dark:focus:ring-red-500';
    
    return (
      <div className={className}>
        {label && (
          <label 
            htmlFor={props.id} 
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            {label}
          </label>
        )}
        
        <select
          ref={ref}
          className={`${baseStyles} ${error ? errorStyles : ''} ${props.disabled ? 'bg-gray-100 dark:bg-gray-800 cursor-not-allowed' : ''}`}
          {...props}
        >
          {options.map((option) => (
            <option 
              key={option.value} 
              value={option.value}
              className="dark:bg-gray-700 dark:text-white"
            >
              {option.label}
            </option>
          ))}
        </select>
        
        {error && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Select.displayName = 'Select';

export { Select };
export type { Option as SelectOption };

