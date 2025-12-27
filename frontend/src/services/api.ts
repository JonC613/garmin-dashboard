import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface HeartRateData {
  datetime: string;
  time: string;
  heart_rate_bpm: number;
}

export interface StressData {
  datetime: string;
  time: string;
  stress_level: number;
}

export interface SleepData {
  date: string;
  sleep_start: string | null;
  sleep_end: string | null;
  total_sleep_seconds: number;
  deep_sleep_seconds: number;
  light_sleep_seconds: number;
  rem_sleep_seconds: number;
  awake_seconds: number;
  sleep_score: number | null;
  sleep_quality: string | null;
  avg_respiration: number | null;
  avg_spo2: number | null;
  lowest_spo2: number | null;
  restless_moments: number | null;
  body_battery_change: number | null;
  avg_overnight_hrv: number | null;
  hrv_status: string | null;
  resting_heart_rate: number | null;
}

export interface Activity {
  activity_id: number;
  activity_name: string;
  start_time: string;
  duration_seconds: number;
  distance_meters: number | null;
  avg_heart_rate: number | null;
  max_heart_rate: number | null;
  calories: number | null;
}

export interface BodyBatteryData {
  datetime: string;
  time: string;
  battery_level: number;
}

export interface StepsData {
  date: string;
  total_steps: number;
  step_goal: number;
  total_distance_meters: number;
  calories_total: number;
  calories_bmr: number;
  calories_active: number;
  moderate_intensity_minutes: number;
  vigorous_intensity_minutes: number;
}

export interface RestingHeartRateData {
  date: string;
  resting_heart_rate: number | null;
  min_heart_rate: number | null;
  max_heart_rate: number | null;
}

export interface DashboardData {
  date: string;
  heart_rate: HeartRateData[];
  stress: StressData[];
  sleep: SleepData | null;
  activities: Activity[];
  body_battery: BodyBatteryData[];
  steps: StepsData | null;
  resting_heart_rate: RestingHeartRateData | null;
}

export const garminApi = {
  async getHeartRate(date: string) {
    const response = await axios.get(`${API_BASE_URL}/heart-rate/${date}`);
    return response.data;
  },

  async getStress(date: string) {
    const response = await axios.get(`${API_BASE_URL}/stress/${date}`);
    return response.data;
  },

  async getSleep(date: string) {
    const response = await axios.get(`${API_BASE_URL}/sleep/${date}`);
    return response.data;
  },

  async getActivities(date: string) {
    const response = await axios.get(`${API_BASE_URL}/activities/${date}`);
    return response.data;
  },

  async getAllData(date: string): Promise<DashboardData> {
    const response = await axios.get(`${API_BASE_URL}/data/${date}`);
    return response.data.data;
  },

  async getTodayData(): Promise<DashboardData> {
    const response = await axios.get(`${API_BASE_URL}/today`);
    return response.data.data;
  }
};
