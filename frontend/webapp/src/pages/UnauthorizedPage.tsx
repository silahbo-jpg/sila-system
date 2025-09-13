import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Result } from 'antd';

const UnauthorizedPage: React.FC = () => {
  const navigate = useNavigate();
  
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <Result
        status="403"
        title="403"
        subTitle="Desculpe, você não está autorizado a acessar esta página."
        extra={
          <Button 
            type="primary" 
            onClick={() => navigate('/')}
          >
            Voltar para a Página Inicial
          </Button>
        }
      />
    </div>
  );
};

export default UnauthorizedPage;

