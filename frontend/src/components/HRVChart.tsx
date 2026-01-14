import React from 'react';
import { Card } from '@fluentui/react-components';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { HRVData } from '../services/api';

interface HRVChartProps {
  data: HRVData[];
}

export const HRVChart: React.FC<HRVChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <Card style={{ padding: '20px' }}>
        <h3>HRV (Heart Rate Variability)</h3>
        <p style={{ color: '#666', marginTop: '10px' }}>No HRV data available for this date.</p>
      </Card>
    );
  }

  // Calculate statistics
  const values = data.map(d => d.hrv_value);
  const avgHRV = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1);
  const minHRV = Math.min(...values).toFixed(1);
  const maxHRV = Math.max(...values).toFixed(1);

  // If only one data point (typical for nightly HRV), show as a simple stat card
  if (data.length === 1) {
    return (
      <Card style={{ padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h3 style={{ margin: 0 }}>HRV (Heart Rate Variability)</h3>
          <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '12px', color: '#666' }}>Nightly Average: </span>
              <span style={{ fontSize: '24px', fontWeight: '600', color: '#6366f1' }}>{avgHRV} ms</span>
            </div>
          </div>
        </div>
        
        <div style={{ padding: '20px', backgroundColor: '#f9fafb', borderRadius: '8px', textAlign: 'center' }}>
          <div style={{ fontSize: '48px', fontWeight: '600', color: '#6366f1', marginBottom: '10px' }}>
            {avgHRV} ms
          </div>
          <div style={{ fontSize: '14px', color: '#666' }}>
            Measured during sleep
          </div>
        </div>
        
        <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '4px' }}>
          <p style={{ fontSize: '13px', color: '#666', margin: 0 }}>
            <strong>About HRV:</strong> Heart Rate Variability measures the variation in time between heartbeats. 
            Higher HRV generally indicates better cardiovascular fitness and recovery. 
            Lower HRV may indicate stress, fatigue, or overtraining. Garmin typically measures HRV during sleep.
          </p>
        </div>
      </Card>
    );
  }

  // Multiple data points - show as a chart
  const chartData = data.map(item => ({
    time: item.time.substring(0, 5), // HH:MM
    hrv: item.hrv_value
  }));

  return (
    <Card style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h3 style={{ margin: 0 }}>HRV (Heart Rate Variability)</h3>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div>
            <span style={{ fontSize: '12px', color: '#666' }}>Average: </span>
            <span style={{ fontSize: '16px', fontWeight: '600', color: '#6366f1' }}>{avgHRV} ms</span>
          </div>
          <div>
            <span style={{ fontSize: '12px', color: '#666' }}>Range: </span>
            <span style={{ fontSize: '14px', color: '#666' }}>{minHRV} - {maxHRV} ms</span>
          </div>
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="time" 
            stroke="#666"
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            stroke="#666"
            tick={{ fontSize: 12 }}
            label={{ value: 'HRV (ms)', angle: -90, position: 'insideLeft', style: { fontSize: 12 } }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'white', 
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '12px'
            }}
            formatter={(value: number) => [`${value} ms`, 'HRV']}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="hrv" 
            stroke="#6366f1" 
            strokeWidth={2}
            dot={false}
            name="HRV"
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '4px' }}>
        <p style={{ fontSize: '13px', color: '#666', margin: 0 }}>
          <strong>About HRV:</strong> Heart Rate Variability measures the variation in time between heartbeats. 
          Higher HRV generally indicates better cardiovascular fitness and recovery. 
          Lower HRV may indicate stress, fatigue, or overtraining.
        </p>
      </div>
    </Card>
  );
};
