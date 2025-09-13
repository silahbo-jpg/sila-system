import { ReactNode } from 'react';
import { 
  HomeIcon, 
  UserGroupIcon, 
  AcademicCapIcon,
  BuildingOffice2Icon,
  HeartIcon,
  ScaleIcon,
  WrenchScrewdriverIcon,
  TruckIcon,
  GlobeAltIcon,
  CurrencyDollarIcon,
  ClipboardDocumentCheckIcon,
  ShieldCheckIcon,
  BellAlertIcon,
  DocumentTextIcon,
  LightBulbIcon,
} from '@heroicons/react/24/outline';

export interface Module {
  id: string;
  name: string;
  description: string;
  icon: ReactNode;
  path: string;
  status: 'active' | 'coming-soon' | 'beta' | 'maintenance';
  featured: boolean;
  category: string;
  featureFlag: string;
  permissions?: string[];
  submodules?: Array<{
    id: string;
    name: string;
    description: string;
    path: string;
    icon: ReactNode;
    permissions?: string[];
  }>;
}

// Helper to create consistent icon styling
const createIcon = (Icon: any) => (
  <div className="p-2 rounded-lg bg-primary-100 text-primary-600">
    <Icon className="h-6 w-6" />
  </div>
);

export const modules: Module[] = [
  {
    id: 'citizenship',
    name: 'Cidadania',
    description: 'Documentos, certidões e serviços de identificação do cidadão',
    icon: createIcon(UserGroupIcon),
    path: '/cidadania',
    status: 'active',
    featured: true,
    category: 'Cidadão',
    featureFlag: 'module.citizenship',
    permissions: ['citizen.access'],
    submodules: [
      {
        id: 'document-request',
        name: 'Solicitar Documentos',
        description: 'Solicite certidões e documentos pessoais',
        path: '/cidadania/documentos/solicitar',
        icon: createIcon(DocumentTextIcon),
        permissions: ['citizen.documents.request'],
      },
      {
        id: 'id-card',
        name: 'Carteira de Identidade',
        description: 'Emita sua segunda via do RG',
        path: '/cidadania/rg',
        icon: createIcon(ShieldCheckIcon),
        permissions: ['citizen.documents.id_card'],
      },
    ],
  },
  {
    id: 'education',
    name: 'Educação',
    description: 'Matrículas, boletins e serviços educacionais',
    icon: createIcon(AcademicCapIcon),
    path: '/educacao',
    status: 'active',
    featured: true,
    category: 'Cidadão',
    featureFlag: 'module.education',
    permissions: ['education.access'],
  },
  {
    id: 'health',
    name: 'Saúde',
    description: 'Agendamentos, prontuário e serviços de saúde',
    icon: createIcon(HeartIcon),
    path: '/saude',
    status: 'coming-soon',
    featured: true,
    category: 'Cidadão',
    featureFlag: 'module.health',
  },
  {
    id: 'urbanism',
    name: 'Urbanismo',
    description: 'Licenças, alvarás e serviços de urbanização',
    icon: createIcon(BuildingOffice2Icon),
    path: '/urbanismo',
    status: 'coming-soon',
    featured: false,
    category: 'Empresa',
    featureFlag: 'module.urbanism',
  },
  {
    id: 'sanitation',
    name: 'Saneamento',
    description: 'Solicitações e serviços de limpeza urbana',
    icon: createIcon(WrenchScrewdriverIcon),
    path: '/saneamento',
    status: 'coming-soon',
    featured: false,
    category: 'Cidadão',
    featureFlag: 'module.sanitation',
  },
  {
    id: 'transport',
    name: 'Transporte',
    description: 'Passe escolar, bilhetes e informações de transporte',
    icon: createIcon(TruckIcon),
    path: '/transporte',
    status: 'coming-soon',
    featured: false,
    category: 'Cidadão',
    featureFlag: 'module.transport',
  },
  {
    id: 'tourism',
    name: 'Turismo',
    description: 'Pontos turísticos e eventos culturais',
    icon: createIcon(GlobeAltIcon),
    path: '/turismo',
    status: 'coming-soon',
    featured: false,
    category: 'Visitante',
    featureFlag: 'module.tourism',
  },
  {
    id: 'commerce',
    name: 'Comércio',
    description: 'Alvarás e serviços para empreendedores',
    icon: createIcon(CurrencyDollarIcon),
    path: '/comercio',
    status: 'beta',
    featured: true,
    category: 'Empresa',
    featureFlag: 'module.commerce',
  },
  {
    id: 'social-assistance',
    name: 'Assistência Social',
    description: 'Programas e benefícios sociais',
    icon: createIcon(HeartIcon),
    path: '/assistencia-social',
    status: 'active',
    featured: false,
    category: 'Cidadão',
    featureFlag: 'module.social_assistance',
  },
  {
    id: 'public-services',
    name: 'Serviços Públicos',
    description: 'Solicitações e serviços municipais',
    icon: createIcon(ClipboardDocumentCheckIcon),
    path: '/servicos-publicos',
    status: 'active',
    featured: false,
    category: 'Cidadão',
    featureFlag: 'module.public_services',
  },
  {
    id: 'notifications',
    name: 'Notificações',
    description: 'Acompanhe suas notificações e alertas',
    icon: createIcon(BellAlertIcon),
    path: '/notificacoes',
    status: 'active',
    featured: false,
    category: 'Geral',
    featureFlag: 'feature.notifications',
  },
  {
    id: 'suggestions',
    name: 'Sugestões',
    description: 'Envie sugestões para melhorar nossos serviços',
    icon: createIcon(LightBulbIcon),
    path: '/sugestoes',
    status: 'active',
    featured: false,
    category: 'Geral',
    featureFlag: 'feature.suggestions',
  },
];

// Helper functions to filter modules
export const getFeaturedModules = () => 
  modules.filter(module => module.featured && module.status === 'active');

export const getModulesByCategory = (category: string) => 
  modules.filter(module => module.category === category);

export const getActiveModules = () => 
  modules.filter(module => module.status === 'active');

export const getModuleById = (id: string) => 
  modules.find(module => module.id === id);

export default modules;

