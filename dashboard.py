import streamlit as st
import paho.mqtt.client as mqtt
import json
import time
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Geospatial Digital Twin", layout="wide")
st.title("🚁 Multi-Mission Digital Twin Dashboard")

@st.cache_resource
def get_data_store():
    return {
        'throttle': 0, 'temp': 25, 'speed': 0, 
        'lat': 17.3850, 'lon': 78.4867, 
        'pred_temp': 25, 'dist_km': 0.0, 'safe_range': 2.0,
        'status': 'WAITING FOR DATA...'
    }

latest_data = get_data_store()

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    if msg.topic == "drone/sensors":
        for key in ['throttle', 'temp', 'speed', 'lat', 'lon']:
            latest_data[key] = payload.get(key, latest_data[key])
    elif msg.topic == "drone/twin/analytics":
        latest_data['pred_temp'] = payload.get('predicted_temp', 25)
        latest_data['dist_km'] = payload.get('distance_km', 0.0)
        latest_data['safe_range'] = payload.get('safe_range_km', 2.0)
        latest_data['status'] = payload.get('status', "UNKNOWN")

@st.cache_resource
def get_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    client.subscribe("drone/sensors")
    client.subscribe("drone/twin/analytics")
    client.loop_start()
    return client

get_mqtt_client()

st.subheader("Physical Hardware Telemetry")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Current Throttle", f"{latest_data['throttle']} %")
col2.metric("Physical Temp", f"{latest_data['temp']} °C")
col3.metric("Ground Speed", f"{latest_data['speed']} m/s")
col4.metric("Latitude", f"{latest_data['lat']}")
col5.metric("Longitude", f"{latest_data['lon']}")

st.divider()

col_map, col_twin = st.columns([2, 1])

with col_map:
    st.subheader("Live Radar")
    
    # ---------------------------------------------------------
    # UPGRADED MAP WITH FOLIUM (Custom Drone Icon!)
    # ---------------------------------------------------------
    # 1. Create a map centered exactly on the drone's coordinates
    m = folium.Map(location=[latest_data['lat'], latest_data['lon']], zoom_start=15)
    
    # 2. Inject a custom HTML Div containing a Drone Emoji
    folium.Marker(
        [latest_data['lat'], latest_data['lon']],
        tooltip="Drone Alpha-1",
        icon=folium.DivIcon(html=f'<div style="font-size: 32px; transform: translate(-50%, -50%);">🚁</div>')
    ).add_to(m)

    # 3. Render the Folium map inside Streamlit
    st_folium(m, width=800, height=400, returned_objects=[])
    # ---------------------------------------------------------

with col_twin:
    st.subheader("Digital Twin Analytics")
    st.metric("Predicted Temp (30s)", f"{latest_data['pred_temp']} °C")
    st.metric("Distance from Base", f"{latest_data['dist_km']} km")
    st.metric("Static Safe Range", f"{latest_data['safe_range']} km")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    status = latest_data['status']
    if "NORMAL" in status:
        st.success(status)
    elif "WARNING" in status:
        st.warning(status) 
    elif "DANGER" in status or "CRITICAL" in status:
        st.error(status) 
    else:
        st.info(status)

time.sleep(1)
st.rerun()