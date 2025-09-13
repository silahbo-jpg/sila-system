import React from 'react';
import { Link } from 'react-router-dom';
import { cn } from '../../utils/cn';

interface FooterProps {
  className?: string;
}

export const Footer: React.FC<FooterProps> = ({ className }) => {
  return (
    <footer className={cn(
      'bg-angola-black border-t-2 border-angola-gold mt-auto',
      className
    )}>
      <div className="page-container py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <span className="mr-2 text-angola-gold">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L1 12h3v9h6v-6h4v6h6v-9h3L12 2zm0 2.8L18 10v9h-2v-6h-8v6H6v-9l6-7.2z" />
                </svg>
              </span>
              SILA - HUAMBO
            </h3>
            <p className="text-gray-300 text-sm leading-relaxed">
              SILA - Sistema Integrado Local de Administração.
              <br />
              <span className="text-angola-gold font-medium">Modernizando os serviços municipais de Huambo.</span>
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold text-white mb-4 border-b border-angola-red/30 pb-2">Links Rápidos</h4>
            <ul className="space-y-3">
              <li>
                <Link 
                  to="/services" 
                  className="text-gray-300 hover:text-angola-gold text-sm transition-colors duration-300 flex items-center group"
                >
                  <span className="mr-2 text-angola-red group-hover:text-angola-gold transition-colors">•</span>
                  Catálogo de Serviços
                </Link>
              </li>
              <li>
                <Link 
                  to="/about" 
                  className="text-gray-300 hover:text-angola-gold text-sm transition-colors duration-300 flex items-center group"
                >
                  <span className="mr-2 text-angola-red group-hover:text-angola-gold transition-colors">•</span>
                  Sobre o SILA
                </Link>
              </li>
              <li>
                <Link 
                  to="/contact" 
                  className="text-gray-300 hover:text-angola-gold text-sm transition-colors duration-300 flex items-center group"
                >
                  <span className="mr-2 text-angola-red group-hover:text-angola-gold transition-colors">•</span>
                  Contato
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold text-white mb-4 border-b border-angola-red/30 pb-2">Suporte Institucional</h4>
            <div className="space-y-3">
              <p className="text-gray-300 text-sm mb-3">
                <span className="text-angola-gold font-medium">Administração Municipal de Huambo</span>
                <br />Precisa de ajuda? Entre em contato:
              </p>
              <div className="space-y-2">
                <p className="text-gray-300 text-sm flex items-center">
                  <span className="mr-2 text-angola-gold">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                    </svg>
                  </span>
                  suporte@sila.gov.ao
                </p>
                <p className="text-gray-300 text-sm flex items-center">
                  <span className="mr-2 text-angola-gold">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                    </svg>
                  </span>
                  Tel/WhatsApp: 926880397
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-8 pt-6 border-t border-angola-red/30 flex flex-col sm:flex-row justify-between items-center">
          <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <p className="text-gray-400 text-sm flex items-center">
              <span className="mr-2 text-angola-gold">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </span>
              © {new Date().getFullYear()} Administração Municipal de Huambo
            </p>
            <p className="text-gray-400 text-xs">
              Todos os direitos reservados.
            </p>
          </div>
          <div className="flex space-x-6 mt-4 sm:mt-0">
            <Link 
              to="/privacy" 
              className="text-gray-400 hover:text-angola-gold text-sm transition-colors duration-300"
            >
              Privacidade
            </Link>
            <span className="text-angola-red">•</span>
            <Link 
              to="/terms" 
              className="text-gray-400 hover:text-angola-gold text-sm transition-colors duration-300"
            >
              Termos
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;