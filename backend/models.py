"""
Database models for Garmin health data
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class HeartRate(Base):
    __tablename__ = "heart_rate"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    heart_rate_bpm = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Stress(Base):
    __tablename__ = "stress"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    stress_level = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Sleep(Base):
    __tablename__ = "sleep"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    sleep_start = Column(DateTime, nullable=True)
    sleep_end = Column(DateTime, nullable=True)
    total_sleep_seconds = Column(Integer, nullable=False)
    deep_sleep_seconds = Column(Integer, nullable=False)
    light_sleep_seconds = Column(Integer, nullable=False)
    rem_sleep_seconds = Column(Integer, nullable=False)
    awake_seconds = Column(Integer, nullable=False)
    sleep_score = Column(Integer, nullable=True)
    sleep_quality = Column(String(50), nullable=True)
    avg_respiration = Column(Float, nullable=True)
    avg_spo2 = Column(Float, nullable=True)
    lowest_spo2 = Column(Float, nullable=True)
    restless_moments = Column(Integer, nullable=True)
    body_battery_change = Column(Integer, nullable=True)
    avg_overnight_hrv = Column(Float, nullable=True)
    hrv_status = Column(String(50), nullable=True)
    resting_heart_rate = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, nullable=False, unique=True, index=True)
    date = Column(Date, nullable=False, index=True)
    activity_name = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    distance_meters = Column(Float, nullable=True)
    avg_heart_rate = Column(Integer, nullable=True)
    max_heart_rate = Column(Integer, nullable=True)
    calories = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class BodyBattery(Base):
    __tablename__ = "body_battery"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    charged = Column(Integer, nullable=True)
    drained = Column(Integer, nullable=True)
    level = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class DailySteps(Base):
    __tablename__ = "daily_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    total_steps = Column(Integer, nullable=False)
    total_distance_meters = Column(Float, nullable=True)
    total_calories = Column(Integer, nullable=True)
    active_calories = Column(Integer, nullable=True)
    bmr_calories = Column(Integer, nullable=True)
    moderate_intensity_minutes = Column(Integer, nullable=True)
    vigorous_intensity_minutes = Column(Integer, nullable=True)
    floors_ascended = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class RestingHeartRate(Base):
    __tablename__ = "resting_heart_rate"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    resting_hr = Column(Integer, nullable=False)
    min_hr = Column(Integer, nullable=True)
    max_hr = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class HRV(Base):
    __tablename__ = "hrv"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    hrv_value = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
