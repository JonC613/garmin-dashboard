import React from 'react';
import { Card } from '@fluentui/react-components';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { StressData } from '../services/api';

interface StressChartProps {
  data: StressData[];
}

export const StressChart: React.FC<StressChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <Card style={{ padding: '20px', textAlign: 'center' }}>
        <h3>Stress Levels</h3>
        <p style={{ color: '#888' }}>No stress data available</p>
      </Card>
    );
  }

  const avgStress = data.reduce((sum, d) => sum + d.stress_level, 0) / data.length;
  const maxStress = Math.max(...data.map(d => d.stress_level));

  const getStressColor = (level: number) => {
    if (level < 25) return '#27ae60';
    if (level < 50) return '#f39c12';
    if (level < 75) return '#e67e22';
    return '#e74c3c';
  };

  return (
    <Card style={{ padding: '20px' }}>
      <h3 style={{ marginBottom: '10px' }}>Stress Levels Throughout Day</h3>
      <p style={{ color: '#666', marginBottom: '15px' }}>
        Average: {avgStress.toFixed(1)} | Peak: {maxStress}
      </p>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="time" 
            tick={{ fontSize: 12 }}
            interval={Math.floor(data.length / 10)}
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
          />
          <Tooltip />
          {/* Stress level zones */}
          <ReferenceLine y={25} stroke="#27ae60" strokeDasharray="3 3" strokeOpacity={0.3} />
          <ReferenceLine y={50} stroke="#f39c12" strokeDasharray="3 3" strokeOpacity={0.3} />
          <ReferenceLine y={75} stroke="#e74c3c" strokeDasharray="3 3" strokeOpacity={0.3} />
          <Line 
            type="monotone" 
            dataKey="stress_level" 
            stroke="#9b59b6" 
            strokeWidth={2}
            dot={false}
            name="Stress Level"
          />
        </LineChart>
      </ResponsiveContainer>
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '15px', fontSize: '12px' }}>
        <span style={{ color: '#27ae60' }}>■ Low (0-25)</span>
        <span style={{ color: '#f39c12' }}>■ Medium (25-50)</span>
        <span style={{ color: '#e67e22' }}>■ High (50-75)</span>
        <span style={{ color: '#e74c3c' }}>■ Very High (75-100)</span>
      </div>
    </Card>
  );
};
