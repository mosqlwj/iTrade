import axios from 'axios';
import type { 
  LoginRequest, 
  LoginResponse, 
  Indicator, 
  IndicatorData, 
  IndicatorSummary,
  TrendAnalysis,
  Alert,
  CreateAlertRequest
} from '../types';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (data: LoginRequest) => 
    api.post<LoginResponse>('/api/auth/login', data),
  register: (data: { username: string; password: string; email?: string }) =>
    api.post('/api/auth/register', data),
};

export const indicatorApi = {
  getIndicators: () => 
    api.get<{ total: number; items: Indicator[] }>('/api/indicators'),
  
  getIndicatorData: (code: string, forceUpdate = false) => 
    api.get<IndicatorData>(`/api/indicators/${code}/data`, { params: { force_update: forceUpdate } }),
  
  compareIndicators: (codes: string[], startDate?: string, endDate?: string) =>
    api.post('/api/indicators/compare', { codes, start_date: startDate, end_date: endDate }),
  
  getTrend: (code: string) => 
    api.get<TrendAnalysis>(`/api/indicators/${code}/trend`),
  
  getDashboardSummary: () => 
    api.get<IndicatorSummary[]>('/api/dashboard/summary'),
};

export const alertApi = {
  createAlert: (data: CreateAlertRequest) =>
    api.post<Alert>('/api/alerts', data),
  
  getAlerts: (skip = 0, limit = 100) =>
    api.get<{ total: number; items: Alert[] }>('/api/alerts', { params: { skip, limit } }),
  
  checkAlerts: () =>
    api.get('/api/alerts/check'),
  
  updateAlert: (id: number, data: Partial<CreateAlertRequest & { is_active: boolean }>) =>
    api.put<Alert>(`/api/alerts/${id}`, data),
  
  deleteAlert: (id: number) =>
    api.delete(`/api/alerts/${id}`),
};

export default api;
