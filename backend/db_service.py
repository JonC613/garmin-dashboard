"""
Database service for saving and retrieving Garmin data
"""

from sqlalchemy.orm import Session
from models import (
    HeartRate, Stress, Sleep, Activity, BodyBattery, 
    DailySteps, RestingHeartRate, HRV
)
from datetime import datetime, date
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations"""
    
    @staticmethod
    def save_heart_rate_data(db: Session, date_str: str, heart_rate_data: List[Dict[str, Any]]):
        """Save heart rate data to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Delete existing data for this date
            db.query(HeartRate).filter(HeartRate.date == data_date).delete()
            
            # Insert new data
            for item in heart_rate_data:
                hr = HeartRate(
                    date=data_date,
                    datetime=datetime.fromisoformat(item['datetime']),
                    heart_rate_bpm=item['heart_rate_bpm']
                )
                db.add(hr)
            
            db.commit()
            logger.info(f"Saved {len(heart_rate_data)} heart rate records for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving heart rate data: {e}")
            raise
    
    @staticmethod
    def save_stress_data(db: Session, date_str: str, stress_data: List[Dict[str, Any]]):
        """Save stress data to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Delete existing data for this date
            db.query(Stress).filter(Stress.date == data_date).delete()
            
            # Insert new data
            for item in stress_data:
                stress = Stress(
                    date=data_date,
                    datetime=datetime.fromisoformat(item['datetime']),
                    stress_level=item['stress_level']
                )
                db.add(stress)
            
            db.commit()
            logger.info(f"Saved {len(stress_data)} stress records for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving stress data: {e}")
            raise
    
    @staticmethod
    def save_sleep_data(db: Session, sleep_data: Dict[str, Any]):
        """Save sleep data to database"""
        try:
            data_date = datetime.strptime(sleep_data['date'], "%Y-%m-%d").date()
            
            # Check if record exists
            existing = db.query(Sleep).filter(Sleep.date == data_date).first()
            
            sleep_start = None
            if sleep_data.get('sleep_start'):
                sleep_start = datetime.fromisoformat(sleep_data['sleep_start'])
            
            sleep_end = None
            if sleep_data.get('sleep_end'):
                sleep_end = datetime.fromisoformat(sleep_data['sleep_end'])
            
            if existing:
                # Update existing record
                existing.sleep_start = sleep_start
                existing.sleep_end = sleep_end
                existing.total_sleep_seconds = sleep_data['total_sleep_seconds']
                existing.deep_sleep_seconds = sleep_data['deep_sleep_seconds']
                existing.light_sleep_seconds = sleep_data['light_sleep_seconds']
                existing.rem_sleep_seconds = sleep_data['rem_sleep_seconds']
                existing.awake_seconds = sleep_data['awake_seconds']
                existing.sleep_score = sleep_data.get('sleep_score')
                existing.sleep_quality = sleep_data.get('sleep_quality')
                existing.avg_respiration = sleep_data.get('avg_respiration')
                existing.avg_spo2 = sleep_data.get('avg_spo2')
                existing.lowest_spo2 = sleep_data.get('lowest_spo2')
                existing.restless_moments = sleep_data.get('restless_moments')
                existing.body_battery_change = sleep_data.get('body_battery_change')
                existing.avg_overnight_hrv = sleep_data.get('avg_overnight_hrv')
                existing.hrv_status = sleep_data.get('hrv_status')
                existing.resting_heart_rate = sleep_data.get('resting_heart_rate')
                existing.updated_at = datetime.utcnow()
            else:
                # Create new record
                sleep = Sleep(
                    date=data_date,
                    sleep_start=sleep_start,
                    sleep_end=sleep_end,
                    total_sleep_seconds=sleep_data['total_sleep_seconds'],
                    deep_sleep_seconds=sleep_data['deep_sleep_seconds'],
                    light_sleep_seconds=sleep_data['light_sleep_seconds'],
                    rem_sleep_seconds=sleep_data['rem_sleep_seconds'],
                    awake_seconds=sleep_data['awake_seconds'],
                    sleep_score=sleep_data.get('sleep_score'),
                    sleep_quality=sleep_data.get('sleep_quality'),
                    avg_respiration=sleep_data.get('avg_respiration'),
                    avg_spo2=sleep_data.get('avg_spo2'),
                    lowest_spo2=sleep_data.get('lowest_spo2'),
                    restless_moments=sleep_data.get('restless_moments'),
                    body_battery_change=sleep_data.get('body_battery_change'),
                    avg_overnight_hrv=sleep_data.get('avg_overnight_hrv'),
                    hrv_status=sleep_data.get('hrv_status'),
                    resting_heart_rate=sleep_data.get('resting_heart_rate')
                )
                db.add(sleep)
            
            db.commit()
            logger.info(f"Saved sleep record for {sleep_data['date']}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving sleep data: {e}")
            raise
    
    @staticmethod
    def save_activities(db: Session, date_str: str, activities: List[Dict[str, Any]]):
        """Save activities to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            for activity_data in activities:
                activity_id = activity_data['activity_id']
                
                # Check if activity exists
                existing = db.query(Activity).filter(Activity.activity_id == activity_id).first()
                
                start_time = datetime.fromisoformat(activity_data['start_time'])
                
                if existing:
                    # Update existing activity
                    existing.activity_name = activity_data['activity_name']
                    existing.start_time = start_time
                    existing.duration_seconds = activity_data['duration_seconds']
                    existing.distance_meters = activity_data.get('distance_meters')
                    existing.avg_heart_rate = activity_data.get('avg_heart_rate')
                    existing.max_heart_rate = activity_data.get('max_heart_rate')
                    existing.calories = activity_data.get('calories')
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new activity
                    activity = Activity(
                        activity_id=activity_id,
                        date=data_date,
                        activity_name=activity_data['activity_name'],
                        start_time=start_time,
                        duration_seconds=activity_data['duration_seconds'],
                        distance_meters=activity_data.get('distance_meters'),
                        avg_heart_rate=activity_data.get('avg_heart_rate'),
                        max_heart_rate=activity_data.get('max_heart_rate'),
                        calories=activity_data.get('calories')
                    )
                    db.add(activity)
            
            db.commit()
            logger.info(f"Saved {len(activities)} activities for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving activities: {e}")
            raise
    
    @staticmethod
    def save_body_battery_data(db: Session, date_str: str, body_battery_data: List[Dict[str, Any]]):
        """Save body battery data to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Delete existing data for this date
            db.query(BodyBattery).filter(BodyBattery.date == data_date).delete()
            
            # Insert new data
            for item in body_battery_data:
                bb = BodyBattery(
                    date=data_date,
                    datetime=datetime.fromisoformat(item['datetime']),
                    charged=item.get('charged'),
                    drained=item.get('drained'),
                    level=item['level']
                )
                db.add(bb)
            
            db.commit()
            logger.info(f"Saved {len(body_battery_data)} body battery records for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving body battery data: {e}")
            raise
    
    @staticmethod
    def save_daily_steps(db: Session, date_str: str, steps_data: Dict[str, Any]):
        """Save daily steps data to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if record exists
            existing = db.query(DailySteps).filter(DailySteps.date == data_date).first()
            
            if existing:
                # Update existing record
                existing.total_steps = steps_data['total_steps']
                existing.total_distance_meters = steps_data.get('total_distance_meters')
                existing.total_calories = steps_data.get('total_calories')
                existing.active_calories = steps_data.get('active_calories')
                existing.bmr_calories = steps_data.get('bmr_calories')
                existing.moderate_intensity_minutes = steps_data.get('moderate_intensity_minutes')
                existing.vigorous_intensity_minutes = steps_data.get('vigorous_intensity_minutes')
                existing.floors_ascended = steps_data.get('floors_ascended')
                existing.updated_at = datetime.utcnow()
            else:
                # Create new record
                steps = DailySteps(
                    date=data_date,
                    total_steps=steps_data['total_steps'],
                    total_distance_meters=steps_data.get('total_distance_meters'),
                    total_calories=steps_data.get('total_calories'),
                    active_calories=steps_data.get('active_calories'),
                    bmr_calories=steps_data.get('bmr_calories'),
                    moderate_intensity_minutes=steps_data.get('moderate_intensity_minutes'),
                    vigorous_intensity_minutes=steps_data.get('vigorous_intensity_minutes'),
                    floors_ascended=steps_data.get('floors_ascended')
                )
                db.add(steps)
            
            db.commit()
            logger.info(f"Saved daily steps for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving daily steps: {e}")
            raise
    
    @staticmethod
    def save_resting_heart_rate(db: Session, date_str: str, rhr_data: Dict[str, Any]):
        """Save resting heart rate data to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if record exists
            existing = db.query(RestingHeartRate).filter(RestingHeartRate.date == data_date).first()
            
            if existing:
                # Update existing record
                existing.resting_hr = rhr_data['resting_hr']
                existing.min_hr = rhr_data.get('min_hr')
                existing.max_hr = rhr_data.get('max_hr')
                existing.updated_at = datetime.utcnow()
            else:
                # Create new record
                rhr = RestingHeartRate(
                    date=data_date,
                    resting_hr=rhr_data['resting_hr'],
                    min_hr=rhr_data.get('min_hr'),
                    max_hr=rhr_data.get('max_hr')
                )
                db.add(rhr)
            
            db.commit()
            logger.info(f"Saved resting heart rate for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving resting heart rate: {e}")
            raise
    
    @staticmethod
    def save_hrv_data(db: Session, date_str: str, hrv_data: List[Dict[str, Any]]):
        """Save HRV data to database"""
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Delete existing data for this date
            db.query(HRV).filter(HRV.date == data_date).delete()
            
            # Insert new data
            for item in hrv_data:
                hrv = HRV(
                    date=data_date,
                    datetime=datetime.fromisoformat(item['datetime']),
                    hrv_value=item['hrv_value']
                )
                db.add(hrv)
            
            db.commit()
            logger.info(f"Saved {len(hrv_data)} HRV records for {date_str}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving HRV data: {e}")
            raise
    
    @staticmethod
    def save_all_garmin_data(db: Session, date_str: str, data: Dict[str, Any]):
        """Save all Garmin data from API response"""
        try:
            # Save each data type
            if data.get('heart_rate'):
                DatabaseService.save_heart_rate_data(db, date_str, data['heart_rate'])
            
            if data.get('stress'):
                DatabaseService.save_stress_data(db, date_str, data['stress'])
            
            if data.get('sleep'):
                DatabaseService.save_sleep_data(db, data['sleep'])
            
            if data.get('activities'):
                DatabaseService.save_activities(db, date_str, data['activities'])
            
            if data.get('body_battery'):
                DatabaseService.save_body_battery_data(db, date_str, data['body_battery'])
            
            if data.get('steps'):
                DatabaseService.save_daily_steps(db, date_str, data['steps'])
            
            if data.get('resting_heart_rate'):
                DatabaseService.save_resting_heart_rate(db, date_str, data['resting_heart_rate'])
            
            if data.get('hrv'):
                DatabaseService.save_hrv_data(db, date_str, data['hrv'])
            
            logger.info(f"Successfully saved all Garmin data for {date_str}")
        except Exception as e:
            logger.error(f"Error saving all Garmin data: {e}")
            raise
