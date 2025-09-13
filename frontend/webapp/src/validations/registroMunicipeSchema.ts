import { z } from 'zod';

// Expressão regular para validar BI angolano (exemplo: 000000000LA042)
const biRegex = /^\d{9}[A-Z]{2}\d{3}$/i;

// Expressão regular para validar número de telefone angolano (ex: 923456789, 912345678)
const phoneRegex = /^[9][1-9]\d{7}$/;

export const registroMunicipeSchema = z.object({
  // Nome completo (mínimo 3 caracteres, máximo 100)
  nome: z.string()
    .min(3, { message: 'O nome deve ter pelo menos 3 caracteres' })
    .max(100, { message: 'O nome não pode ter mais de 100 caracteres' })
    .transform(name => {
      return name.trim().split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
    }),

  // Número do BI (formato: 9 dígitos + 2 letras + 3 dígitos)
  numero_bi: z.string()
    .regex(biRegex, { 
      message: 'Formato de BI inválido. Use o formato: 000000000LA042' 
    })
    .transform(bi => bi.toUpperCase()),

  // Foto do rosto (opcional, mas se enviada deve ser uma imagem)
  foto: z.instanceof(FileList)
    .refine(files => files.length === 0 || files[0]?.type.startsWith('image/'), {
      message: 'O arquivo deve ser uma imagem',
    })
    .optional()
    .nullable(),

  // Anexo do BI (opcional, mas se enviado deve ser PDF)
  bi_anexo: z.instanceof(FileList)
    .refine(files => files.length === 0 || files[0]?.type === 'application/pdf', {
      message: 'O arquivo deve ser um PDF',
    })
    .optional()
    .nullable(),
});

// Tipo TypeScript inferido do schema
export type RegistroMunicipeFormData = z.infer<typeof registroMunicipeSchema>;

