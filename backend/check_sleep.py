from garmin_service import GarminService
import json

s = GarminService()
data = s.client.get_sleep_data('2025-12-25')

print("=== dailySleepDTO ===")
daily = data.get('dailySleepDTO', {})
print(f"Sleep start: {daily.get('sleepStartTimestampLocal')}")
print(f"Sleep end: {daily.get('sleepEndTimestampLocal')}")
print(f"Sleep score: {daily.get('overallSleepScore')}")
print(f"Sleep quality: {daily.get('sleepQualityTypeName')}")
print(f"Validation: {daily.get('validation')}")

print("\n=== Sleep Stages ===")
print(f"Deep sleep: {daily.get('deepSleepSeconds')} sec ({daily.get('deepSleepSeconds', 0)/3600:.2f} hrs)")
print(f"Light sleep: {daily.get('lightSleepSeconds')} sec ({daily.get('lightSleepSeconds', 0)/3600:.2f} hrs)")
print(f"REM sleep: {daily.get('remSleepSeconds')} sec ({daily.get('remSleepSeconds', 0)/3600:.2f} hrs)")
print(f"Awake: {daily.get('awakeSleepSeconds')} sec ({daily.get('awakeSleepSeconds', 0)/3600:.2f} hrs)")

print("\n=== Sleep Metrics ===")
print(f"Restless moments: {data.get('restlessMomentsCount')}")
print(f"Body battery change: {data.get('bodyBatteryChange')}")
print(f"Avg overnight HRV: {data.get('avgOvernightHrv')}")
print(f"HRV status: {data.get('hrvStatus')}")
print(f"Resting HR: {data.get('restingHeartRate')}")

print("\n=== Respiration ===")
spo2 = data.get('wellnessSpO2SleepSummaryDTO', {})
print(f"Avg SpO2: {spo2.get('averageSpO2Value')}")
print(f"Lowest SpO2: {spo2.get('lowestSpO2Value')}")

print("\n=== Available detailed data ===")
print(f"Sleep levels (stages timeline): {len(data.get('sleepLevels', []))} records")
print(f"Sleep movement data: {len(data.get('sleepMovement', []))} records")
print(f"REM sleep data: {bool(data.get('remSleepData'))}")
print(f"SpO2 epoch data: {len(data.get('wellnessEpochSPO2DataDTOList', []))} records")
print(f"Respiration data: {len(data.get('wellnessEpochRespirationDataDTOList', []))} records")
print(f"Sleep heart rate: {bool(data.get('sleepHeartRate'))}")
print(f"Sleep stress: {bool(data.get('sleepStress'))}")
print(f"Sleep body battery: {bool(data.get('sleepBodyBattery'))}")
print(f"HRV data: {bool(data.get('hrvData'))}")
print(f"Breathing disruption: {bool(data.get('breathingDisruptionData'))}")
