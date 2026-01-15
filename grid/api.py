from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random # Replace with your AI model imports

app = FastAPI()

# Enable CORS so Next.js (port 3000) can talk to Python (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data structure you expect from Next.js
class GridRequest(BaseModel):
    grid_id: str
    rainfall: float
    tilt: float

# Load your AI Model here (runs only once on startup!)
# model = load_model("landslide_model.h5")
print("AI Model Loaded")

@app.post("/predict-risk")
async def predict_risk(data: GridRequest):
    # In reality: result = model.predict([[data.rainfall, data.tilt]])
    # Simulating logic for now:
    calculated_risk = (data.rainfall * 0.5) + (data.tilt * 2)

    return {
        "grid_id": data.grid_id,
        "risk_score": min(calculated_risk, 100), # Cap at 100%
        "status": "High" if calculated_risk > 80 else "Low"
    }

# Run with: uvicorn api:app --reload