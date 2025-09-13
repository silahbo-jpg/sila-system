import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

type ModuleStatus = 'active' | 'coming-soon' | 'beta' | 'maintenance';

interface ModuleCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  status?: ModuleStatus;
  className?: string;
  onClick?: () => void;
}

const statusStyles = {
  active: 'bg-green-100 text-green-800',
  'coming-soon': 'bg-blue-100 text-blue-800',
  beta: 'bg-yellow-100 text-yellow-800',
  maintenance: 'bg-red-100 text-red-800',
};

const statusLabels = {
  active: 'Disponível',
  'coming-soon': 'Em Breve',
  beta: 'Beta',
  maintenance: 'Manutenção',
};

export const ModuleCard: React.FC<ModuleCardProps> = ({
  title,
  description,
  icon,
  status = 'active',
  className = '',
  onClick,
}) => {
  const navigate = useNavigate();
  const isDisabled = status !== 'active';
  
  const defaultIcon = (
    <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-600">
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        className="h-6 w-6" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" 
        />
      </svg>
    </div>
  );

  const handleClick = () => {
    if (isDisabled) return;
    
    if (onClick) {
      onClick();
    } else {
      // Default navigation behavior if no onClick provided
      const path = `/modulos/${title.toLowerCase().replace(/\s+/g, '-')}`;
      navigate(path);
    }
  };

  return (
    <motion.div
      whileHover={!isDisabled ? { y: -4, boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)' } : {}}
      transition={{ type: 'spring', stiffness: 400, damping: 10 }}
      onClick={handleClick}
      className={`
        relative bg-white rounded-xl p-6 border border-gray-200 overflow-hidden 
        ${isDisabled ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer hover:shadow-lg transition-shadow'}
        ${className}
      `}
    >
      {/* Status Badge */}
      {status !== 'active' && (
        <div className={`absolute top-3 right-3 text-xs font-medium px-2.5 py-0.5 rounded-full ${statusStyles[status]}`}>
          {statusLabels[status]}
        </div>
      )}
      
      {/* Icon */}
      <div className="mb-4">
        {icon || defaultIcon}
      </div>
      
      {/* Content */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600 text-sm">
          {description}
        </p>
      </div>
      
      {/* Action Button */}
      <div className="mt-6">
        <button
          disabled={isDisabled}
          className={`
            w-full py-2 px-4 rounded-lg text-sm font-medium transition-colors
            ${
              isDisabled
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-primary-50 text-primary-700 hover:bg-primary-100'
            }
          `}
        >
          {isDisabled ? 'Indisponível' : 'Acessar'}
        </button>
      </div>
      
      {/* Hover overlay */}
      {!isDisabled && (
        <div className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent opacity-0 hover:opacity-100 transition-opacity rounded-xl" />
      )}
    </motion.div>
  );
};

export default ModuleCard;

