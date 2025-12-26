import React from 'react';
import { Card } from '@fluentui/react-components';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { BodyBatteryData } from '../services/api';

interface BodyBatteryChartProps {
  data: BodyBatteryData[];
}

export const BodyBatteryChart: React.FC<BodyBatteryChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <Card style={{ padding: '20px', marginBottom: '20px' }}>
        <h3 style={{ margin: '0 0 15px 0', fontSize: '18px' }}>Body Battery</h3>
        <p style={{ color: '#888' }}>No body battery data available</p>
      </Card>
    );
  }

  const chartData = data.map(d => ({
    time: d.time,
    battery: d.battery_level,
  }));

  const avgBattery = (data.reduce((sum, d) => sum + d.battery_level, 0) / data.length).toFixed(1);
  const currentBattery = data[data.length - 1]?.battery_level || 0;
  const peakBattery = Math.max(...data.map(d => d.battery_level));

  // Determine battery color based on level
  const getBatteryColor = (level: number) => {
    if (level >= 75) return '#10b981'; // green
    if (level >= 50) return '#f59e0b'; // orange
    if (level >= 25) return '#ef4444'; // red
    return '#991b1b'; // dark red
  };

  return (
    <Card style={{ padding: '20px', marginBottom: '20px' }}>
      <h3 style={{ margin: '0 0 10px 0', fontSize: '18px' }}>Body Battery</h3>
      <p style={{ margin: '0 0 15px 0', color: '#666', fontSize: '14px' }}>
        Current: <strong style={{ color: getBatteryColor(currentBattery) }}>{currentBattery}</strong> | 
        Average: <strong>{avgBattery}</strong> | 
        Peak: <strong>{peakBattery}</strong> | 
        Samples: <strong>{data.length}</strong>
      </p>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="time" 
            tick={{ fontSize: 12 }}
            interval="preserveStartEnd"
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
          />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="battery" 
            stroke="#10b981" 
            strokeWidth={2}
            dot={false}
            name="Body Battery"
          />
        </LineChart>
      </ResponsiveContainer>
      <div style={{ marginTop: '10px', display: 'flex', gap: '15px', fontSize: '12px', color: '#666' }}>
        <span>■ <span style={{ color: '#10b981' }}>High (75-100)</span></span>
        <span>■ <span style={{ color: '#f59e0b' }}>Medium (50-75)</span></span>
        <span>■ <span style={{ color: '#ef4444' }}>Low (25-50)</span></span>
        <span>■ <span style={{ color: '#991b1b' }}>Very Low (0-25)</span></span>
      </div>
    </Card>
  );
};
