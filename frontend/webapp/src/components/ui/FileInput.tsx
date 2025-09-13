import React, { ChangeEvent, ReactNode } from 'react';
import { FieldError, UseFormRegisterReturn } from 'react-hook-form';

type FileInputProps = {
  label: string;
  id: string;
  accept?: string;
  error?: FieldError;
  register: UseFormRegisterReturn;
  disabled?: boolean;
  className?: string;
  required?: boolean;
  multiple?: boolean;
  preview?: ReactNode;
  helperText?: string;
};

const FileInput = ({
  label,
  id,
  accept,
  error,
  register,
  disabled = false,
  className = '',
  required = false,
  multiple = false,
  preview,
  helperText,
  ...props
}: FileInputProps & React.InputHTMLAttributes<HTMLInputElement>) => {
  const { onChange, ...restRegister } = register;
  
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (onChange) {
      // Garante que o evento seja passado corretamente para o react-hook-form
      const event = {
        target: {
          name: register.name,
          value: e.target.files
        }
      };
      onChange(event as any);
    }
  };

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
          type="file"
          accept={accept}
          disabled={disabled}
          className={`block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-colors ${
            error ? 'border-red-500' : 'border-gray-300'
          } ${disabled ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'}`}
          multiple={multiple}
          onChange={handleChange}
          {...restRegister}
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
      
      {helperText && !error && (
        <p className="mt-1 text-xs text-gray-500">{helperText}</p>
      )}
      
      {error && (
        <p className="mt-1 text-sm text-red-600">
          <span className="font-medium">Erro:</span> {error.message}
        </p>
      )}
      
      {preview && <div className="mt-2">{preview}</div>}
    </div>
  );
};

export default FileInput;

