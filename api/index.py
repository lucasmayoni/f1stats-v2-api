from fastapi import FastAPI, HTTPException
import fastf1
import pandas as pd
import json
import os

app = FastAPI()

# Enable caching to /tmp (suitable for container environments)
# Note: Cache will not persist across restarts unless a volume is mounted
fastf1.Cache.enable_cache('/tmp')

@app.get("/api/fastest_lap")
def get_fastest_lap(year: int = 2021, gp: str = 'Bahrain', session_type: str = 'Q', driver: str = None):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        
        if driver:
            fastest_lap = session.laps.pick_driver(driver).pick_fastest()
        else:
            fastest_lap = session.laps.pick_fastest()
        car_data = fastest_lap.get_car_data().add_distance()
        
        # Convert to JSON compatible format
        # orient='records' gives a list of objects
        data = json.loads(car_data.to_json(orient='records'))
        
        return {
            "year": year,
            "gp": gp,
            "session_type": session_type,
            "driver": fastest_lap['Driver'],
            "lap_time": str(fastest_lap['LapTime']),
            "telemetry": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/stats/race_pace")
def get_race_pace(year: int = 2021, gp: str = 'Bahrain', session_type: str = 'R'):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        
        # Pick all laps that are accurate (no in/out laps, track limits, etc)
        # We also want to exclude Safety Car / VSC laps to get true race pace
        # '1' indicates clear track status
        laps = session.laps.pick_accurate()
        laps = laps[laps['TrackStatus'] == '1']
        
        # Get list of drivers
        drivers = session.drivers
        
        results = []
        
        for driver in drivers:
            driver_laps = laps.pick_drivers(driver)
            
            if len(driver_laps) == 0:
                continue
                
            # Get driver info
            # Accessing session.results for driver info requires that it is loaded
            # fastf1 v3.1+ usually loads it with session.load()
            # We can pick the first lap to get basic info if needed or lookup in session.results
            # A safer way to get team color/name is from the laps object itself which has team info
            
            team_name = driver_laps['Team'].iloc[0]
            # FastF1 doesn't always have hex colors easily accessible on the lap object without lookups
            # but session.results does.
            try:
                driver_info = session.get_driver(driver)
                team_color = f"#{driver_info['TeamColor']}" if driver_info['TeamColor'] else None
            except:
                team_color = None

            # Calculate stats
            lap_times_seconds = driver_laps['LapTime'].dt.total_seconds()
            
            # Use pandas for quantiles
            q1 = lap_times_seconds.quantile(0.25)
            median = lap_times_seconds.median()
            q3 = lap_times_seconds.quantile(0.75)
            min_lap = lap_times_seconds.min()
            max_lap = lap_times_seconds.max()
            std_dev = lap_times_seconds.std()
            
            results.append({
                "driver": driver,
                "team": team_name,
                "color": team_color,
                "lap_times": lap_times_seconds.tolist(),
                "metrics": {
                    "min": min_lap,
                    "q1": q1,
                    "median": median,
                    "q3": q3,
                    "max": max_lap,
                    "std": std_dev if not pd.isna(std_dev) else 0.0
                }
            })
            
        return {
            "year": year,
            "gp": gp,
            "session_type": session_type,
            "data": results
        }
        
    except Exception as e:
        # In production, logging the error is better than just raising it
        print(f"Error processing race pace: {e}")
        raise HTTPException(status_code=500, detail=str(e))
