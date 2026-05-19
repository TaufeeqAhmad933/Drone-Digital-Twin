
***

```markdown
# 🚁 Autonomous Drone Digital Twin & Telemetry Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-3C5280)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)

An **Edge-to-Cloud Geospatial Digital Twin** built in Python. This distributed system simulates real-time drone telemetry, runs continuous predictive analytics to detect hardware/environmental anomalies, and visualizes the flight dynamics on a live radar dashboard. It features an autonomous "Edge Reflex" loop that executes emergency safety interventions with zero latency.

## ✨ Key Features

* **Real-Time Predictive Engine:** Calculates a 30-second future thermal trajectory and dynamic safe-return range using the Haversine formula.
* **Invisible Anomaly Detection:** Correlates throttle output with GPS ground speed to detect invisible environmental hazards (e.g., severe headwinds).
* **Autonomous Edge Reflex:** The simulated physical edge device independently listens for safety commands and instantly kills throttle or initiates Return-To-Home (RTH) protocols.
* **Multi-Mission State Machine:** Automatically cycles through 3 distinct mission profiles:
  1. *Mission 1:* Normal Flight $\rightarrow$ Triggers **Thermal Meltdown**.
  2. *Mission 2:* Hyper Speed $\rightarrow$ Triggers **Safe Range Breach**.
  3. *Mission 3:* Hurricane Headwind $\rightarrow$ Triggers **Invisible Wind Anomaly**.
* **Live Radar Control Room:** A modern `Streamlit` + `Folium` dashboard that tracks live GPS coordinates, telemetry, and dynamic safety status banners.

---

## 🏗️ System Architecture

This project uses a **Decoupled Microservices Architecture** communicating over the MQTT protocol:

1. **Edge Simulator (`edge_simulator.py`):** Acts as the physical drone. Publishes raw sensor telemetry (Throttle, Temp, Speed, Lat, Lon) and subscribes to emergency commands.
2. **Message Broker (Eclipse Mosquitto):** The central router running in Docker, ensuring decoupled, lightning-fast pub/sub communication.
3. **Digital Twin Engine (`digital_twin.py`):** The "Brain". Subscribes to the raw sensors, processes predictive algorithms, and publishes analytics and safety commands.
4. **Dashboard (`dashboard.py`):** The "Control Room". A passive subscriber that visualizes the data flow and renders the live map.

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:
* **Python 3.8+**
* **Docker** (to run the Mosquitto MQTT Broker)
* Git

---

## 🚀 Installation & Setup

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/drone-digital-twin.git](https://github.com/yourusername/drone-digital-twin.git)
cd drone-digital-twin
```

**2. Install Python dependencies:**
```bash
pip install paho-mqtt streamlit pandas folium streamlit-folium
```

**3. Start the MQTT Broker (via Docker):**
Open a terminal and spin up the Eclipse Mosquitto broker on port 1883:
```bash
docker run -it -p 1883:1883 eclipse-mosquitto
```

---

## 🎮 How to Run the System

Because this is a distributed system, you need to run the components simultaneously. **Open three separate terminals** (leave your Docker broker running in the background) and run them in this exact order:

**Terminal 1: Launch the Dashboard**
```bash
python -m streamlit run dashboard.py
```
*(This will automatically open the UI in your web browser at `http://localhost:8501`)*

**Terminal 2: Start the Digital Twin Engine**
```bash
python digital_twin.py
```
*(Wait to see `[TWIN] Online. Monitoring flight dynamics...`)*

**Terminal 3: Launch the Drone Mission**
```bash
python edge_simulator.py
```

Now, switch to your web browser and watch the Digital Twin predict and prevent system failures in real-time!

---

## 📂 Project Structure

```text
drone-digital-twin/
│
├── edge_simulator.py    # Generates fake physical data and executes reflexes
├── digital_twin.py      # Runs the predictive math and anomaly detection
├── dashboard.py         # Streamlit/Folium UI for real-time visualization
└── README.md            # Project documentation
```

---

## 🔮 Future Enhancements
* **Hardware Integration:** Replace `edge_simulator.py` with C++ code flashed to a physical ESP32 microcontroller reading an INA219 current sensor and GPS module.
* **Cloud Migration:** Replace the local Mosquitto broker with **Azure IoT Hub** and host the Digital Twin logic on **Azure Functions / Azure Digital Twins**.
* **Machine Learning:** Replace the mathematical prediction formulas with an ML model trained on historical flight degradation data.

lp making the GitHub repository!
