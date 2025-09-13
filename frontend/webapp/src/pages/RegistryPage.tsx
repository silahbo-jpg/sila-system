import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Divider,
  Grid,
  Paper,
  Typography,
  TextField,
  CircularProgress,
  Alert,
  Snackbar,
  Card,
  CardContent,
  CardActions,
  IconButton,
  InputAdornment,
} from '@mui/material';
import {
  Search as SearchIcon,
  PersonAdd as PersonAddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { api } from '../services/api';
import { PageHeader } from '../components/PageHeader';
import { CitizenForm } from '../components/registry/CitizenForm';

interface Citizen {
  id: number;
  full_name: string;
  document_id: string;
  birth_date: string;
  address: string;
  district: string;
  postal_code: string;
  phone: string;
  email: string;
  is_active: boolean;
  age: number;
}

const RegistryPage: React.FC = () => {
  const navigate = useNavigate();
  const [citizens, setCitizens] = useState<Citizen[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [showForm, setShowForm] = useState<boolean>(false);
  const [selectedCitizen, setSelectedCitizen] = useState<Citizen | null>(null);
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error'}>({ 
    open: false, 
    message: '', 
    severity: 'success' 
  });

  const fetchCitizens = async () => {
    setLoading(true);
    try {
      const response = await api.get('/registry/citizens');
      setCitizens(response.data);
      setError(null);
    } catch (err) {
      console.error('Erro ao buscar cidadãos:', err);
      setError('Não foi possível carregar os dados dos cidadãos. Tente novamente mais tarde.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCitizens();
  }, []);

  const handleSearch = () => {
    if (!searchTerm.trim()) {
      fetchCitizens();
      return;
    }
    
    setLoading(true);
    api.get(`/registry/citizens/search?term=${searchTerm}`)
      .then(response => {
        setCitizens(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro na busca:', err);
        setError('Erro ao realizar a busca. Tente novamente.');
        setLoading(false);
      });
  };

  const handleAddCitizen = () => {
    setSelectedCitizen(null);
    setShowForm(true);
  };

  const handleEditCitizen = (citizen: Citizen) => {
    setSelectedCitizen(citizen);
    setShowForm(true);
  };

  const handleDeleteCitizen = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir este cidadão?')) {
      try {
        await api.delete(`/registry/citizens/${id}`);
        fetchCitizens();
        setSnackbar({
          open: true,
          message: 'Cidadão excluído com sucesso!',
          severity: 'success'
        });
      } catch (err) {
        console.error('Erro ao excluir cidadão:', err);
        setSnackbar({
          open: true,
          message: 'Erro ao excluir cidadão. Tente novamente.',
          severity: 'error'
        });
      }
    }
  };

  const handleFormSubmit = async (citizenData: Partial<Citizen>) => {
    try {
      if (selectedCitizen) {
        // Edição
        await api.put(`/registry/citizens/${selectedCitizen.id}`, citizenData);
        setSnackbar({
          open: true,
          message: 'Cidadão atualizado com sucesso!',
          severity: 'success'
        });
      } else {
        // Criação
        await api.post('/registry/citizens', citizenData);
        setSnackbar({
          open: true,
          message: 'Cidadão cadastrado com sucesso!',
          severity: 'success'
        });
      }
      setShowForm(false);
      fetchCitizens();
    } catch (err) {
      console.error('Erro ao salvar cidadão:', err);
      setSnackbar({
        open: true,
        message: 'Erro ao salvar dados do cidadão. Verifique os campos e tente novamente.',
        severity: 'error'
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'full_name', headerName: 'Nome Completo', width: 250 },
    { field: 'document_id', headerName: 'Documento', width: 150 },
    { field: 'age', headerName: 'Idade', type: 'number', width: 90 },
    { field: 'district', headerName: 'Bairro', width: 150 },
    { field: 'phone', headerName: 'Telefone', width: 150 },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 150,
      renderCell: (params) => (
        <Box>
          <IconButton 
            color="primary" 
            onClick={() => handleEditCitizen(params.row as Citizen)}
            size="small"
          >
            <EditIcon />
          </IconButton>
          <IconButton 
            color="error" 
            onClick={() => handleDeleteCitizen(params.row.id)}
            size="small"
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <PageHeader 
        title="Cadastro Único de Munícipes" 
        subtitle="Gestão centralizada de informações dos cidadãos"
      />
      
      {showForm ? (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            {selectedCitizen ? 'Editar Cidadão' : 'Novo Cidadão'}
          </Typography>
          <CitizenForm 
            initialData={selectedCitizen || undefined}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
          />
        </Paper>
      ) : (
        <>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={6} md={8}>
                <TextField
                  fullWidth
                  label="Buscar cidadão (nome, documento ou endereço)"
                  variant="outlined"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={handleSearch}>
                          <SearchIcon />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4} sx={{ display: 'flex', justifyContent: { xs: 'flex-start', sm: 'flex-end' } }}>
                <Button
                  variant="contained"
                  startIcon={<PersonAddIcon />}
                  onClick={handleAddCitizen}
                  sx={{ mr: 1 }}
                >
                  Novo Cidadão
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={fetchCitizens}
                >
                  Atualizar
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Paper sx={{ height: 400, width: '100%' }}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <CircularProgress />
              </Box>
            ) : (
              <DataGrid
                rows={citizens}
                columns={columns}
                pageSize={5}
                rowsPerPageOptions={[5, 10, 25]}
                checkboxSelection
                disableSelectionOnClick
              />
            )}
          </Paper>
        </>
      )}

      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={6000} 
        onClose={handleCloseSnackbar}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default RegistryPage;
