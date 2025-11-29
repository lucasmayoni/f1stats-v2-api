from fastapi import FastAPI, HTTPException
import fastf1
import pandas as pd
import json
import os

app = FastAPI()

# Enable caching to /tmp for Vercel (read-only filesystem elsewhere)
# Note: Cache will not persist across cold starts
fastf1.Cache.enable_cache('/tmp')

@app.get("/api/fastest_lap")
def get_fastest_lap(year: int = 2021, gp: str = 'Bahrain', session_type: str = 'Q'):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        
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
