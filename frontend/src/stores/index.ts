import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authApi, indicatorApi, alertApi } from '../api';
import type { User, IndicatorSummary, IndicatorData, TrendAnalysis, Alert } from '../types';

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const userInfo = ref<User | null>(null);
  const isLoggedIn = computed(() => !!token.value);

  const login = async (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const res = await authApi.login(formData);
    token.value = res.data.access_token;
    localStorage.setItem('token', res.data.access_token);
  };

  const register = async (username: string, password: string, email?: string) => {
    const data: { username: string; password: string; email?: string } = { username, password };
    if (email) {
      data.email = email;
    }
    await authApi.register(data);
  };

  const logout = () => {
    token.value = null;
    userInfo.value = null;
    localStorage.removeItem('token');
  };

  return { token, userInfo, isLoggedIn, login, register, logout };
});

export const useIndicatorStore = defineStore('indicator', () => {
  const summary = ref<IndicatorSummary[]>([]);
  const currentData = ref<IndicatorData | null>(null);
  const trend = ref<TrendAnalysis | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchSummary = async () => {
    loading.value = true;
    try {
      const res = await indicatorApi.getDashboardSummary();
      summary.value = res.data;
    } catch (e: any) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  };

  const fetchIndicatorData = async (code: string, forceUpdate = false) => {
    loading.value = true;
    try {
      const res = await indicatorApi.getIndicatorData(code, forceUpdate);
      currentData.value = res.data;
      return res.data;
    } catch (e: any) {
      error.value = e.message;
      throw e;
    } finally {
      loading.value = false;
    }
  };

  const fetchTrend = async (code: string) => {
    try {
      const res = await indicatorApi.getTrend(code);
      trend.value = res.data;
      return res.data;
    } catch (e: any) {
      error.value = e.message;
      throw e;
    }
  };

  return { summary, currentData, trend, loading, error, fetchSummary, fetchIndicatorData, fetchTrend };
});

export const useAlertStore = defineStore('alert', () => {
  const alerts = ref<Alert[]>([]);
  const loading = ref(false);

  const fetchAlerts = async () => {
    loading.value = true;
    try {
      const res = await alertApi.getAlerts();
      alerts.value = res.data.items;
    } finally {
      loading.value = false;
    }
  };

  const createAlert = async (data: { indicator_code: string; condition: string; threshold: number }) => {
    const res = await alertApi.createAlert(data);
    alerts.value.push(res.data);
    return res.data;
  };

  const deleteAlert = async (id: number) => {
    await alertApi.deleteAlert(id);
    alerts.value = alerts.value.filter(a => a.id !== id);
  };

  const checkAlerts = async () => {
    return await alertApi.checkAlerts();
  };

  return { alerts, loading, fetchAlerts, createAlert, deleteAlert, checkAlerts };
});
