import { api } from '../../../api/axios';

interface CitizenRequest {
  id?: string;
  name: string;
  nif: string;
  birthDate: string;
  // Add other fields as per your backend model
}

export const citizenshipApi = {
  // Create a new citizen request
  async createCitizenRequest(data: Omit<CitizenRequest, 'id'>) {
    const response = await api.post('/api/v1/citizenship/requests/', data);
    return response.data;
  },

  // Get all citizen requests with pagination
  async getCitizenRequests(params?: { page?: number; pageSize?: number }) {
    const response = await api.get('/api/v1/citizenship/requests/', { params });
    return response.data;
  },

  // Get a single citizen request by ID
  async getCitizenRequestById(id: string) {
    const response = await api.get(`/api/v1/citizenship/requests/${id}/`);
    return response.data;
  },

  // Update a citizen request
  async updateCitizenRequest(id: string, data: Partial<CitizenRequest>) {
    const response = await api.patch(`/api/v1/citizenship/requests/${id}/`, data);
    return response.data;
  },

  // Submit a citizen request for review
  async submitCitizenRequest(id: string) {
    const response = await api.post(`/api/v1/citizenship/requests/${id}/submit/`);
    return response.data;
  },

  // Approve a citizen request
  async approveRequest(id: string, comment?: string) {
    const response = await api.post(`/api/v1/citizenship/requests/${id}/approve/`, { comment });
    return response.data;
  },

  // Reject a citizen request
  async rejectRequest(id: string, reason: string) {
    const response = await api.post(`/api/v1/citizenship/requests/${id}/reject/`, { reason });
    return response.data;
  },

  // Request more information for a citizen request
  async requestMoreInfo(id: string, message: string) {
    const response = await api.post(`/api/v1/citizenship/requests/${id}/request-info/`, { message });
    return response.data;
  },

  // Upload document for a citizen request
  async uploadDocument(requestId: string, file: File, documentType: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    
    const response = await api.post(
      `/api/v1/citizenship/requests/${requestId}/documents/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },
};

