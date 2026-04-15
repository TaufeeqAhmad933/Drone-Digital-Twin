import json
import paho.mqtt.client as mqtt
from math import radians, cos, sin, asin, sqrt

BROKER = "127.0.0.1"
PORT = 1883

HOME_LAT, HOME_LON = 17.3850, 78.4867

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    a = sin((lat2 - lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1)/2)**2
    return 2 * asin(sqrt(a)) * 6371 

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[TWIN] Online. Monitoring flight dynamics...")
    client.subscribe("drone/sensors")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    current_temp = data.get("temp")
    current_throttle = data.get("throttle")
    speed = data.get("speed")
    lat, lon = data.get("lat"), data.get("lon")

    # Adjusted prediction math to be slightly more realistic
    predicted_temp = current_temp + (current_throttle * 0.02 * 30)
    distance_from_home_km = haversine(HOME_LON, HOME_LAT, lon, lat)
    
    # Set a strict 2.0 km safe range for the demo
    safe_range_km = 2.0 

    # Anomaly Logic
    expected_speed = current_throttle * 0.4
    wind_anomaly = (current_throttle > 30) and (speed < expected_speed * 0.2)

    status = "STATUS: NORMAL"
    
    # Priority 1: Wind Anomaly
    if wind_anomaly:
        status = "WARNING: INVISIBLE ANOMALY (HEAVY HEADWIND)"
        print("⚠️ [TWIN] ANOMALY DETECTED. Sending RTH.")
        client.publish("drone/commands", json.dumps({"command": "RETURN_TO_HOME"}))
        
    # Priority 2: Range Breach
    elif distance_from_home_km > safe_range_km:
        status = "CRITICAL: INSUFFICIENT ENERGY! FORCING RTH NOW."
        print(f"⚠️ [TWIN] RANGE BREACH! Dist: {round(distance_from_home_km,2)}km")
        client.publish("drone/commands", json.dumps({"command": "RETURN_TO_HOME"}))
        
    # Priority 3: Thermal Meltdown
    elif predicted_temp > 45.0:
        status = "DANGER: MELTDOWN IMMINENT"
        print(f"⚠️ [TWIN] THERMAL BREACH! Future temp {round(predicted_temp,1)}C.")
        client.publish("drone/commands", json.dumps({"command": "THROTTLE_DOWN"}))

    twin_data = {
        "predicted_temp": round(predicted_temp, 1),
        "distance_km": round(distance_from_home_km, 2),
        "safe_range_km": round(safe_range_km, 2),
        "status": status
    }
    client.publish("drone/twin/analytics", json.dumps(twin_data))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()