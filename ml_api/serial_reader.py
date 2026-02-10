import serial
import threading
import time

# ---------------- CONFIG ----------------
SERIAL_PORT = "COM3"          # 🔁 Change if needed
BAUD_RATE = 115200            # MUST match Serial.begin()
# ----------------------------------------

latest_sensor_data = {
    "soil": None,
    "tilt": None,
    "vibration": None
}

def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # allow board reset
        print("✅ Device connected on", SERIAL_PORT)

        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            # 🔎 Debug: see everything coming from Arduino
            print("📡 RAW:", line)

            # Expected format:
            # Raw Data: soil,tilt,vibration
            if line.startswith("Raw Data:"):
                data = line.replace("Raw Data:", "").strip()

                try:
                    soil, tilt, vib = map(float, data.split(","))

                    latest_sensor_data["soil"] = soil
                    latest_sensor_data["tilt"] = tilt
                    latest_sensor_data["vibration"] = vib

                    print("📥 Parsed:", latest_sensor_data)

                except ValueError:
                    print("⚠️ Parse failed →", data)

    except serial.SerialException as e:
        print("❌ Serial error:", e)

    except Exception as e:
        print("❌ Unexpected error:", e)

def start_serial_thread():
    t = threading.Thread(target=read_serial, daemon=True)
    t.start()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    start_serial_thread()
    while True:
        time.sleep(1)
