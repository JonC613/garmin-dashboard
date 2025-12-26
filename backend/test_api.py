"""Test script to check available Garmin API data"""
import json
from garmin_service import GarminService

# Initialize service (auto-authenticates)
service = GarminService()

target_date = "2025-12-25"

print("=" * 50)
print("Testing Body Battery:")
try:
    from datetime import datetime
    dt = datetime.strptime(target_date, "%Y-%m-%d").date()
    battery_data = service.client.get_body_battery(dt.isoformat(), dt.isoformat())
    print("Success! Type:", type(battery_data))
    print("Data:", json.dumps(battery_data, indent=2, default=str)[:500])
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Testing Steps Data:")
try:
    steps_data = service.client.get_steps_data(dt.isoformat())
    print("Success! Type:", type(steps_data))
    print("Data:", json.dumps(steps_data, indent=2, default=str)[:500])
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Testing Resting Heart Rate:")
try:
    rhr_data = service.client.get_rhr_day(dt.isoformat())
    print("Success! Type:", type(rhr_data))
    print("Data:", json.dumps(rhr_data, indent=2, default=str)[:500])
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Testing get_daily_steps (alternative):")
try:
    daily_steps = service.client.get_daily_steps(dt.isoformat())
    print("Success! Type:", type(daily_steps))
    print("Data:", json.dumps(daily_steps, indent=2, default=str)[:500])
except Exception as e:
    print(f"Error: {e}")
