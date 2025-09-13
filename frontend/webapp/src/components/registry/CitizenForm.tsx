import React, { useState } from 'react';
import {
  Box,
  Button,
  Grid,
  TextField,
  FormControlLabel,
  Switch,
  Divider,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import ptBR from 'date-fns/locale/pt-BR';

interface Citizen {
  id?: number;
  full_name: string;
  document_id: string;
  birth_date: string;
  address: string;
  district: string;
  postal_code: string;
  phone: string;
  email: string;
  is_active: boolean;
}

interface CitizenFormProps {
  initialData?: Citizen;
  onSubmit: (data: Partial<Citizen>) => void;
  onCancel: () => void;
}

export const CitizenForm: React.FC<CitizenFormProps> = ({ initialData, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<Partial<Citizen>>({
    full_name: initialData?.full_name || '',
    document_id: initialData?.document_id || '',
    birth_date: initialData?.birth_date || '',
    address: initialData?.address || '',
    district: initialData?.district || '',
    postal_code: initialData?.postal_code || '',
    phone: initialData?.phone || '',
    email: initialData?.email || '',
    is_active: initialData?.is_active !== undefined ? initialData.is_active : true,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });

    // Limpar erro do campo quando o usuário digita
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: '',
      });
    }
  };

  const handleDateChange = (date: Date | null) => {
    if (date) {
      setFormData({
        ...formData,
        birth_date: date.toISOString().split('T')[0],
      });

      // Limpar erro do campo quando o usuário seleciona uma data
      if (errors.birth_date) {
        setErrors({
          ...errors,
          birth_date: '',
        });
      }
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.full_name?.trim()) {
      newErrors.full_name = 'Nome completo é obrigatório';
    }

    if (!formData.document_id?.trim()) {
      newErrors.document_id = 'Documento de identificação é obrigatório';
    }

    if (!formData.birth_date) {
      newErrors.birth_date = 'Data de nascimento é obrigatória';
    }

    if (!formData.address?.trim()) {
      newErrors.address = 'Endereço é obrigatório';
    }

    if (!formData.district?.trim()) {
      newErrors.district = 'Bairro é obrigatório';
    }

    if (!formData.postal_code?.trim()) {
      newErrors.postal_code = 'Código postal é obrigatório';
    }

    if (formData.email && !/^\S+@\S+\.\S+$/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            fullWidth
            label="Nome Completo"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            error={!!errors.full_name}
            helperText={errors.full_name}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            fullWidth
            label="Documento de Identificação"
            name="document_id"
            value={formData.document_id}
            onChange={handleChange}
            error={!!errors.document_id}
            helperText={errors.document_id}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
            <DatePicker
              label="Data de Nascimento"
              value={formData.birth_date ? new Date(formData.birth_date) : null}
              onChange={handleDateChange}
              slotProps={{
                textField: {
                  fullWidth: true,
                  required: true,
                  error: !!errors.birth_date,
                  helperText: errors.birth_date,
                },
              }}
            />
          </LocalizationProvider>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="Telefone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            error={!!errors.phone}
            helperText={errors.phone}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            required
            fullWidth
            label="Endereço"
            name="address"
            value={formData.address}
            onChange={handleChange}
            error={!!errors.address}
            helperText={errors.address}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            fullWidth
            label="Bairro"
            name="district"
            value={formData.district}
            onChange={handleChange}
            error={!!errors.district}
            helperText={errors.district}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            fullWidth
            label="Código Postal"
            name="postal_code"
            value={formData.postal_code}
            onChange={handleChange}
            error={!!errors.postal_code}
            helperText={errors.postal_code}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            error={!!errors.email}
            helperText={errors.email}
          />
        </Grid>
        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={formData.is_active}
                onChange={handleChange}
                name="is_active"
                color="primary"
              />
            }
            label="Cidadão Ativo"
          />
        </Grid>
      </Grid>
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button onClick={onCancel} sx={{ mr: 1 }}>
          Cancelar
        </Button>
        <Button type="submit" variant="contained" color="primary">
          {initialData ? 'Atualizar' : 'Cadastrar'}
        </Button>
      </Box>
    </Box>
  );
};
