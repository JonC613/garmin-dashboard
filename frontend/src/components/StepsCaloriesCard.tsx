import React from 'react';
import { Card } from '@fluentui/react-components';
import { StepsData } from '../services/api';

interface StepsCaloriesCardProps {
  data: StepsData | null;
}

export const StepsCaloriesCard: React.FC<StepsCaloriesCardProps> = ({ data }) => {
  if (!data) {
    return (
      <Card style={{ padding: '20px', marginBottom: '20px' }}>
        <h3 style={{ margin: '0 0 15px 0', fontSize: '18px' }}>Steps & Activity</h3>
        <p style={{ color: '#888' }}>No activity data available</p>
      </Card>
    );
  }

  const stepProgress = data.step_goal > 0 ? (data.total_steps / data.step_goal) * 100 : 0;
  const distanceMiles = (data.total_distance_meters * 0.000621371).toFixed(2);
  const totalIntensityMinutes = data.moderate_intensity_minutes + data.vigorous_intensity_minutes;

  return (
    <Card style={{ padding: '20px', marginBottom: '20px' }}>
      <h3 style={{ margin: '0 0 20px 0', fontSize: '18px' }}>Steps & Activity Summary</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
        {/* Steps */}
        <div>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Steps</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#0078d4' }}>
            {data.total_steps.toLocaleString()}
          </div>
          <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
            Goal: {data.step_goal.toLocaleString()} ({stepProgress.toFixed(0)}%)
          </div>
          <div style={{ 
            marginTop: '8px', 
            height: '6px', 
            backgroundColor: '#e0e0e0', 
            borderRadius: '3px',
            overflow: 'hidden'
          }}>
            <div style={{ 
              height: '100%', 
              width: `${Math.min(stepProgress, 100)}%`, 
              backgroundColor: stepProgress >= 100 ? '#10b981' : '#0078d4',
              transition: 'width 0.3s ease'
            }} />
          </div>
        </div>

        {/* Distance */}
        <div>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Distance</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#10b981' }}>
            {distanceMiles}
          </div>
          <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
            miles
          </div>
        </div>

        {/* Calories */}
        <div>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Calories</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#f59e0b' }}>
            {data.calories_total.toLocaleString()}
          </div>
          <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
            Active: {data.calories_active} | BMR: {data.calories_bmr}
          </div>
        </div>

        {/* Intensity Minutes */}
        <div>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Intensity Minutes</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#8b5cf6' }}>
            {totalIntensityMinutes}
          </div>
          <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
            Moderate: {data.moderate_intensity_minutes} | Vigorous: {data.vigorous_intensity_minutes}
          </div>
        </div>
      </div>
    </Card>
  );
};
