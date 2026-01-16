# 🌍 AI-Based Grid-Level Landslide Early Warning System

An **AI-driven landslide early warning system** that integrates **satellite analysis, grid-based monitoring, ground sensors, and machine learning** to assess landslide risk and generate **grid-specific alerts for authorities**.

---

## 🚀 Overview

Landslides are highly localized disasters caused by a combination of **steep slopes, rainfall, weak soil, and reduced vegetation cover**.
Most existing systems issue **broad regional warnings**, which are often inaccurate.

This project focuses on **grid-level landslide risk forecasting**, enabling **precise monitoring and targeted response**.

---

## ▶️ How to Run the Project

Follow the steps below to train the models and start the application locally.

---

### 1️⃣ Train the Machine Learning Models

Open a terminal in the project root and run:

```bash
cd training
python satellite_train.py
python sensor_train.py
```

**What this does:**

* Trains the **satellite landslide risk model** (Gradient Boosted Tree)
* Trains the **ground sensor risk model** (Random Forest)
* Saves trained model files for backend inference

> ⚠️ Training is required only once unless the data or model is updated.

---

### 2️⃣ Start the ML Backend (FastAPI)

Navigate to the ML API directory and start the backend server:

```bash
cd ..
cd ml_api
python -m uvicorn main:app --reload
```

**What this does:**

* Starts the FastAPI backend
* Loads trained ML models
* Exposes REST APIs for risk prediction
* Runs at: `http://localhost:8000`

The `--reload` flag automatically restarts the server on code changes.

---

### 3️⃣ Start the Frontend (Next.js Dashboard)

Open a **new terminal window** and run:

```bash
cd ..
cd web
npm install
npm run dev
```

#### What `npm install` does:

* Installs all frontend dependencies listed in `package.json`
* This includes React, Next.js, chart libraries, and UI utilities
* Required only the **first time** or when dependencies change

#### What `npm run dev` does:

* Starts the Next.js development server
* Runs the web dashboard locally
* Accessible at: `http://localhost:3000`

---

## 🖥️ Running Services Summary

| Service                 | URL                                            |
| ----------------------- | ---------------------------------------------- |
| ML Backend (FastAPI)    | [http://localhost:8000](http://localhost:8000) |
| Web Dashboard (Next.js) | [http://localhost:3000](http://localhost:3000) |

---

## ℹ️ Notes

* Make sure **Python 3.9+** and **Node.js 18+** are installed
* Backend and frontend must run **simultaneously**
* Hardcoded satellite data is used only to demonstrate workflow in the current prototype

---

### ✅ Quick Start (TL;DR)

```bash
cd training
python satellite_train.py
python sensor_train.py

cd ../ml_api
python -m uvicorn main:app --reload

cd ../web
npm install
npm run dev
```

---

## 🧠 System Architecture

### 1. Grid-Based Area Division

* The region is divided into **uniform grid cells**
* Each grid is monitored and evaluated independently
* Risk is calculated **per grid**

### 2. Satellite-Based Risk Assessment (Baseline)

* Satellite-derived features:

  * Rainfall
  * Slope
  * Elevation
  * Vegetation Index (NDVI)
  * Soil proxy
  * Historical landslide susceptibility
* A **Gradient Boosted Tree (GBT)** model estimates baseline landslide susceptibility
* High-risk grids are identified for **ground sensor deployment**

### 3. Ground Sensor Monitoring (Real-Time)

* Sensors are deployed **only in high-risk grids**
* Measures:

  * Soil moisture
  * Tilt
  * Vibration
  * 3-axis acceleration (X, Y, Z)
* Sensors communicate via **LoRa** to a **Grid Gateway**
* Gateway forwards data to the central server where internet is available

### 4. Machine Learning & Risk Evaluation

* **Gradient Boosted Trees** → Satellite data (long-term susceptibility)
* **Random Forest** → Ground sensor data (real-time instability)
* Risk levels:

  * **LOW**
  * **MODERATE**
  * **HIGH**

### 5. Alerts & Dashboard

* Risk is continuously updated per grid
* **Alerts are generated only for authorities**
* A web dashboard provides:

  * Grid-wise risk visualization
  * Sensor status
  * Real-time updates

---

## 🛠️ Tech Stack

### Software & Backend

* Python
* pandas, NumPy
* scikit-learn
* XGBoost
* FastAPI
* GitHub

### Frontend

* Next.js / React
* Grid-based monitoring dashboard

### Machine Learning

* Gradient Boosted Trees (Satellite data)
* Random Forest (Ground sensor data)
* Synthetic + historical datasets

### Hardware

* ESP32 / microcontroller
* Capacitive soil moisture sensor
* MPU6050 (IMU / tilt)
* LoRa communication
* Grid Gateway (internet-enabled)

### Satellite Data

* Digital Elevation Model (DEM)
* Sentinel-2 (NDVI)
* Weather and historical disaster data

---

## 📂 Project Structure
```
training/        # ML training scripts & datasets
backend/         # FastAPI services for ML inference
web/             # Next.js dashboard
hardware/        # Sensor & gateway logic
```
---

## 📌 Key Features

* Grid-level risk forecasting
* Real-time ground monitoring
* AI-based decision support
* Designed for hilly and low-connectivity regions
* Scalable and modular architecture

---

## 📖 Use Case

Designed for **disaster management authorities** to:

* Monitor landslide-prone regions
* Deploy sensors efficiently
* Receive targeted early warnings
* Improve preparedness and response

---

## 📊 Data & Model Training

The machine learning models are trained using a combination of:

* Synthetic datasets generated based on geotechnical knowledge and known landslide-triggering conditions

* Historical records and publicly available environmental references (used for feature design and validation)

* The satellite model is trained on features such as rainfall, slope, vegetation index (NDVI), elevation, soil proxy, and historical susceptibility using a Gradient Boosted Tree.

* The ground sensor model is trained on simulated sensor readings (soil moisture, tilt, vibration, and acceleration) using a Random Forest classifier, designed to handle noisy, real-time data.

---

## ⚠️ Note on Satellite Data in the Prototype

In the current prototype, satellite values are hardcoded within the application.

This is done only to demonstrate the system workflow and decision logic (risk calculation, sensor deployment logic, and alert generation).

In a full deployment, these values would be dynamically fetched from real satellite and weather data sources.

---

### 🔑 One-line summary

> **A grid-based AI system combining satellite intelligence and real-time ground sensing for accurate landslide early warnings.**