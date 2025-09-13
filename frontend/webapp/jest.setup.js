import '@testing-library/jest-dom';

// Mock para o react-hook-form
jest.mock('react-hook-form', () => ({
  ...jest.requireActual('react-hook-form'),
  useForm: () => ({
    register: jest.fn(),
    handleSubmit: jest.fn(),
    formState: { errors: {} },
    setValue: jest.fn(),
    watch: jest.fn(),
    trigger: jest.fn(),
  }),
}));

// Mock para o FileReader
class MockFileReader {
  readAsDataURL = jest.fn();
  result = '';
  onload = () => {};
  onerror = () => {};
  
  constructor() {
    this.onload = jest.fn();
    this.onerror = jest.fn();
  }
}

global.FileReader = MockFileReader;

