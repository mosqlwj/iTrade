export interface User {
  id: number;
  username: string;
  email?: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Indicator {
  id: number;
  code: string;
  name: string;
  category: string;
  unit?: string;
  description?: string;
  update_frequency?: string;
  data_source: string;
  is_active: boolean;
}

export interface IndicatorDataPoint {
  date: string;
  value: number;
}

export interface IndicatorData {
  indicator_code: string;
  indicator_name: string;
  unit?: string;
  data: IndicatorDataPoint[];
  latest_value?: number;
  change_percent?: number;
}

export interface IndicatorSummary {
  code: string;
  name: string;
  value?: number;
  change?: number;
  trend: string;
  unit?: string;
}

export interface TrendAnalysis {
  indicator_code: string;
  trend: string;
  change_percent: number;
  ma_7?: number;
  ma_30?: number;
  prediction?: {
    predicted?: number;
    trend: string;
    confidence: string;
  };
}

export interface Alert {
  id: number;
  user_id: number;
  indicator_code: string;
  condition: string;
  threshold: number;
  is_active: boolean;
  last_triggered?: string;
  created_at: string;
}

export interface CreateAlertRequest {
  indicator_code: string;
  condition: string;
  threshold: number;
}
