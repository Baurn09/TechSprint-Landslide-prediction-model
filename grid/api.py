from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# Enable connection between React (port 3000) and Python (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. DATA MODELS ---
# This is what the Frontend sends to us
class Bounds(BaseModel):
    north: float
    south: float
    east: float
    west: float

class GridRequest(BaseModel):
    bounds: Bounds

# --- 2. GRID GENERATION ENGINE ---
# This logic matches what you used to generate your HTML file.
def generate_manipur_grids():
    print("Generating Manipur Grid System...")
    grids = []
    
    # Coordinates covering the Noney/Tupul/Imphal region
    # We use a 0.005 step (approx 500m) for performance
    lat_start, lat_end = 24.50, 25.10 
    lon_start, lon_end = 93.40, 94.20
    step = 0.005 

    lats = np.arange(lat_start, lat_end, step)
    lons = np.arange(lon_start, lon_end, step)

    count = 0
    for lat in lats:
        for lon in lons:
            count += 1
            
            # Simulate sensor data (In real life, you'd fetch this from a DB)
            rainfall = round(np.random.uniform(20, 150), 1)
            tilt = round(np.random.uniform(0, 15), 1)
            
            # Simple Risk Algorithm
            # High Rain + High Tilt = High Risk
            risk_score = min((rainfall * 0.4) + (tilt * 3), 100)
            
            status = "Low"
            if risk_score > 80: status = "High"
            elif risk_score > 50: status = "Moderate"

            grids.append({
                "grid_id": f"G_{count}",
                # React Leaflet needs bounds: [[south, west], [north, east]]
                "bounds": [[lat, lon], [lat + step, lon + step]],
                # Center points for filtering
                "lat_center": lat + (step/2),
                "lon_center": lon + (step/2),
                "rainfall": rainfall,
                "tilt": tilt,
                "risk_score": round(risk_score, 1),
                "status": status
            })
            
    print(f"✅ Generated {len(grids)} active monitoring grids.")
    return grids

# Load the grids into memory as soon as the server starts
ALL_GRIDS = generate_manipur_grids()

# --- 3. API ENDPOINTS ---

@app.post("/get-grids")
async def get_grids(request: GridRequest):
    """
    Receives the map's current view (North/South/East/West)
    and returns ONLY the grids inside that view.
    """
    bounds = request.bounds
    visible_grids = []
    
    # Filter the 10,000+ grids down to just what is visible
    # This keeps the app fast.
    for grid in ALL_GRIDS:
        lat = grid["lat_center"]
        lon = grid["lon_center"]
        
        if (bounds.south <= lat <= bounds.north) and (bounds.west <= lon <= bounds.east):
            visible_grids.append(grid)
            
    return visible_grids