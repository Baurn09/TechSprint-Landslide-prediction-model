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

## 🧭 Application Navigation & User Flow

This section explains how users navigate through the system and how information is progressively revealed from **high-level risk overview** to **detailed sensor-level insights**.

---

### 1️⃣ Landing Page

* This is the **entry point** of the application.
* Users can choose between:

  * **View Map** → for geographical risk visualization
  * **Admin Console** → for authority-level monitoring and management

---

### 2️⃣ View Map → Grid-Based Risk Visualization

* Displays an **interactive map divided into grids**.
* Each grid represents an **independent monitoring zone**.

#### Grid Color Coding

* 🟡 **Yellow grids** → Moderate to critical zones identified via satellite analysis
* 🔴 **Red grids** → Aggregated high-risk grids where **ground sensors are deployed**

---

### 3️⃣ Clicking on a Grid (Overview Dialog)

Clicking on a grid opens a **dialog box** showing contextual information, such as:

* **Location**: Senapati Hill Slopes
* **Soil Type**: Clay with colluvial deposits
* **Terrain**: Steep cut slopes
* **Nature of Instability**: Road-induced instability
* **Ground Sensors**: Deployed

A **“View Details”** button is available for deeper inspection.

---

### 4️⃣ View Details → Satellite Risk Assessment

This page provides **satellite-derived risk factors** for the selected grid:

* Slope Factor
* Rainfall Index
* Vegetation Index (NDVI)
* Soil Stability Proxy
* Historical Susceptibility

#### Sensor Deployment Assessment

* **Satellite Risk Score**: `0.922`
* 🔴 **High susceptibility detected. Ground sensors recommended.**

#### Ground Sensor Status

* Ground sensors are **deployed** in this area
* Option available to **View Ground Sensor Data**

---

### 5️⃣ View Ground Sensor Data → Real-Time Monitoring

This page shows **live ground sensor monitoring** for the selected area.

#### Ground Sensor Monitoring

* **Area**: SENAPATI
* **Sensor ID**: —

#### Sensor Readings

* **Soil Moisture (%)**: `95.0`
* **Tilt Index**: `0.149`
* **Vibration Index**: `0.017`

#### Machine Learning Output

* **Model**: Random Forest
* **Ground Sensor Risk Score**: `0.42`

#### Visual Trends

* Soil Moisture Trend
* Motion Magnitude Trend

#### Sensor Configuration

* Soil moisture probe (depth: 1 m)
* 3-axis accelerometer
* Sampling interval: 3 seconds

---

### 6️⃣ Admin Console (Landing Page → Admin)

Accessible from the landing page via **Admin**.

#### Admin Dashboard Overview

**Landslide Monitoring – Admin Console**
*Disaster Management Authority*

* **Monitored Zones**: 6
* **Sensor-Deployed Zones**: 3
* **Active Alerts**: 2
* **Last Update**: 2 minutes ago

#### Active Alerts Table

| Area   | Level    | Time      |
| ------ | -------- | --------- |
| Noney  | CRITICAL | 14:32 IST |
| Ukhrul | WARNING  | 13:10 IST |

---

### 7️⃣ Grid Gateway → Aggregated Sensor Feed

From the Admin Console, selecting **Grid Gateway** opens the **Collection Booth view**.

**Landslide Monitoring – Admin Console**
*Disaster Management Authority*

**Collection Booth (Grid Gateway)**
Aggregated sensor feed from hill-region ground sensors.

| Sensor ID  | Area   | Risk     | Soil (%) | Motion | Last Seen |
| ---------- | ------ | -------- | -------- | ------ | --------- |
| MN-NNY-001 | Noney  | CRITICAL | 83       | 0.792  | 13s ago   |
| MN-NNY-002 | Noney  | SAFE     | 54       | 0.386  | 1s ago    |
| MN-UKH-001 | Ukhrul | SAFE     | 75       | 0.682  | —         |

This view helps authorities:

* Monitor **multiple sensors at once**
* Identify **critical sensor-level anomalies**
* Track **data freshness and connectivity**

---

## 🔑 Navigation Philosophy

* **Map-first → Detail-on-demand**
* **Satellite risk → Sensor confirmation**
* **Public view → Authority-only insights**
* Designed to support **fast decision-making during emergencies**

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
grid/            # Used to give each grid an ID used for independent monitoring (Future Scope)
hardware/        # Sensor & gateway logic (Future Scope)
ml_api/          # FastAPI services for satellite ML inference
training/        # ML training scripts & datasets
web/             # Next.js dashboard
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