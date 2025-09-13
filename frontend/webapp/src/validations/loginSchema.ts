import { z } from 'zod';

export const loginSchema = z.object({
  username: z.string()
    .min(3, { message: 'O nome de usuário deve ter pelo menos 3 caracteres' })
    .max(50, { message: 'O nome de usuário não pode ter mais de 50 caracteres' })
    .regex(/^[a-zA-Z0-9_]+$/, { 
      message: 'Use apenas letras, números e sublinhado (_)' 
    }),
  
  password: z.string()
    .min(6, { message: 'A senha deve ter pelo menos 6 caracteres' })
    .max(100, { message: 'A senha não pode ter mais de 100 caracteres' })
});

export type LoginFormData = z.infer<typeof loginSchema>;

