import React from 'react';
import { Card } from '@fluentui/react-components';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { SleepData } from '../services/api';

interface SleepChartProps {
  data: SleepData | null;
}

export const SleepChart: React.FC<SleepChartProps> = ({ data }) => {
  if (!data || data.total_sleep_seconds === 0) {
    return (
      <Card style={{ padding: '20px', textAlign: 'center' }}>
        <h3>Sleep Breakdown</h3>
        <p style={{ color: '#888' }}>No sleep data available</p>
      </Card>
    );
  }

  const sleepStages = [
    {
      name: 'Deep',
      minutes: Math.round(data.deep_sleep_seconds / 60),
      color: '#3498db'
    },
    {
      name: 'Light',
      minutes: Math.round(data.light_sleep_seconds / 60),
      color: '#5dade2'
    },
    {
      name: 'REM',
      minutes: Math.round(data.rem_sleep_seconds / 60),
      color: '#9b59b6'
    },
    {
      name: 'Awake',
      minutes: Math.round(data.awake_seconds / 60),
      color: '#e74c3c'
    }
  ];

  const totalHours = (data.total_sleep_seconds / 3600).toFixed(1);
  const sleepScore = data.sleep_score || 'N/A';

  return (
    <Card style={{ padding: '20px' }}>
      <h3 style={{ marginBottom: '10px' }}>Sleep Breakdown</h3>
      
      {/* Summary metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '12px', marginBottom: '15px' }}>
        <div style={{ fontSize: '13px' }}>
          <div style={{ color: '#888', marginBottom: '3px' }}>Total Sleep</div>
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0078d4' }}>{totalHours} hrs</div>
        </div>
        
        <div style={{ fontSize: '13px' }}>
          <div style={{ color: '#888', marginBottom: '3px' }}>Sleep Score</div>
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#10b981' }}>{sleepScore}</div>
        </div>
        
        {data.sleep_quality && (
          <div style={{ fontSize: '13px' }}>
            <div style={{ color: '#888', marginBottom: '3px' }}>Quality</div>
            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#8b5cf6' }}>{data.sleep_quality}</div>
          </div>
        )}
        
        {data.restless_moments !== null && data.restless_moments !== undefined && (
          <div style={{ fontSize: '13px' }}>
            <div style={{ color: '#888', marginBottom: '3px' }}>Restless Moments</div>
            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#f59e0b' }}>{data.restless_moments}</div>
          </div>
        )}
        
        {data.body_battery_change !== null && data.body_battery_change !== undefined && (
          <div style={{ fontSize: '13px' }}>
            <div style={{ color: '#888', marginBottom: '3px' }}>Body Battery</div>
            <div style={{ fontSize: '16px', fontWeight: 'bold', color: data.body_battery_change >= 0 ? '#10b981' : '#ef4444' }}>
              {data.body_battery_change >= 0 ? '+' : ''}{data.body_battery_change}
            </div>
          </div>
        )}
        
        {data.avg_overnight_hrv !== null && data.avg_overnight_hrv !== undefined && (
          <div style={{ fontSize: '13px' }}>
            <div style={{ color: '#888', marginBottom: '3px' }}>Overnight HRV</div>
            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#06b6d4' }}>{data.avg_overnight_hrv.toFixed(1)} ms</div>
          </div>
        )}
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={sleepStages}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} label={{ value: 'Minutes', angle: -90, position: 'insideLeft' }} />
          <Tooltip formatter={(value) => `${value} min`} />
          <Bar dataKey="minutes" radius={[8, 8, 0, 0]}>
            {sleepStages.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      {data.avg_spo2 && (
        <div style={{ marginTop: '15px', fontSize: '14px', color: '#666' }}>
          <span style={{ marginRight: '20px' }}>Avg SpO2: {data.avg_spo2}%</span>
          {data.lowest_spo2 && <span style={{ marginRight: '20px' }}>Lowest: {data.lowest_spo2}%</span>}
          {data.avg_respiration && <span>Avg Respiration: {data.avg_respiration} brpm</span>}
        </div>
      )}
    </Card>
  );
};
