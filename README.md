# Landslide Early Warning System

An **AI-powered landslide early warning system** that combines  
**ground sensors, machine learning, software analytics, and satellite-assisted monitoring**
to detect and assess landslide risk in real time.

---

## 🚀 Project Overview

Landslides are sudden and destructive natural disasters, especially in hilly and high-rainfall regions.  
This project aims to provide an **early warning mechanism** by:

- Identifying **landslide-prone areas** using satellite data
- Deploying **ground sensors** for real-time monitoring
- Using **machine learning** to classify risk levels
- Triggering alerts when conditions become dangerous

---

## 🧠 How the System Works

1. **Satellite Analysis (WHERE)**
   - Terrain slope and vegetation indices (NDVI) are extracted
   - High-risk zones are identified
   - Helps decide where to place ground sensors

2. **Ground Sensors (WHEN)**
   - Soil moisture sensor
   - Tilt / IMU sensor
   - (Optional) vibration / rainfall sensors
   - Data is collected in real time

3. **Machine Learning (HOW SEVERE)**
   - A Random Forest classifier combines:
     - Sensor data
     - Satellite-derived parameters
   - Outputs risk level: **LOW / MEDIUM / HIGH**

4. **Software & Alerts**
   - Backend receives sensor data
   - ML model predicts risk
   - Alerts can be triggered for high-risk conditions

---

## 🛠️ Tech Stack

### Software
- Python
- pandas, NumPy
- scikit-learn
- (not yet done) (backend)
- GitHub (collaboration & version control)

### Machine Learning
- Random Forest Classifier
- Synthetic training data (based on geotechnical thresholds)

### Hardware
- ESP32 / microcontroller
- Capacitive soil moisture sensor
- MPU6050 (tilt / IMU)
- (Optional) vibration & rainfall sensors

### Satellite Data
- Digital Elevation Model (DEM)
- Sentinel-2 (NDVI / vegetation)
- Used for terrain risk assessment (supporting layer)

---

## 📂 Project Structure

