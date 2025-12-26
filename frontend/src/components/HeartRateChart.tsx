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
import { HeartRateData } from '../services/api';

interface HeartRateChartProps {
  data: HeartRateData[];
}

export const HeartRateChart: React.FC<HeartRateChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <Card style={{ padding: '20px', textAlign: 'center' }}>
        <h3>Heart Rate</h3>
        <p style={{ color: '#888' }}>No heart rate data available</p>
      </Card>
    );
  }

  const avgHr = data.reduce((sum, d) => sum + d.heart_rate_bpm, 0) / data.length;

  return (
    <Card style={{ padding: '20px' }}>
      <h3 style={{ marginBottom: '10px' }}>Heart Rate Throughout Day</h3>
      <p style={{ color: '#666', marginBottom: '15px' }}>
        Average: {avgHr.toFixed(1)} bpm | Samples: {data.length}
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
            domain={['dataMin - 10', 'dataMax + 10']}
            tick={{ fontSize: 12 }}
          />
          <Tooltip />
          <ReferenceLine 
            y={avgHr} 
            stroke="#888" 
            strokeDasharray="3 3"
            label={{ value: `Avg: ${avgHr.toFixed(1)}`, fontSize: 12 }}
          />
          <Line 
            type="monotone" 
            dataKey="heart_rate_bpm" 
            stroke="#e74c3c" 
            strokeWidth={2}
            dot={false}
            name="Heart Rate (bpm)"
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
};
