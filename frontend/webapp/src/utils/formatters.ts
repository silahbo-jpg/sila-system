/**
 * Módulo de formatação de dados para o frontend,
 * com suporte a formatação específica para o contexto angolano.
 * 
 * Este módulo fornece funções para formatar dados de maneira consistente,
 * como valores monetários, datas e documentos de identificação, garantindo
 * que a interface exiba os dados em um formato padronizado e familiar
 * aos usuários angolanos.
 */

/**
 * Formata um valor monetário no padrão angolano.
 * 
 * @param value - Valor a ser formatado (pode ser number, string ou undefined)
 * @param currency - Código da moeda (padrão: 'AOA' para Kwanza Angolano)
 * @param includeSymbol - Se deve incluir o símbolo da moeda (padrão: true)
 * @returns Valor formatado (ex: 'Kz 1.234,56')
 * 
 * @example
 * formatMoney(1234.5); // 'Kz 1.234,50'
 * formatMoney("1234.5", 'AOA', false); // '1.234,50'
 */
export function formatMoney(
  value: number | string | undefined, 
  currency: string = 'AOA',
  includeSymbol: boolean = true
): string {
  if (value === undefined || value === null || value === '') {
    return '';
  }
  
  let numericValue: number;
  
  // Converte para número
  if (typeof value === 'string') {
    // Remove todos os caracteres não numéricos, exceto vírgula e ponto
    const cleanValue = value.toString().replace(/[^0-9,-]+/g, '');
    // Substitui vírgula por ponto para parseFloat
    numericValue = parseFloat(cleanValue.replace(',', '.'));
  } else {
    numericValue = value;
  }
  
  // Verifica se o valor é um número válido
  if (isNaN(numericValue)) {
    return '';
  }
  
  // Formata o número com separador de milhar como ponto e decimal como vírgula
  const formattedValue = numericValue.toFixed(2)
    .replace('.', ',')
    .replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  
  // Adiciona o símbolo da moeda se solicitado
  if (includeSymbol && currency.toUpperCase() === 'AOA') {
    return `Kz ${formattedValue}`;
  }
  
  return formattedValue;
}

/**
 * Verifica se uma data é válida.
 * 
 * @param dateValue - Data a ser validada (string, Date ou undefined)
 * @returns true se a data for válida, false caso contrário
 */
function isValidDate(dateValue: string | Date | undefined): boolean {
  if (!dateValue) {
    return false;
  }
  
  try {
    const date = new Date(dateValue);
    return !isNaN(date.getTime());
  } catch (e) {
    return false;
  }
}

/**
 * Formata uma data para o formato DD-MM-YYYY, padrão angolano.
 * 
 * @param value - Data a ser formatada (string, Date ou undefined)
 * @returns Data formatada como DD-MM-YYYY ou string vazia se a data for inválida
 * 
 * @example
 * formatDate("2025-07-23"); // '23-07-2025'
 * formatDate(new Date('2025-12-31')); // '31-12-2025'
 */
export function formatDate(value: string | Date | undefined): string {
  if (!value || !isValidDate(value)) {
    return '';
  }
  
  const date = new Date(value);
  
  // Obtém dia, mês e ano
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  
  return `${day}-${month}-${year}`;
}

/**
 * Formata números de identificação angolanos (BI e CPF).
 * 
 * @param numeroBi - Número do Bilhete de Identidade (14 dígitos, formato ##########AA##)
 * @param cpf - Número de contribuinte fiscal (CPF) angolano
 * @returns Documento formatado ou string vazia se inválido
 * 
 * @example
 * formatId("1234567890AB12"); // '1234567890AB12'
 * formatId(undefined, "12345678901"); // '12345678901'
 */
export function formatId(
  numeroBi?: string,
  cpf?: string
): string {
  if (numeroBi) {
    // Remove caracteres não alfanuméricos e converte para maiúsculas
    const biClean = numeroBi.toString().replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    // Verifica se o BI tem o formato correto (14 caracteres alfanuméricos)
    if (/^[0-9]{10}[A-Z]{2}[0-9]{2}$/.test(biClean)) {
      return biClean;
    }
  }
  
  if (cpf) {
    // Remove caracteres não numéricos
    const cpfClean = cpf.toString().replace(/\D/g, '');
    // Verifica se o CPF tem entre 9 e 14 dígitos
    if (cpfClean.length >= 9 && cpfClean.length <= 14) {
      return cpfClean;
    }
  }
  
  return '';
}

/**
 * Formata um número de telefone no formato angolano.
 * 
 * @param phoneNumber - Número de telefone a ser formatado
 * @returns Número formatado ou string vazia se inválido
 * 
 * @example
 * formatPhoneNumber("923456789"); // '923 456 789'
 * formatPhoneNumber("+244923456789"); // '+244 923 456 789'
 */
export function formatPhoneNumber(phoneNumber: string): string {
  if (!phoneNumber) {
    return '';
  }
  
  // Remove todos os caracteres não numéricos
  const cleaned = phoneNumber.toString().replace(/\D/g, '');
  
  // Verifica se é um número angolano (9 dígitos começando com 9)
  if (/^9\d{8}$/.test(cleaned)) {
    return cleaned.replace(/(\d{3})(\d{3})(\d{3})/, '$1 $2 $3');
  }
  
  // Verifica se é um número internacional de Angola (código 244)
  if (/^244\d{9}$/.test(cleaned)) {
    return `+${cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{3})/, '$1 $2 $3 $4')}`;
  }
  
  // Retorna o número limpo se não corresponder a nenhum formato conhecido
  return cleaned;
}

/**
 * Formata um valor numérico como porcentagem.
 * 
 * @param value - Valor a ser formatado (0-1 ou 0-100)
 * @param isDecimal - Se true, considera que o valor está entre 0 e 1 (padrão: false)
 * @returns Valor formatado como porcentagem
 * 
 * @example
 * formatPercent(0.125, true); // '12,5%'
 * formatPercent(12.5); // '12,5%'
 */
export function formatPercent(value: number, isDecimal: boolean = false): string {
  if (value === undefined || value === null) {
    return '';
  }
  
  // Converte para decimal se necessário
  const decimalValue = isDecimal ? value * 100 : value;
  
  // Formata com 2 casas decimais e substitui ponto por vírgula
  return `${decimalValue.toFixed(2).replace('.', ',')}%`;
}

