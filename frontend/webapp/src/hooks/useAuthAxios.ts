import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import SessionExpired from '../components/SessionExpired';

const useAuthAxios = () => {
  const instance = axios.create();

  // Garante que o token mais atual do localStorage seja usado a cada requisição
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  });

  // Intercepta respostas 401 para forçar logout e redirecionar
  instance.interceptors.response.use(
    response => response,
    error => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        // Renderiza feedback visual antes do redirecionamento
        const root = document.getElementById('root');
        if (root) {
          ReactDOM.render(<SessionExpired />, root);
        }
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

export default useAuthAxios;

