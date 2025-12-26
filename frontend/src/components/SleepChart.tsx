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
      <p style={{ color: '#666', marginBottom: '15px' }}>
        Total: {totalHours} hours | Score: {sleepScore}
      </p>
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
          {data.avg_respiration && <span>Avg Respiration: {data.avg_respiration} brpm</span>}
        </div>
      )}
    </Card>
  );
};
