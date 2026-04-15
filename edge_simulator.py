import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883

throttle, speed, cooldown_timer = 0.0, 0.0, 0
temperature = 25.0
mission_type = 1 

HOME_LAT, HOME_LON = 17.3850, 78.4867
current_lat, current_lon = HOME_LAT, HOME_LON

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[EDGE] Connected. Listening for commands...")
    client.subscribe("drone/commands")

def on_message(client, userdata, msg):
    global throttle, cooldown_timer
    payload = json.loads(msg.payload.decode())
    
    # THE BUG FIX: Only accept emergency commands if we are actually flying!
    if payload.get("command") in ["THROTTLE_DOWN", "RETURN_TO_HOME"]:
        if throttle > 0.0: 
            print(f"\n🚨 [EDGE] {payload.get('command')} RECEIVED! Initiating emergency protocols!\n")
            throttle = 0.0 
            cooldown_timer = 0 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

print("[EDGE] Starting Multi-Mission Simulation...")
try:
    while True:
        if throttle == 0.0:
            # --- COOLDOWN PHASE ---
            cooldown_timer += 1
            speed = 0.0
            temperature = max(25.0, temperature - 5.0) 
            
            # Reset the GPS coordinates back to home while it cools down
            current_lat, current_lon = HOME_LAT, HOME_LON
            
            if cooldown_timer >= 4: 
                mission_type = (mission_type % 3) + 1 
                print(f"\n🔋 [EDGE] Recovered. Launching Mission Profile {mission_type}...\n")
                throttle = 10.0 
        else:
            # --- ACTIVE FLIGHT PHASE ---
            if throttle < 90:
                throttle += 5.0 
                
            # MISSION 1: Normal Flight -> Thermal Meltdown
            if mission_type == 1:
                speed = throttle * 0.4 
                temperature += (throttle * 0.1) 
                current_lat += (speed * 0.00001)
                current_lon += (speed * 0.00001)
                
            # MISSION 2: Hyper Speed -> Range Breach
            elif mission_type == 2:
                speed = throttle * 3.0 
                temperature += (throttle * 0.01) # Stays cool
                current_lat += (speed * 0.001) # Jumps kilometers instantly
                current_lon += (speed * 0.001)
                
            # MISSION 3: Hurricane Headwind -> Invisible Anomaly
            elif mission_type == 3:
                speed = throttle * 0.02 # Barely moving!
                temperature += (throttle * 0.05) 
                current_lat += (speed * 0.00001)
                current_lon += (speed * 0.00001)
                
        payload = {
            "throttle": round(throttle, 1),
            "temp": round(temperature, 1),
            "speed": round(speed, 1),
            "lat": round(current_lat, 5),
            "lon": round(current_lon, 5)
        }
        client.publish("drone/sensors", json.dumps(payload))
        time.sleep(1)
        
except KeyboardInterrupt:
    client.loop_stop()