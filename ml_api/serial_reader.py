import serial
import threading
import time

# ---------------- CONFIG ----------------
=======
SERIAL_PORT = "COM6"          # 🔁 Change if needed
>>>>>>> a23f945d35499f454bf4ad023d94e3ac1dbf13de
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

            print(f"📡 RAW: '{line}'") # Added quotes to see hidden spaces

            # Use 'in' instead of 'startswith' to be safer
            if "Raw Data:" in line:
                try:
                    # Split by colon first, then take the second part
                    data_part = line.split(":")[-1].strip()
                    soil, tilt, vib = map(float, data_part.split(","))

                    latest_sensor_data["soil"] = soil
                    latest_sensor_data["tilt"] = tilt
                    latest_sensor_data["vibration"] = vib
                    
                except ValueError as e:
                    print(f"⚠️ Parse error: {e} in data: {line}")

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
