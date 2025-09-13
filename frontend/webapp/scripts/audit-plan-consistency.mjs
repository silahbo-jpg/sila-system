import { existsSync, readdirSync } from 'fs';
import { resolve } from 'path';
const r = (p) => resolve(process.cwd(), p);

const checks = [
  'src/services/api.ts',
  'src/store/auth.ts',
  'src/routes/ProtectedRoute.tsx',
  'src/routes/RoleGuard.tsx',
  'src/config/services.json',
  'src/pages/Servicos.tsx',
  'src/services/ServiceView.tsx',
];

console.log('— Audit: plano de harmonização\n');
for (const c of checks) {
  console.log(`${existsSync(r(c)) ? 'OK   ' : 'MISS '} ${c}`);
}

const pages = resolve(process.cwd(), 'src/pages');
if (existsSync(pages)) {
  const list = readdirSync(pages).filter(f => /login/i.test(f));
  console.log(`\nPáginas de login detectadas: ${list.join(', ') || 'nenhuma'}`);
}

