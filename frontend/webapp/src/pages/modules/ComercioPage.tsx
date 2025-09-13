import React from 'react';
import { Card, Button, List, Tag } from 'antd';
import { ShopOutlined, FileDoneOutlined } from '@ant-design/icons';

const ComercioPage: React.FC = () => {
  const services = [
    {
      id: 1,
      title: 'Licença de Comércio',
      description: 'Solicite a licença para abertura de estabelecimento comercial',
      icon: <FileDoneOutlined className="text-2xl" />,
    },
    {
      id: 2,
      title: 'Alvará de Funcionamento',
      description: 'Regularize o alvará do seu estabelecimento',
      icon: <ShopOutlined className="text-2xl" />,
    },
  ];

  return (
    <div className="p-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Comércio</h1>
        <p className="text-gray-600">
          Serviços de licenciamento e regularização de estabelecimentos comerciais
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((service) => (
          <Card 
            key={service.id}
            hoverable
            className="h-full flex flex-col"
          >
            <div className="flex items-center mb-4">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
                {service.icon}
              </div>
              <h3 className="text-xl font-semibold">{service.title}</h3>
            </div>
            <p className="text-gray-600 mb-6 flex-grow">{service.description}</p>
            <Button type="primary" block>
              Solicitar
            </Button>
          </Card>
        ))}
      </div>

      <div className="mt-12">
        <h2 className="text-2xl font-semibold mb-4">Informações Importantes</h2>
        <Card>
          <List
            itemLayout="horizontal"
            dataSource={[
              'Documentação necessária para licenciamento',
              'Taxas e prazos',
              'Legislação municipal aplicável',
              'Áreas de atuação restritas',
            ]}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    <div className="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100">
                      <span className="text-blue-600">•</span>
                    </div>
                  }
                  title={item}
                />
              </List.Item>
            )}
          />
        </Card>
      </div>
    </div>
  );
};

export default ComercioPage;

