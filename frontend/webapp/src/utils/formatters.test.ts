import { formatMoney, formatDate, formatId, formatPhoneNumber, formatPercent } from './formatters';

describe('Formatters', () => {
  describe('formatMoney', () => {
    it('formats money values with Kz symbol', () => {
      expect(formatMoney(1234.5)).toBe('Kz 1.234,50');
      expect(formatMoney('1234.5')).toBe('Kz 1.234,50');
      expect(formatMoney('1,234.5')).toBe('Kz 1.234,50');
    });

    it('formats money without symbol when includeSymbol is false', () => {
      expect(formatMoney(1234.5, 'AOA', false)).toBe('1.234,50');
    });

    it('returns empty string for invalid values', () => {
      expect(formatMoney(undefined)).toBe('');
      expect(formatMoney('')).toBe('');
      expect(formatMoney('abc')).toBe('');
    });
  });

  describe('formatDate', () => {
    it('formats dates in DD-MM-YYYY format', () => {
      expect(formatDate('2025-07-23')).toBe('23-07-2025');
      expect(formatDate(new Date('2025-12-31'))).toBe('31-12-2025');
    });

    it('returns empty string for invalid dates', () => {
      expect(formatDate(undefined)).toBe('');
      expect(formatDate('invalid-date')).toBe('');
    });
  });

  describe('formatId', () => {
    it('validates and formats BI numbers', () => {
      expect(formatId('1234567890AB12')).toBe('1234567890AB12');
      expect(formatId('12.345.678-90-AB-12')).toBe('1234567890AB12');
    });

    it('validates and formats CPF numbers', () => {
      expect(formatId(undefined, '12345678901')).toBe('12345678901');
      expect(formatId(undefined, '123.456.789-01')).toBe('12345678901');
    });

    it('returns empty string for invalid IDs', () => {
      expect(formatId('123')).toBe('');
      expect(formatId(undefined, '123')).toBe('');
    });
  });

  describe('formatPhoneNumber', () => {
    it('formats Angolan phone numbers', () => {
      expect(formatPhoneNumber('923456789')).toBe('923 456 789');
      expect(formatPhoneNumber('+244923456789')).toBe('+244 923 456 789');
    });

    it('returns cleaned number for unknown formats', () => {
      expect(formatPhoneNumber('12345')).toBe('12345');
    });
  });

  describe('formatPercent', () => {
    it('formats decimal values as percentage', () => {
      expect(formatPercent(12.5)).toBe('12,50%');
      expect(formatPercent(0.125, true)).toBe('12,50%');
    });
  });
});

