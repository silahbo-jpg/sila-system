import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

// Import translation files
const resources = {
  pt: {
    translation: {
      // App-level translations
      app: {
        title: 'SILA - Sistema Integrado Local de Administração',
        description: 'Plataforma Digital do Governo de Angola - Portal de Serviços ao Cidadão',
        loading: 'Carregando...',
        error: 'Erro',
        success: 'Sucesso',
        warning: 'Aviso',
        info: 'Informação',
      },
      
      // Navigation
      nav: {
        home: 'Início',
        services: 'Serviços',
        dashboard: 'Painel',
        login: 'Entrar',
        logout: 'Sair',
        training: 'Modo Treino',
        profile: 'Perfil',
        help: 'Ajuda',
        language: 'Idioma',
      },
      
      // Common actions
      actions: {
        submit: 'Submeter',
        cancel: 'Cancelar',
        save: 'Guardar',
        edit: 'Editar',
        delete: 'Eliminar',
        view: 'Ver',
        download: 'Descarregar',
        upload: 'Carregar',
        search: 'Pesquisar',
        filter: 'Filtrar',
        clear: 'Limpar',
        back: 'Voltar',
        next: 'Próximo',
        previous: 'Anterior',
        close: 'Fechar',
        open: 'Abrir',
      },
      
      // Forms
      forms: {
        required: 'Campo obrigatório',
        invalid: 'Formato inválido',
        email: 'Email inválido',
        password: 'Palavra-passe',
        confirmPassword: 'Confirmar palavra-passe',
        passwordMismatch: 'As palavras-passe não coincidem',
        name: 'Nome',
        fullName: 'Nome completo',
        idNumber: 'Número de identificação',
        phone: 'Telefone',
        address: 'Endereço',
        birthDate: 'Data de nascimento',
      },
      
      // Services
      services: {
        title: 'Serviços Disponíveis',
        health: 'Saúde',
        education: 'Educação',
        citizenship: 'Cidadania',
        finance: 'Finanças',
        justice: 'Justiça',
        urbanism: 'Urbanismo',
        consultation: 'Consulta Médica',
        identityCard: 'Carteira de Identidade',
        schoolEnrollment: 'Matrícula Escolar',
        taxConsultation: 'Consulta de Impostos',
        mediation: 'Mediação',
        buildingPermit: 'Licenciamento de Obras',
      },
      
      // Training mode
      training: {
        title: 'Modo de Treino',
        description: 'Ambiente seguro para aprender a usar os serviços SILA',
        warning: '⚠️ AMBIENTE DE TREINO - Todos os dados são fictícios',
        startSession: 'Iniciar Sessão de Treino',
        chooseModule: 'Escolher Módulo',
        progress: 'Progresso',
        completed: 'Concluído',
        inProgress: 'Em progresso',
        notStarted: 'Não iniciado',
      },
      
      // Messages
      messages: {
        welcome: 'Bem-vindo ao SILA',
        loginSuccess: 'Login realizado com sucesso',
        loginError: 'Erro no login. Verifique as suas credenciais.',
        saveSuccess: 'Dados guardados com sucesso',
        saveError: 'Erro ao guardar dados',
        deleteConfirm: 'Tem a certeza que deseja eliminar?',
        noData: 'Nenhum dado disponível',
        accessDenied: 'Acesso negado',
      },
      
      // Accessibility
      a11y: {
        skipToContent: 'Saltar para o conteúdo principal',
        menuToggle: 'Alternar menu de navegação',
        closeDialog: 'Fechar diálogo',
        openInNewTab: 'Abrir numa nova aba',
        sortAscending: 'Ordenar por ordem crescente',
        sortDescending: 'Ordenar por ordem decrescente',
      },
    },
  },
  en: {
    translation: {
      // App-level translations
      app: {
        title: 'SILA - Integrated Local Administration System',
        description: 'Digital Government Platform for Angola - Citizen Services Portal',
        loading: 'Loading...',
        error: 'Error',
        success: 'Success',
        warning: 'Warning',
        info: 'Information',
      },
      
      // Navigation
      nav: {
        home: 'Home',
        services: 'Services',
        dashboard: 'Dashboard',
        login: 'Login',
        logout: 'Logout',
        training: 'Training Mode',
        profile: 'Profile',
        help: 'Help',
        language: 'Language',
      },
      
      // Common actions
      actions: {
        submit: 'Submit',
        cancel: 'Cancel',
        save: 'Save',
        edit: 'Edit',
        delete: 'Delete',
        view: 'View',
        download: 'Download',
        upload: 'Upload',
        search: 'Search',
        filter: 'Filter',
        clear: 'Clear',
        back: 'Back',
        next: 'Next',
        previous: 'Previous',
        close: 'Close',
        open: 'Open',
      },
      
      // Forms
      forms: {
        required: 'Required field',
        invalid: 'Invalid format',
        email: 'Invalid email',
        password: 'Password',
        confirmPassword: 'Confirm password',
        passwordMismatch: 'Passwords do not match',
        name: 'Name',
        fullName: 'Full name',
        idNumber: 'ID number',
        phone: 'Phone',
        address: 'Address',
        birthDate: 'Birth date',
      },
      
      // Services
      services: {
        title: 'Available Services',
        health: 'Health',
        education: 'Education',
        citizenship: 'Citizenship',
        finance: 'Finance',
        justice: 'Justice',
        urbanism: 'Urbanism',
        consultation: 'Medical Consultation',
        identityCard: 'Identity Card',
        schoolEnrollment: 'School Enrollment',
        taxConsultation: 'Tax Consultation',
        mediation: 'Mediation',
        buildingPermit: 'Building Permit',
      },
      
      // Training mode
      training: {
        title: 'Training Mode',
        description: 'Safe environment to learn how to use SILA services',
        warning: '⚠️ TRAINING ENVIRONMENT - All data is fake',
        startSession: 'Start Training Session',
        chooseModule: 'Choose Module',
        progress: 'Progress',
        completed: 'Completed',
        inProgress: 'In progress',
        notStarted: 'Not started',
      },
      
      // Messages
      messages: {
        welcome: 'Welcome to SILA',
        loginSuccess: 'Login successful',
        loginError: 'Login error. Please check your credentials.',
        saveSuccess: 'Data saved successfully',
        saveError: 'Error saving data',
        deleteConfirm: 'Are you sure you want to delete?',
        noData: 'No data available',
        accessDenied: 'Access denied',
      },
      
      // Accessibility
      a11y: {
        skipToContent: 'Skip to main content',
        menuToggle: 'Toggle navigation menu',
        closeDialog: 'Close dialog',
        openInNewTab: 'Open in new tab',
        sortAscending: 'Sort ascending',
        sortDescending: 'Sort descending',
      },
    },
  },
}

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'pt', // Default language (Portuguese for Angola)
    fallbackLng: 'en', // Fallback language
    
    interpolation: {
      escapeValue: false, // React already escapes values
    },
    
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
    
    react: {
      useSuspense: false, // Disable suspense for SSR compatibility
    },
  })

export default i18n