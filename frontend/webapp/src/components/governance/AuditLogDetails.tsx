import React from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Divider,
  Chip,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';

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
  details?: any;
}

interface AuditLogDetailsProps {
  log: AuditLog;
}

export const AuditLogDetails: React.FC<AuditLogDetailsProps> = ({ log }) => {
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

  const getActionDescription = (action: string) => {
    switch (action) {
      case 'CREATE':
        return 'Criação de recurso';
      case 'UPDATE':
        return 'Atualização de recurso';
      case 'DELETE':
        return 'Exclusão de recurso';
      case 'LOGIN':
        return 'Login no sistema';
      case 'LOGOUT':
        return 'Logout do sistema';
      case 'PROCESS_PAYMENT':
        return 'Processamento de pagamento';
      default:
        return action;
    }
  };

  const parseUserAgent = (userAgent: string) => {
    let browser = 'Desconhecido';
    let os = 'Desconhecido';

    if (userAgent.includes('Firefox')) {
      browser = 'Mozilla Firefox';
    } else if (userAgent.includes('Chrome')) {
      browser = 'Google Chrome';
    } else if (userAgent.includes('Safari')) {
      browser = 'Safari';
    } else if (userAgent.includes('Edge')) {
      browser = 'Microsoft Edge';
    } else if (userAgent.includes('MSIE') || userAgent.includes('Trident')) {
      browser = 'Internet Explorer';
    }

    if (userAgent.includes('Windows')) {
      os = 'Windows';
    } else if (userAgent.includes('Mac OS')) {
      os = 'macOS';
    } else if (userAgent.includes('Linux')) {
      os = 'Linux';
    } else if (userAgent.includes('Android')) {
      os = 'Android';
    } else if (userAgent.includes('iOS')) {
      os = 'iOS';
    }

    return { browser, os };
  };

  const { browser, os } = log.user_agent ? parseUserAgent(log.user_agent) : { browser: 'Desconhecido', os: 'Desconhecido' };

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Informações Básicas</Typography>
              <Divider sx={{ mb: 2 }} />
              <List dense>
                <ListItem>
                  <ListItemText 
                    primary="ID do Log" 
                    secondary={log.id} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Data e Hora" 
                    secondary={formatDateTime(log.timestamp)} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Ação" 
                    secondary={
                      <Chip 
                        label={getActionDescription(log.action)} 
                        color={getActionColor(log.action) as any}
                        size="small"
                        sx={{ mt: 0.5 }}
                      />
                    } 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Tipo de Recurso" 
                    secondary={log.resource_type} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="ID do Recurso" 
                    secondary={log.resource_id} 
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Informações do Usuário</Typography>
              <Divider sx={{ mb: 2 }} />
              <List dense>
                <ListItem>
                  <ListItemText 
                    primary="ID do Usuário" 
                    secondary={log.user_id} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Nome do Usuário" 
                    secondary={log.user_name} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Endereço IP" 
                    secondary={log.ip_address} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Navegador" 
                    secondary={browser} 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Sistema Operacional" 
                    secondary={os} 
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {log.details && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Detalhes da Operação</Typography>
                <Divider sx={{ mb: 2 }} />
                <Paper 
                  elevation={0} 
                  sx={{ 
                    p: 2, 
                    backgroundColor: '#f5f5f5', 
                    maxHeight: '300px', 
                    overflow: 'auto',
                    fontFamily: 'monospace'
                  }}
                >
                  <pre>{JSON.stringify(log.details, null, 2)}</pre>
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};
