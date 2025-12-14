import sys
import os
import json

# Add current directory to path so we can import api module
sys.path.append(os.getcwd())

try:
    from api.index import get_race_pace
except ImportError:
    # Fallback if running from src directory
    sys.path.append(os.path.dirname(os.getcwd()))
    from api.index import get_race_pace

def verify():
    print("Testing get_race_pace()...")
    # Use a known race, Bahrain 2021
    try:
        # We assume the cache directory setup in api/index.py works (it sets it to /tmp)
        result = get_race_pace(year=2021, gp='Bahrain', session_type='R')
        
        if not result or 'data' not in result:
             print("FAILED: No data returned")
             return

        drivers_count = len(result['data'])
        print(f"Success! Retrieved data for {drivers_count} drivers.")
        
        if drivers_count > 0:
            sample = result['data'][0]
            print(f"Metrics key present: {'metrics' in sample}")
            print(f"Sample Driver: {sample['driver']}")
            print(f"Sample Team: {sample['team']}")
            print(f"Sample Median Lap: {sample['metrics']['median']}")
            
            # Simple validation rules
            if sample['metrics']['median'] < 50:
                 print("WARNING: Median lap time seems too low (<50s)")
            
        # Save full sample output for inspection
        os.makedirs('output', exist_ok=True)
        with open('output/race_pace_sample.json', 'w') as f:
            json.dump(result, f, indent=2)
            
    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()
