import React from 'react';
import { Card, Button, List, Tag, Space } from 'antd';
import { FileDoneOutlined, ClockCircleOutlined, CheckCircleOutlined, PlusOutlined } from '@ant-design/icons';

const CitizenDashboard: React.FC = () => {
  const recentRequests = [
    {
      id: 'REQ-001',
      title: 'Certidão de Residência',
      status: 'Em Análise',
      date: '2023-06-15',
      color: 'blue',
    },
  ];

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Meu Painel</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
              <FileDoneOutlined className="text-xl" />
            </div>
            <div>
              <div className="text-gray-500">Solicitações Ativas</div>
              <div className="text-2xl font-bold">5</div>
            </div>
          </div>
        </Card>
      </div>
      
      <Card 
        title="Solicitações Recentes" 
        extra={
          <Button type="link" size="small">
            Ver Todas
          </Button>
        }
      >
        <List
          itemLayout="horizontal"
          dataSource={recentRequests}
          renderItem={(item) => (
            <List.Item
              actions={[
                <Button type="link" size="small">Detalhes</Button>
              ]}
            >
              <List.Item.Meta
                title={item.title}
                description={
                  <Space>
                    <Tag color={item.color}>{item.status}</Tag>
                    <span>{item.date}</span>
                  </Space>
                }
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default CitizenDashboard;

