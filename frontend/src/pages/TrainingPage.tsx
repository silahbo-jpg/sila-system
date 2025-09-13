import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  AcademicCapIcon,
  PlayIcon,
  BookOpenIcon,
  CheckCircleIcon,
  ClockIcon,
  UserGroupIcon,
  ChartBarIcon,
  LightBulbIcon,
  DocumentTextIcon,
  VideoCameraIcon
} from '@heroicons/react/24/outline';

interface TrainingModule {
  id: string;
  title: string;
  title_en: string;
  description: string;
  description_en: string;
  category: string;
  duration: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  completionRate: number;
  enrolled: number;
  status: 'available' | 'locked' | 'completed';
  type: 'video' | 'interactive' | 'document' | 'quiz';
}

interface TrainingStats {
  totalModules: number;
  completedModules: number;
  totalHours: number;
  certificatesEarned: number;
}

const TrainingPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [modules, setModules] = useState<TrainingModule[]>([]);
  const [stats, setStats] = useState<TrainingStats>({
    totalModules: 0,
    completedModules: 0,
    totalHours: 0,
    certificatesEarned: 0
  });
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  const categories = [
    'digital_services',
    'citizen_support',
    'data_management',
    'security_compliance',
    'customer_service',
    'technical_skills'
  ];

  const difficulties = ['beginner', 'intermediate', 'advanced'];

  useEffect(() => {
    const loadTrainingData = async () => {
      setIsLoading(true);

      // Mock training modules data
      const mockModules: TrainingModule[] = [
        {
          id: '1',
          title: 'Introdução aos Serviços Digitais do SILA',
          title_en: 'Introduction to SILA Digital Services',
          description: 'Aprenda os fundamentos da plataforma SILA e como navegar pelos serviços digitais',
          description_en: 'Learn the fundamentals of the SILA platform and how to navigate digital services',
          category: 'digital_services',
          duration: '45 min',
          difficulty: 'beginner',
          completionRate: 92,
          enrolled: 1250,
          status: 'available',
          type: 'video'
        },
        {
          id: '2',
          title: 'Atendimento ao Cidadão: Melhores Práticas',
          title_en: 'Citizen Support: Best Practices',
          description: 'Técnicas para fornecer suporte eficaz aos cidadãos usando a plataforma SILA',
          description_en: 'Techniques for providing effective support to citizens using the SILA platform',
          category: 'citizen_support',
          duration: '1h 20min',
          difficulty: 'intermediate',
          completionRate: 87,
          enrolled: 890,
          status: 'available',
          type: 'interactive'
        },
        {
          id: '3',
          title: 'Gestão de Dados e Relatórios',
          title_en: 'Data Management and Reporting',
          description: 'Como gerenciar dados governamentais e gerar relatórios precisos',
          description_en: 'How to manage government data and generate accurate reports',
          category: 'data_management',
          duration: '2h 15min',
          difficulty: 'advanced',
          completionRate: 76,
          enrolled: 445,
          status: 'available',
          type: 'document'
        },
        {
          id: '4',
          title: 'Conformidade e Segurança Digital',
          title_en: 'Digital Compliance and Security',
          description: 'Protocolos de segurança e conformidade para serviços governamentais digitais',
          description_en: 'Security and compliance protocols for digital government services',
          category: 'security_compliance',
          duration: '1h 45min',
          difficulty: 'intermediate',
          completionRate: 94,
          enrolled: 678,
          status: 'completed',
          type: 'quiz'
        }
      ];

      const mockStats: TrainingStats = {
        totalModules: 12,
        completedModules: 3,
        totalHours: 15,
        certificatesEarned: 2
      };

      setTimeout(() => {
        setModules(mockModules);
        setStats(mockStats);
        setIsLoading(false);
      }, 1000);
    };

    loadTrainingData();
  }, []);

  const filteredModules = modules.filter(module => {
    const categoryMatch = selectedCategory === 'all' || module.category === selectedCategory;
    const difficultyMatch = selectedDifficulty === 'all' || module.difficulty === selectedDifficulty;
    return categoryMatch && difficultyMatch;
  });

  const getDifficultyColor = (difficulty: TrainingModule['difficulty']) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: TrainingModule['status']) => {
    switch (status) {
      case 'available': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'locked': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: TrainingModule['type']) => {
    switch (type) {
      case 'video': return VideoCameraIcon;
      case 'interactive': return LightBulbIcon;
      case 'document': return DocumentTextIcon;
      case 'quiz': return CheckCircleIcon;
      default: return BookOpenIcon;
    }
  };

  const startModule = (moduleId: string) => {
    // In a real app, this would navigate to the training module
    alert(t('training.startModule.comingSoon'));
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sila-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <AcademicCapIcon className="w-8 h-8 text-sila-primary mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">
              {t('training.title')}
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            {t('training.subtitle')}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <BookOpenIcon className="w-8 h-8 text-sila-primary" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{t('training.stats.totalModules')}</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalModules}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <CheckCircleIcon className="w-8 h-8 text-green-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{t('training.stats.completed')}</p>
                <p className="text-2xl font-bold text-gray-900">{stats.completedModules}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <ClockIcon className="w-8 h-8 text-blue-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{t('training.stats.totalHours')}</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalHours}h</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center">
              <ChartBarIcon className="w-8 h-8 text-yellow-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{t('training.stats.certificates')}</p>
                <p className="text-2xl font-bold text-gray-900">{stats.certificatesEarned}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                {t('training.filters.category')}
              </label>
              <select
                id="category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
              >
                <option value="all">{t('training.filters.allCategories')}</option>
                {categories.map(category => (
                  <option key={category} value={category}>
                    {t(`training.categories.${category}`)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-2">
                {t('training.filters.difficulty')}
              </label>
              <select
                id="difficulty"
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
              >
                <option value="all">{t('training.filters.allDifficulties')}</option>
                {difficulties.map(difficulty => (
                  <option key={difficulty} value={difficulty}>
                    {t(`training.difficulty.${difficulty}`)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Training Modules */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredModules.map((module) => {
            const TypeIcon = getTypeIcon(module.type);
            return (
              <div key={module.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
                <div className="p-6">
                  {/* Module Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center flex-1">
                      <TypeIcon className="w-6 h-6 text-sila-primary mr-3" />
                      <h3 className="text-lg font-semibold text-gray-900">
                        {i18n.language === 'pt' ? module.title : module.title_en}
                      </h3>
                    </div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(module.status)}`}>
                      {t(`training.status.${module.status}`)}
                    </span>
                  </div>

                  {/* Module Description */}
                  <p className="text-gray-600 text-sm mb-4">
                    {i18n.language === 'pt' ? module.description : module.description_en}
                  </p>

                  {/* Module Metadata */}
                  <div className="flex flex-wrap gap-4 mb-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getDifficultyColor(module.difficulty)}`}>
                      {t(`training.difficulty.${module.difficulty}`)}
                    </span>
                    <div className="flex items-center text-sm text-gray-500">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      {module.duration}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <UserGroupIcon className="w-4 h-4 mr-1" />
                      {module.enrolled} {t('training.enrolled')}
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="mb-4">
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>{t('training.completionRate')}</span>
                      <span>{module.completionRate}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-sila-primary h-2 rounded-full" 
                        style={{ width: `${module.completionRate}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Action Button */}
                  <button
                    onClick={() => startModule(module.id)}
                    disabled={module.status === 'locked'}
                    className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {module.status === 'completed' ? (
                      <>
                        <CheckCircleIcon className="w-4 h-4 mr-2" />
                        {t('training.actions.review')}
                      </>
                    ) : module.status === 'locked' ? (
                      <>
                        {t('training.actions.locked')}
                      </>
                    ) : (
                      <>
                        <PlayIcon className="w-4 h-4 mr-2" />
                        {t('training.actions.start')}
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* No Results */}
        {filteredModules.length === 0 && (
          <div className="text-center py-12">
            <AcademicCapIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {t('training.noResults.title')}
            </h3>
            <p className="text-gray-600">
              {t('training.noResults.description')}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrainingPage;