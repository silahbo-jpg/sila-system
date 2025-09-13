import React from 'react';
import { FieldError, UseFormRegisterReturn } from 'react-hook-form';

type InputProps = {
  label: string;
  id: string;
  type?: string;
  placeholder?: string;
  error?: FieldError;
  register: UseFormRegisterReturn;
  disabled?: boolean;
  className?: string;
  required?: boolean;
  autoComplete?: string;
};

const Input = ({
  label,
  id,
  type = 'text',
  placeholder = '',
  error,
  register,
  disabled = false,
  className = '',
  required = false,
  autoComplete,
  ...props
}: InputProps & React.InputHTMLAttributes<HTMLInputElement>) => {
  return (
    <div className={`mb-4 ${className}`}>
      <label
        htmlFor={id}
        className={`block text-sm font-medium mb-1 ${
          error ? 'text-red-600' : 'text-gray-700'
        }`}
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <div className="relative">
        <input
          id={id}
          type={type}
          placeholder={placeholder}
          disabled={disabled}
          autoComplete={autoComplete}
          className={`block w-full px-4 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
            error
              ? 'border-red-500 bg-red-50'
              : 'border-gray-300 hover:border-gray-400'
          } ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
          {...register}
          {...props}
        />
        
        {error && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <svg
              className="h-5 w-5 text-red-500"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
          </div>
        )}
      </div>
      {error && (
        <p className="mt-1 text-sm text-red-600">
          <span className="font-medium">Erro:</span> {error.message}
        </p>
      )}
    </div>
  );
};

export default Input;

