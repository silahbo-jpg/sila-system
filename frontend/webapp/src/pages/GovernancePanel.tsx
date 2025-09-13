import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Divider,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  IconButton,
  TextField,
  InputAdornment,
} from '@mui/material';
import {
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  GetApp as DownloadIcon,
  Security as SecurityIcon,
  History as HistoryIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { api } from '../services/api';
import { PageHeader } from '../components/PageHeader';
import { AuditLogDetails } from '../components/governance/AuditLogDetails';

interface AuditLog {
  id: number;
  timestamp: string;
  user_id: number;
  user_name: string;
  action: string;
  resource_type: string;
  resource_id: string;
  ip_address: string;
  user_agent: string;
}

const GovernancePanel: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState<number>(0);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [page, setPage] = useState<number>(0);
  const [rowsPerPage, setRowsPerPage] = useState<number>(10);
  const [totalLogs, setTotalLogs] = useState<number>(0);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);
  const [showLogDetails, setShowLogDetails] = useState<boolean>(false);

  const fetchAuditLogs = async (pageNum = page, rowsNum = rowsPerPage, search = searchTerm) => {
    setLoading(true);
    try {
      const response = await api.get('/governance/audit-logs', {
        params: {
          page: pageNum,
          limit: rowsNum,
          search: search || undefined,
        },
      });
      setAuditLogs(response.data.items);
      setTotalLogs(response.data.total);
      setError(null);
    } catch (err) {
      console.error('Erro ao carregar logs de auditoria:', err);
      setError('Não foi possível carregar os logs de auditoria. Tente novamente mais tarde.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAuditLogs();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
    fetchAuditLogs(newPage, rowsPerPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newRowsPerPage = parseInt(event.target.value, 10);
    setRowsPerPage(newRowsPerPage);
    setPage(0);
    fetchAuditLogs(0, newRowsPerPage);
  };

  const handleSearch = () => {
    setPage(0);
    fetchAuditLogs(0, rowsPerPage, searchTerm);
  };

  const handleViewLogDetails = (log: AuditLog) => {
    setSelectedLog(log);
    setShowLogDetails(true);
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'CREATE':
        return 'success';
      case 'UPDATE':
        return 'info';
      case 'DELETE':
        return 'error';
      case 'LOGIN':
        return 'primary';
      case 'LOGOUT':
        return 'secondary';
      default:
        return 'default';
    }
  };

  const formatDateTime = (dateTimeStr: string) => {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('pt-AO', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <PageHeader 
        title="Painel de Governança" 
        subtitle="Monitoramento, auditoria e compliance institucional"
      />
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {!showLogDetails ? (
        <>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab icon={<HistoryIcon />} label="Logs de Auditoria" />
                <Tab icon={<SecurityIcon />} label="Permissões" />
                <Tab icon={<AssessmentIcon />} label="Relatórios" />
              </Tabs>
            </Box>
          </Paper>

          {tabValue === 0 && (
            <>
              <Paper sx={{ p: 2, mb: 3 }}>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12} sm={8} md={6}>
                    <TextField
                      fullWidth
                      label="Buscar logs (usuário, ação, recurso)"
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
                  <Grid item xs={12} sm={4} md={6} sx={{ display: 'flex', justifyContent: { xs: 'flex-start', sm: 'flex-end' } }}>
                    <Button
                      variant="outlined"
                      startIcon={<DownloadIcon />}
                    >
                      Exportar Logs
                    </Button>
                  </Grid>
                </Grid>
              </Paper>

              <Paper>
                {loading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <>
                    <TableContainer>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Data/Hora</TableCell>
                            <TableCell>Usuário</TableCell>
                            <TableCell>Ação</TableCell>
                            <TableCell>Recurso</TableCell>
                            <TableCell>ID Recurso</TableCell>
                            <TableCell>Ações</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {auditLogs.map((log) => (
                            <TableRow key={log.id}>
                              <TableCell>{log.id}</TableCell>
                              <TableCell>{formatDateTime(log.timestamp)}</TableCell>
                              <TableCell>{log.user_name}</TableCell>
                              <TableCell>
                                <Chip 
                                  label={log.action} 
                                  color={getActionColor(log.action) as any}
                                  size="small"
                                />
                              </TableCell>
                              <TableCell>{log.resource_type}</TableCell>
                              <TableCell>{log.resource_id}</TableCell>
                              <TableCell>
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleViewLogDetails(log)}
                                  title="Ver detalhes"
                                >
                                  <VisibilityIcon />
                                </IconButton>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                    <TablePagination
                      rowsPerPageOptions={[5, 10, 25]}
                      component="div"
                      count={totalLogs}
                      rowsPerPage={rowsPerPage}
                      page={page}
                      onPageChange={handleChangePage}
                      onRowsPerPageChange={handleChangeRowsPerPage}
                      labelRowsPerPage="Linhas por página:"
                    />
                  </>
                )}
              </Paper>
            </>
          )}

          {tabValue === 1 && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Gestão de Permissões</Typography>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body1">
                O módulo de gestão de permissões estará disponível em breve. Aqui será possível configurar
                perfis de acesso, atribuir permissões a usuários e definir políticas de segurança para
                o sistema SILA.
              </Typography>
            </Paper>
          )}

          {tabValue === 2 && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Relatórios de Governança</Typography>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body1" paragraph>
                O módulo de relatórios de governança estará disponível em breve. Aqui será possível gerar
                relatórios detalhados sobre atividades do sistema, conformidade com políticas e métricas
                de segurança.
              </Typography>
              <Grid container spacing={2} sx={{ mt: 2 }}>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper elevation={2} sx={{ p: 2, textAlign: 'center', opacity: 0.7 }}>
                    <Typography variant="subtitle1">Relatório de Atividades de Usuários</Typography>
                    <Box sx={{ mt: 1 }}>
                      <Button variant="outlined" disabled startIcon={<DownloadIcon />}>
                        Em breve
                      </Button>
                    </Box>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper elevation={2} sx={{ p: 2, textAlign: 'center', opacity: 0.7 }}>
                    <Typography variant="subtitle1">Relatório de Segurança</Typography>
                    <Box sx={{ mt: 1 }}>
                      <Button variant="outlined" disabled startIcon={<DownloadIcon />}>
                        Em breve
                      </Button>
                    </Box>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper elevation={2} sx={{ p: 2, textAlign: 'center', opacity: 0.7 }}>
                    <Typography variant="subtitle1">Relatório de Compliance</Typography>
                    <Box sx={{ mt: 1 }}>
                      <Button variant="outlined" disabled startIcon={<DownloadIcon />}>
                        Em breve
                      </Button>
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </Paper>
          )}
        </>
      ) : (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Detalhes do Log de Auditoria</Typography>
            <Button onClick={() => setShowLogDetails(false)}>Voltar</Button>
          </Box>
          <Divider sx={{ mb: 3 }} />
          {selectedLog && <AuditLogDetails log={selectedLog} />}
        </Paper>
      )}
    </Container>
  );
};

export default GovernancePanel;
