"""
Garmin Connect Service
Handles data fetching from Garmin Connect API
"""

import json
import logging
from datetime import datetime, date
from pathlib import Path
from garminconnect import Garmin, GarminConnectAuthenticationError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GarminService:
    """Service class for Garmin Connect data operations."""
    
    def __init__(self):
        """Initialize Garmin service with credentials."""
        self.client = None
        # Use the directory where this file is located
        script_dir = Path(__file__).parent
        self.creds_file = script_dir / "garmin_credentials.json"
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Garmin Connect."""
        if not self.creds_file.exists():
            raise FileNotFoundError(
                "garmin_credentials.json not found. Please create it with your email and password."
            )
        
        try:
            with open(self.creds_file, 'r') as f:
                creds = json.load(f)
                email = creds.get('email')
                password = creds.get('password')
            
            print("Authenticating with Garmin Connect...")
            self.client = Garmin(email, password)
            self.client.login()
            print("✓ Successfully authenticated!")
            
        except GarminConnectAuthenticationError as e:
            raise Exception(f"Authentication failed: {e}")
        except Exception as e:
            raise Exception(f"Error during authentication: {e}")
    
    def get_heart_rate_data(self, target_date: str):
        """Get heart rate data for a specific date."""
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            hr_data = self.client.get_heart_rates(dt.isoformat())
            
            if not hr_data or 'heartRateValues' not in hr_data or hr_data['heartRateValues'] is None:
                return []
            
            records = []
            for entry in hr_data['heartRateValues']:
                if not entry or len(entry) < 2:
                    continue
                
                timestamp_ms = entry[0]
                hr_value = entry[1]
                
                if hr_value and hr_value > 0:
                    try:
                        dt_obj = datetime.fromtimestamp(timestamp_ms / 1000)
                        records.append({
                            'datetime': dt_obj.isoformat(),
                            'time': dt_obj.strftime('%H:%M:%S'),
                            'heart_rate_bpm': int(hr_value)
                        })
                    except (ValueError, TypeError):
                        continue
            
            return records
            
        except Exception as e:
            raise Exception(f"Error fetching heart rate data: {e}")
    
    def get_stress_data(self, target_date: str):
        """Get stress data for a specific date."""
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            stress_data = self.client.get_stress_data(dt.isoformat())
            
            if not stress_data or 'stressValuesArray' not in stress_data or stress_data['stressValuesArray'] is None:
                return []
            
            records = []
            for entry in stress_data['stressValuesArray']:
                if entry[1] is not None and entry[1] >= 0:
                    timestamp_ms = entry[0]
                    stress_level = entry[1]
                    dt_obj = datetime.fromtimestamp(timestamp_ms / 1000)
                    
                    records.append({
                        'datetime': dt_obj.isoformat(),
                        'time': dt_obj.strftime('%H:%M:%S'),
                        'stress_level': stress_level
                    })
            
            return records
            
        except Exception as e:
            raise Exception(f"Error fetching stress data: {e}")
    
    def get_sleep_data(self, target_date: str):
        """Get sleep data for a specific date."""
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            sleep_data = self.client.get_sleep_data(dt.isoformat())
            
            if not sleep_data:
                return None
            
            # Extract daily sleep DTO for cleaner access
            daily_dto = sleep_data.get('dailySleepDTO', {})
            
            # Extract SpO2 data
            spo2_data = sleep_data.get('wellnessSpO2SleepSummaryDTO', {})
            
            return {
                'date': target_date,
                'sleep_start': daily_dto.get('sleepStartTimestampLocal'),
                'sleep_end': daily_dto.get('sleepEndTimestampLocal'),
                'total_sleep_seconds': daily_dto.get('sleepTimeSeconds', 0),
                'deep_sleep_seconds': daily_dto.get('deepSleepSeconds', 0),
                'light_sleep_seconds': daily_dto.get('lightSleepSeconds', 0),
                'rem_sleep_seconds': daily_dto.get('remSleepSeconds', 0),
                'awake_seconds': daily_dto.get('awakeSleepSeconds', 0),
                'sleep_score': daily_dto.get('overallSleepScore'),
                'sleep_quality': daily_dto.get('sleepQualityTypeName'),
                'avg_respiration': daily_dto.get('averageRespirationValue'),
                'avg_spo2': spo2_data.get('averageSpO2Value'),
                'lowest_spo2': spo2_data.get('lowestSpO2Value'),
                'restless_moments': sleep_data.get('restlessMomentsCount'),
                'body_battery_change': sleep_data.get('bodyBatteryChange'),
                'avg_overnight_hrv': sleep_data.get('avgOvernightHrv'),
                'hrv_status': sleep_data.get('hrvStatus'),
                'resting_heart_rate': sleep_data.get('restingHeartRate')
            }
            
        except Exception as e:
            raise Exception(f"Error fetching sleep data: {e}")
    
    def get_activities(self, target_date: str):
        """Get activities for a specific date."""
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            activities = self.client.get_activities_by_date(
                dt.isoformat(),
                dt.isoformat()
            )
            
            if not activities:
                return []
            
            activity_list = []
            for activity in activities:
                activity_list.append({
                    'activity_id': activity.get('activityId'),
                    'activity_name': activity.get('activityName'),
                    'start_time': activity.get('startTimeLocal'),
                    'duration_seconds': activity.get('duration'),
                    'distance_meters': activity.get('distance'),
                    'avg_heart_rate': activity.get('averageHR'),
                    'max_heart_rate': activity.get('maxHR'),
                    'calories': activity.get('calories')
                })
            
            return activity_list
            
        except Exception as e:
            raise Exception(f"Error fetching activities: {e}")
    
    def get_body_battery_data(self, target_date: str):
        """Get body battery data for a specific date."""
        logger.info(f"Fetching body battery data for {target_date}")
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            logger.debug(f"Calling get_body_battery for date: {dt.isoformat()}")
            # Body battery is fetched as a range, we'll get start and end date the same
            battery_data = self.client.get_body_battery(dt.isoformat(), dt.isoformat())
            logger.debug(f"Body battery response type: {type(battery_data)}, length: {len(battery_data) if battery_data else 0}")
            
            if not battery_data or not isinstance(battery_data, list) or len(battery_data) == 0:
                logger.warning("No body battery data returned")
                return []
            
            # Extract the bodyBatteryValuesArray from the first element
            first_day = battery_data[0]
            logger.debug(f"First day keys: {first_day.keys() if isinstance(first_day, dict) else 'not a dict'}")
            battery_values = first_day.get('bodyBatteryValuesArray', [])
            logger.debug(f"Battery values count: {len(battery_values)}")
            
            if not battery_values:
                return []
            
            records = []
            for entry in battery_values:
                if entry and isinstance(entry, list) and len(entry) >= 2:
                    timestamp_ms = entry[0]
                    battery_level = entry[1]
                    
                    if battery_level is not None:
                        try:
                            dt_obj = datetime.fromtimestamp(timestamp_ms / 1000)
                            records.append({
                                'datetime': dt_obj.isoformat(),
                                'time': dt_obj.strftime('%H:%M:%S'),
                                'battery_level': int(battery_level)
                            })
                        except (ValueError, TypeError):
                            continue
            
            logger.info(f"Returning {len(records)} body battery records")
            return records
            
        except Exception as e:
            # Body battery might not be available for all users/devices
            logger.error(f"Error fetching body battery data: {e}", exc_info=True)
            return []
    
    def get_steps_data(self, target_date: str):
        """Get steps data for a specific date."""
        logger.info(f"Fetching steps data for {target_date}")
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            logger.debug(f"Calling get_steps_data for date: {dt.isoformat()}")
            steps_data = self.client.get_steps_data(dt.isoformat())
            logger.debug(f"Steps data type: {type(steps_data)}, length: {len(steps_data) if steps_data else 0}")
            
            if not steps_data or not isinstance(steps_data, list):
                logger.warning("No steps data returned or invalid format")
                return None
            
            # Sum up all the steps from 15-minute intervals
            total_steps = sum(interval.get('steps', 0) for interval in steps_data)
            logger.debug(f"Calculated total steps: {total_steps}")
            
            # Get user stats to find step goal and other metrics
            try:
                logger.debug("Fetching user summary for additional metrics")
                user_summary = self.client.get_user_summary(dt.isoformat())
                logger.debug(f"User summary keys: {user_summary.keys() if isinstance(user_summary, dict) else 'not a dict'}")
                step_goal = user_summary.get('dailyStepGoal', 10000)
                total_distance_meters = user_summary.get('totalDistanceMeters', 0)
                calories_total = user_summary.get('totalKilocalories', 0)
                calories_bmr = user_summary.get('bmrKilocalories', 0)
                calories_active = user_summary.get('activeKilocalories', 0)
                moderate_intensity = user_summary.get('moderateIntensityMinutes', 0)
                vigorous_intensity = user_summary.get('vigorousIntensityMinutes', 0)
            except Exception as e:
                logger.warning(f"Could not fetch user summary: {e}")
                step_goal = 10000
                total_distance_meters = 0
                calories_total = 0
                calories_bmr = 0
                calories_active = 0
                moderate_intensity = 0
                vigorous_intensity = 0
            
            result = {
                'date': target_date,
                'total_steps': total_steps,
                'step_goal': step_goal,
                'total_distance_meters': total_distance_meters,
                'calories_total': calories_total,
                'calories_bmr': calories_bmr,
                'calories_active': calories_active,
                'moderate_intensity_minutes': moderate_intensity,
                'vigorous_intensity_minutes': vigorous_intensity
            }
            logger.info(f"Returning steps data: {total_steps} steps")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching steps data: {e}", exc_info=True)
            return None
    
    def get_resting_heart_rate(self, target_date: str):
        """Get resting heart rate for a specific date."""
        logger.info(f"Fetching resting heart rate for {target_date}")
        if not self.client:
            raise Exception("Not authenticated")
        
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            logger.debug(f"Calling get_rhr_day for date: {dt.isoformat()}")
            rhr_data = self.client.get_rhr_day(dt.isoformat())
            logger.debug(f"RHR data keys: {rhr_data.keys() if isinstance(rhr_data, dict) else 'not a dict'}")
            
            if not rhr_data or 'allMetrics' not in rhr_data:
                logger.warning("No resting heart rate data returned")
                return None
            
            # Extract resting heart rate from nested structure
            metrics_map = rhr_data.get('allMetrics', {}).get('metricsMap', {})
            logger.debug(f"Metrics map keys: {metrics_map.keys() if isinstance(metrics_map, dict) else 'not a dict'}")
            rhr_metric = metrics_map.get('WELLNESS_RESTING_HEART_RATE', [])
            logger.debug(f"RHR metric: {rhr_metric}")
            
            resting_hr = None
            if rhr_metric and len(rhr_metric) > 0:
                resting_hr = rhr_metric[0].get('value')
            
            # Get min/max heart rate from heart rate data
            min_hr = None
            max_hr = None
            try:
                logger.debug("Fetching heart rate data for min/max calculation")
                hr_data = self.client.get_heart_rates(dt.isoformat())
                if hr_data and 'heartRateValues' in hr_data:
                    hr_values = [
                        entry[1] for entry in hr_data['heartRateValues'] 
                        if entry and len(entry) > 1 and entry[1] is not None
                    ]
                    if hr_values:
                        min_hr = min(hr_values)
                        max_hr = max(hr_values)
                        logger.debug(f"Calculated min/max HR: {min_hr}/{max_hr}")
            except Exception as e:
                logger.warning(f"Could not calculate min/max HR: {e}")
            
            result = {
                'date': target_date,
                'resting_heart_rate': int(resting_hr) if resting_hr else None,
                'min_heart_rate': min_hr,
                'max_heart_rate': max_hr
            }
            logger.info(f"Returning RHR: {result['resting_heart_rate']}")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching resting heart rate: {e}", exc_info=True)
            return None
    
    def get_all_data(self, target_date: str):
        """Get all data for a specific date."""
        return {
            'date': target_date,
            'heart_rate': self.get_heart_rate_data(target_date),
            'stress': self.get_stress_data(target_date),
            'sleep': self.get_sleep_data(target_date),
            'activities': self.get_activities(target_date),
            'body_battery': self.get_body_battery_data(target_date),
            'steps': self.get_steps_data(target_date),
            'resting_heart_rate': self.get_resting_heart_rate(target_date)
        }
