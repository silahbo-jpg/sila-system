import { useQuery, useMutation } from '@tanstack/react-query';
import { createSaude, getSaude, listSaude } from './api';

export const useSaude = (id: number) =>
  useQuery(['saude', id], () => getSaude(id));

export const useCreateSaude = () =>
  useMutation(createSaude);

export const useListSaude = () =>
  useQuery(['saudeList'], listSaude); 
