import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { Table } from '../../../components/ui/Table';
import { CitizenRequestForm } from '../components/CitizenRequestForm';
import { citizenshipApi } from '../api/citizenshipApi';
import { toast } from 'react-hot-toast';

export const CitizenRequestsPage: React.FC = () => {
  const [requests, setRequests] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingRequest, setEditingRequest] = useState<any>(null);
  const navigate = useNavigate();

  const loadRequests = async () => {
    try {
      setIsLoading(true);
      const data = await citizenshipApi.getCitizenRequests();
      setRequests(data.results || []);
    } catch (error) {
      console.error('Error loading requests:', error);
      toast.error('Erro ao carregar pedidos');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadRequests();
  }, []);

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingRequest(null);
    loadRequests();
  };

  const handleEdit = (request: any) => {
    setEditingRequest(request);
    setShowForm(true);
  };

  const handleViewDetails = (requestId: string) => {
    navigate(`/cidadania/pedidos/${requestId}`);
  };

  const handleDelete = async (requestId: string) => {
    if (window.confirm('Tem certeza que deseja excluir este pedido?')) {
      try {
        await citizenshipApi.deleteCitizenRequest(requestId);
        toast.success('Pedido excluído com sucesso');
        loadRequests();
      } catch (error) {
        console.error('Error deleting request:', error);
        toast.error('Erro ao excluir pedido');
      }
    }
  };

  const columns = [
    {
      key: 'id',
      header: 'Número',
      render: (row: any) => `#${row.id.slice(0, 8)}`,
    },
    {
      key: 'name',
      header: 'Nome',
    },
    {
      key: 'nif',
      header: 'NIF',
    },
    {
      key: 'status',
      header: 'Status',
      render: (row: any) => {
        const statusMap: Record<string, string> = {
          draft: 'Rascunho',
          submitted: 'Submetido',
          in_review: 'Em Análise',
          approved: 'Aprovado',
          rejected: 'Rejeitado',
        };
        return statusMap[row.status] || row.status;
      },
    },
    {
      key: 'createdAt',
      header: 'Data de Criação',
      render: (row: any) => new Date(row.createdAt).toLocaleDateString(),
    },
    {
      key: 'actions',
      header: 'Ações',
      render: (row: any) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleViewDetails(row.id)}
          >
            Ver
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleEdit(row)}
          >
            Editar
          </Button>
          <Button
            size="sm"
            variant="destructive"
            onClick={() => handleDelete(row.id)}
          >
            Excluir
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Pedidos de Cidadania</h1>
        <Button onClick={() => setShowForm(true)}>+ Novo Pedido</Button>
      </div>

      {showForm && (
        <Card className="p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">
            {editingRequest ? 'Editar Pedido' : 'Novo Pedido'}
          </h2>
          <CitizenRequestForm
            initialData={editingRequest || {}}
            onSuccess={handleFormSuccess}
            onCancel={() => {
              setShowForm(false);
              setEditingRequest(null);
            }}
          />
        </Card>
      )}

      <Card>
        <Table
          columns={columns}
          data={requests}
          isLoading={isLoading}
          emptyState={
            <div className="text-center py-8">
              <p className="text-gray-500">Nenhum pedido encontrado</p>
              <Button 
                className="mt-4" 
                onClick={() => setShowForm(true)}
              >
                Criar Primeiro Pedido
              </Button>
            </div>
          }
        />
      </Card>
    </div>
  );
};

export default CitizenRequestsPage;

