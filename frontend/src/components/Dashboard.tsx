import React, { useState, useEffect } from 'react';
import {
  FluentProvider,
  webLightTheme,
  Button,
  Card,
  Spinner,
  Text
} from '@fluentui/react-components';
import { Calendar24Regular, ArrowSync24Regular } from '@fluentui/react-icons';
import { garminApi, DashboardData } from '../services/api';
import { HeartRateChart } from './HeartRateChart';
import { StressChart } from './StressChart';
import { SleepChart } from './SleepChart';
import { BodyBatteryChart } from './BodyBatteryChart';
import { StepsCaloriesCard } from './StepsCaloriesCard';

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Get today's date in local timezone
  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  
  const [selectedDate, setSelectedDate] = useState<string>(getTodayDate());

  const loadData = async (date: string) => {
    setLoading(true);
    setError(null);
    try {
      const result = await garminApi.getAllData(date);
      setData(result);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedDate);
  }, [selectedDate]);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(e.target.value);
  };

  const handleRefresh = () => {
    loadData(selectedDate);
  };

  const getSummaryStats = () => {
    if (!data) return null;

    const avgHr = data.heart_rate.length > 0
      ? (data.heart_rate.reduce((sum, d) => sum + d.heart_rate_bpm, 0) / data.heart_rate.length).toFixed(1)
      : 'N/A';

    const avgStress = data.stress.length > 0
      ? (data.stress.reduce((sum, d) => sum + d.stress_level, 0) / data.stress.length).toFixed(1)
      : 'N/A';

    const sleepHours = data.sleep
      ? (data.sleep.total_sleep_seconds / 3600).toFixed(1)
      : '0';

    const activityCount = data.activities.length;
    
    const restingHr = data.resting_heart_rate?.resting_heart_rate || null;
    
    const steps = data.steps?.total_steps || 0;
    const calories = data.steps?.calories_total || 0;
    
    const bodyBattery = data.body_battery.length > 0
      ? data.body_battery[data.body_battery.length - 1].battery_level
      : null;

    return { avgHr, avgStress, sleepHours, activityCount, restingHr, steps, calories, bodyBattery };
  };

  const stats = getSummaryStats();

  return (
    <FluentProvider theme={webLightTheme}>
      <div style={{ 
        minHeight: '100vh', 
        backgroundColor: '#f5f5f5', 
        padding: '20px',
        fontFamily: 'Segoe UI, sans-serif'
      }}>
        {/* Header */}
        <div style={{ 
          maxWidth: '1400px', 
          margin: '0 auto',
          backgroundColor: 'white',
          padding: '30px',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          marginBottom: '20px'
        }}>
          <h1 style={{ 
            margin: '0 0 20px 0', 
            color: '#0078d4',
            fontSize: '32px',
            fontWeight: '600'
          }}>
            Garmin Connect Dashboard
          </h1>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <Calendar24Regular />
            <input
              type="date"
              value={selectedDate}
              onChange={handleDateChange}
              style={{
                padding: '8px 12px',
                border: '1px solid #d1d1d1',
                borderRadius: '4px',
                fontSize: '14px'
              }}
            />
            <Button 
              icon={<ArrowSync24Regular />}
              onClick={handleRefresh}
              disabled={loading}
            >
              Refresh
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        {stats && !loading && (
          <div style={{ 
            maxWidth: '1400px', 
            margin: '0 auto 20px auto',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '15px'
          }}>
            <Card style={{ padding: '20px', textAlign: 'center' }}>              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Steps</div>
              <div style={{ fontSize: '32px', color: '#0078d4', fontWeight: '600' }}>
                {stats.steps.toLocaleString()}
              </div>
              <div style={{ fontSize: '12px', color: '#888' }}>today</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Calories</div>
              <div style={{ fontSize: '32px', color: '#f59e0b', fontWeight: '600' }}>
                {stats.calories.toLocaleString()}
              </div>
              <div style={{ fontSize: '12px', color: '#888' }}>kcal</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Body Battery</div>
              <div style={{ fontSize: '32px', color: '#10b981', fontWeight: '600' }}>
                {stats.bodyBattery !== null ? stats.bodyBattery : 'N/A'}
              </div>
              <div style={{ fontSize: '12px', color: '#888' }}>current</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Resting HR</div>
              <div style={{ fontSize: '32px', color: '#e74c3c', fontWeight: '600' }}>
                {stats.restingHr !== null ? stats.restingHr : 'N/A'}
              </div>
              <div style={{ fontSize: '12px', color: '#888' }}>bpm</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Average Heart Rate</div>
              <div style={{ fontSize: '32px', color: '#e74c3c', fontWeight: '600' }}>{stats.avgHr}</div>
              <div style={{ fontSize: '12px', color: '#888' }}>bpm</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Average Stress</div>
              <div style={{ fontSize: '32px', color: '#9b59b6', fontWeight: '600' }}>{stats.avgStress}</div>
              <div style={{ fontSize: '12px', color: '#888' }}>level</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Total Sleep</div>
              <div style={{ fontSize: '32px', color: '#3498db', fontWeight: '600' }}>{stats.sleepHours}</div>
              <div style={{ fontSize: '12px', color: '#888' }}>hours</div>
            </Card>
            
            <Card style={{ padding: '20px', textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Activities</div>
              <div style={{ fontSize: '32px', color: '#27ae60', fontWeight: '600' }}>{stats.activityCount}</div>
              <div style={{ fontSize: '12px', color: '#888' }}>recorded</div>
            </Card>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div style={{ 
            maxWidth: '1400px', 
            margin: '0 auto',
            textAlign: 'center',
            padding: '60px'
          }}>
            <Spinner size="large" label="Loading Garmin data..." />
          </div>
        )}

        {/* Error State */}
        {error && (
          <div style={{ 
            maxWidth: '1400px', 
            margin: '0 auto',
            backgroundColor: '#fef0f0',
            padding: '20px',
            borderRadius: '8px',
            border: '1px solid #e74c3c'
          }}>
            <Text style={{ color: '#e74c3c' }}>Error: {error}</Text>
          </div>
        )}

        {/* Charts */}
        {data && !loading && (
          <div style={{ 
            maxWidth: '1400px', 
            margin: '0 auto',
            display: 'grid',
            gap: '20px'
          }}>
            <StepsCaloriesCard data={data.steps} />
            <BodyBatteryChart data={data.body_battery} />
            <HeartRateChart data={data.heart_rate} />
            <StressChart data={data.stress} />
            <SleepChart data={data.sleep} />
            
            {/* Activities List */}
            {data.activities.length > 0 && (
              <Card style={{ padding: '20px' }}>
                <h3 style={{ marginBottom: '15px' }}>Activities</h3>
                <div style={{ display: 'grid', gap: '10px' }}>
                  {data.activities.map((activity, index) => (
                    <Card key={index} style={{ padding: '15px', backgroundColor: '#f9f9f9' }}>
                      <div style={{ fontWeight: '600', color: '#27ae60', marginBottom: '5px' }}>
                        {activity.activity_name}
                      </div>
                      <div style={{ fontSize: '14px', color: '#666' }}>
                        <span style={{ marginRight: '15px' }}>
                          Duration: {Math.round(activity.duration_seconds / 60)} min
                        </span>
                        {activity.avg_heart_rate && (
                          <span style={{ marginRight: '15px' }}>
                            Avg HR: {activity.avg_heart_rate} bpm
                          </span>
                        )}
                        {activity.calories && (
                          <span>Calories: {activity.calories}</span>
                        )}
                      </div>
                      <div style={{ fontSize: '12px', color: '#999', marginTop: '5px' }}>
                        {activity.start_time}
                      </div>
                    </Card>
                  ))}
                </div>
              </Card>
            )}
          </div>
        )}
      </div>
    </FluentProvider>
  );
};
