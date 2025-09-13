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
  Card,
  CardContent,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Tabs,
  Tab,
} from '@mui/material';
import {
  AttachMoney as MoneyIcon,
  Receipt as ReceiptIcon,
  AccountBalance as BankIcon,
  TrendingUp as TrendingUpIcon,
  Visibility as VisibilityIcon,
  GetApp as DownloadIcon,
} from '@mui/icons-material';
import { api } from '../services/api';
import { PageHeader } from '../components/PageHeader';
import { PaymentChart } from '../components/finance/PaymentChart';
import { RevenueByTypeChart } from '../components/finance/RevenueByTypeChart';
import { PaymentTable } from '../components/finance/PaymentTable';
import { NewPaymentForm } from '../components/finance/NewPaymentForm';

interface PaymentSummary {
  total_payments: number;
  total_amount: number;
  completed_payments: number;
  completed_amount: number;
  pending_payments: number;
  pending_amount: number;
  failed_payments: number;
}

interface RevenueByType {
  payment_type: string;
  amount: number;
  count: number;
}

interface RecentPayment {
  id: number;
  reference_id: string;
  amount: number;
  payment_type: string;
  status: string;
  created_at: string;
  user_name: string;
}

const FinanceDashboard: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<PaymentSummary | null>(null);
  const [revenueByType, setRevenueByType] = useState<RevenueByType[]>([]);
  const [recentPayments, setRecentPayments] = useState<RecentPayment[]>([]);
  const [tabValue, setTabValue] = useState<number>(0);
  const [showNewPaymentForm, setShowNewPaymentForm] = useState<boolean>(false);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Fazer múltiplas requisições em paralelo
      const [summaryRes, revenueRes, paymentsRes] = await Promise.all([
        api.get('/finance/dashboard/summary'),
        api.get('/finance/dashboard/revenue-by-type'),
        api.get('/finance/payments/recent')
      ]);
      
      setSummary(summaryRes.data);
      setRevenueByType(revenueRes.data);
      setRecentPayments(paymentsRes.data);
      setError(null);
    } catch (err) {
      console.error('Erro ao carregar dados do dashboard:', err);
      setError('Não foi possível carregar os dados financeiros. Tente novamente mais tarde.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleNewPaymentSubmit = async (paymentData: any) => {
    try {
      await api.post('/finance/payments', paymentData);
      setShowNewPaymentForm(false);
      fetchDashboardData();
    } catch (err) {
      console.error('Erro ao criar pagamento:', err);
      setError('Erro ao registrar novo pagamento. Tente novamente.');
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-AO', {
      style: 'currency',
      currency: 'AOA'
    }).format(value);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <PageHeader 
        title="Dashboard Financeiro" 
        subtitle="Gestão de receitas e pagamentos municipais"
      />
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {!showNewPaymentForm ? (
        <>
          {/* Cards de resumo */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <MoneyIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h6" component="div">
                    {summary ? formatCurrency(summary.total_amount) : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Receita Total
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <ReceiptIcon color="success" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h6" component="div">
                    {summary ? summary.total_payments : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total de Pagamentos
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <BankIcon color="info" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h6" component="div">
                    {summary ? formatCurrency(summary.completed_amount) : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Pagamentos Concluídos
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <TrendingUpIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h6" component="div">
                    {summary ? formatCurrency(summary.pending_amount) : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Pagamentos Pendentes
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Botão para novo pagamento */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 3 }}>
            <Button 
              variant="contained" 
              startIcon={<MoneyIcon />}
              onClick={() => setShowNewPaymentForm(true)}
            >
              Registrar Novo Pagamento
            </Button>
          </Box>

          {/* Gráficos e tabelas */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom>Evolução de Pagamentos</Typography>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ height: 300 }}>
                  <PaymentChart />
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom>Receita por Tipo</Typography>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ height: 300 }}>
                  <RevenueByTypeChart data={revenueByType} />
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
                  <Tabs value={tabValue} onChange={handleTabChange}>
                    <Tab label="Pagamentos Recentes" />
                    <Tab label="Pagamentos Pendentes" />
                    <Tab label="Relatórios" />
                  </Tabs>
                </Box>
                {tabValue === 0 && (
                  <PaymentTable payments={recentPayments} />
                )}
                {tabValue === 1 && (
                  <Typography variant="body1" sx={{ p: 2 }}>
                    Lista de pagamentos pendentes estará disponível em breve.
                  </Typography>
                )}
                {tabValue === 2 && (
                  <List>
                    <ListItem>
                      <ListItemText 
                        primary="Relatório de Receitas Mensais" 
                        secondary="Resumo de todas as receitas do mês atual"
                      />
                      <ListItemSecondaryAction>
                        <IconButton edge="end">
                          <DownloadIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText 
                        primary="Relatório de Pagamentos por Tipo" 
                        secondary="Análise detalhada por categoria de pagamento"
                      />
                      <ListItemSecondaryAction>
                        <IconButton edge="end">
                          <DownloadIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText 
                        primary="Relatório de Transações Bancárias" 
                        secondary="Histórico de transações com instituições financeiras"
                      />
                      <ListItemSecondaryAction>
                        <IconButton edge="end">
                          <DownloadIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                  </List>
                )}
              </Paper>
            </Grid>
          </Grid>
        </>
      ) : (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Registrar Novo Pagamento</Typography>
          <Divider sx={{ mb: 3 }} />
          <NewPaymentForm 
            onSubmit={handleNewPaymentSubmit} 
            onCancel={() => setShowNewPaymentForm(false)} 
          />
        </Paper>
      )}
    </Container>
  );
};

export default FinanceDashboard;
