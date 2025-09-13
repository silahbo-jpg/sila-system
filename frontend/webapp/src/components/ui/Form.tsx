import React, { ReactNode } from 'react';
import { FormProvider, UseFormReturn, FieldValues } from 'react-hook-form';

type FormProps<T extends FieldValues> = {
  children: ReactNode;
  methods: UseFormReturn<T>;
  onSubmit: (data: T) => void | Promise<void>;
  className?: string;
  id?: string;
};

const Form = <T extends FieldValues>({
  children,
  methods,
  onSubmit,
  className = '',
  id,
  ...props
}: FormProps<T>) => {
  return (
    <FormProvider {...methods}>
      <form
        id={id}
        onSubmit={methods.handleSubmit(onSubmit)}
        className={`space-y-4 ${className}`}
        noValidate
        {...props}
      >
        {children}
      </form>
    </FormProvider>
  );
};

export default Form;

