import serial
import threading
import time

SERIAL_PORT = "COM3"          # Windows example
# SERIAL_PORT = "/dev/ttyUSB0"  # Linux
BAUD_RATE = 115200            # ✅ MUST match ESP32 Serial.begin()

latest_sensor_data = {
    "soil": None,
    "tilt": None,
    "vibration": None
}

def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # allow ESP32 reset
        print("✅ ESP32 connected via USB")

        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue

            # ESP32 sends: "Raw Data: soil,tilt,vibration"
            if line.startswith("Raw Data:"):
                try:
                    data = line.replace("Raw Data:", "").strip()
                    soil, tilt, vib = map(float, data.split(","))

                    latest_sensor_data["soil"] = soil
                    latest_sensor_data["tilt"] = tilt
                    latest_sensor_data["vibration"] = vib

                    print("📥 Updated:", latest_sensor_data)

                except ValueError:
                    print("⚠️ Bad sensor data:", line)

    except Exception as e:
        print("❌ Serial connection failed:", e)

def start_serial_thread():
    t = threading.Thread(target=read_serial, daemon=True)
    t.start()