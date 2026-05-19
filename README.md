
# 🚁 Autonomous Drone Digital Twin & Telemetry Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-3C5280)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)

An **Edge-to-Cloud Geospatial Digital Twin** built in Python. This distributed system simulates real-time UAV telemetry, runs continuous predictive analytics to detect hardware and environmental anomalies, and visualizes flight dynamics on a live radar dashboard. The architecture features an autonomous "Edge Reflex" loop designed to execute emergency safety interventions with zero latency.

## Table of Contents
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Execution Guide](#execution-guide)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Results](#results)

## Core Features

*   **Real-Time Predictive Engine:** Utilizes the Haversine formula to dynamically calculate a 30-second future thermal trajectory and safe-return range.
*   **Invisible Anomaly Detection:** Cross-references throttle output against GPS ground speed to identify invisible environmental hazards, such as severe headwinds or aerodynamic drag.
*   **Autonomous Edge Reflex:** The simulated edge device actively monitors safety channels to independently execute zero-latency throttle kills or Return-To-Home (RTH) protocols.
*   **Multi-Mission State Machine:** Automatically cycles through three distinct operational profiles to stress-test the digital twin:
    1.  *Mission 1 (Normal Flight):* Culminates in a **Thermal Meltdown**.
    2.  *Mission 2 (Hyper Speed):* Culminates in a **Safe Range Breach**.
    3.  *Mission 3 (Hurricane Headwind):* Culminates in an **Invisible Wind Anomaly**.
*   **Live Radar Control Room:** A modern `Streamlit` and `Folium` interface tracking live GPS coordinates, telemetry streams, and dynamic safety status banners.

## System Architecture

The system utilizes a **Decoupled Microservices Architecture** communicating via the MQTT protocol:

1.  **Edge Simulator (`edge_simulator.py`):** Represents the physical UAV. Publishes raw sensor telemetry (Throttle, Temperature, Speed, Lat/Lon) and subscribes to emergency override commands.
2.  **Message Broker (Eclipse Mosquitto):** A containerized central router ensuring low-latency, decoupled publish/subscribe communication.
3.  **Digital Twin Engine (`digital_twin.py`):** The analytical core. Subscribes to raw sensor data, processes predictive algorithms, and publishes safety commands and analytics.
4.  **Dashboard (`dashboard.py`):** The control room interface. A passive subscriber that visualizes the geospatial data flow and renders the live map.

## Prerequisites

*   **Python 3.8+**
*   **Docker** (required for the Mosquitto MQTT Broker)
*   **Git**

## Installation & Setup

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/drone-digital-twin.git](https://github.com/yourusername/drone-digital-twin.git)
cd drone-digital-twin

```

**2. Install Python dependencies:**

```bash
pip install paho-mqtt streamlit pandas folium streamlit-folium

```

**3. Start the MQTT Broker:**
Spin up the Eclipse Mosquitto broker on port 1883 using Docker:

```bash
docker run -it -p 1883:1883 eclipse-mosquitto

```

## Execution Guide

As a distributed system, all components must run concurrently. With your Docker MQTT broker running in the background, open **three separate terminals** and execute the following in order:

**Terminal 1: Launch the Dashboard**

```bash
python -m streamlit run dashboard.py

```

*(The UI will automatically open in your browser at `http://localhost:8501`)*

**Terminal 2: Start the Digital Twin Engine**

```bash
python digital_twin.py

```

*(Wait for the initialization confirmation: `[TWIN] Online. Monitoring flight dynamics...`)*

**Terminal 3: Launch the Drone Mission**

```bash
python edge_simulator.py

```

Switch to your web browser to monitor the Digital Twin as it predicts and prevents system failures in real time.

## Project Structure

```text
drone-digital-twin/
├── edge_simulator.py    # Generates physical telemetry and executes reflex actions
├── digital_twin.py      # Core predictive algorithms and anomaly detection
├── dashboard.py         # Streamlit/Folium UI for real-time visualization
└── README.md            # Project documentation

```

## Future Enhancements

* **Hardware Integration:** Replace the software simulator with C++ firmware flashed to an ESP32 microcontroller, reading live data from an INA219 current sensor and GPS module.
* **Cloud Migration:** Transition from a local Mosquitto broker to **Azure IoT Hub**, hosting the Digital Twin logic within **Azure Functions** or **Azure Digital Twins**.
* **Machine Learning Integration:** Upgrade mathematical prediction models to trained ML algorithms utilizing historical flight degradation datasets.

## Results

*(Below are live captures of the Digital Twin monitoring and responding to flight anomalies.)*

### 1. Live Telemetry & Radar Tracking


*The Folium radar tracking the drone's live GPS coordinates alongside real-time sensor streams.*
<img width="1919" height="852" alt="Screenshot 2026-05-19 191620" src="https://github.com/user-attachments/assets/2959fffb-8cdf-4173-9f87-908841126ad6" />
<img width="1919" height="834" alt="Screenshot 2026-05-19 191711" src="https://github.com/user-attachments/assets/3825a08a-3dd3-45bd-920a-6e3a9d9fe7de" />
<img width="1919" height="822" alt="Screenshot 2026-05-19 191644" src="https://github.com/user-attachments/assets/7fc7c3ea-cd26-4d10-ae36-109180140a51" />






### 2. Architecture
<img width="1536" height="1024" alt="Drone_DT" src="https://github.com/user-attachments/assets/90f61ab4-f879-43b0-a1bb-1e42fdebbd83" />




---

```

```
