import serial
import threading
import time

# 🔥 SHARED SENSOR STATE (DO NOT REASSIGN THIS)
latest_sensor_data = {
    "soil": None,
    "tilt": None,
    "vibration": None
}

def start_serial_thread():
    t = threading.Thread(target=read_serial, daemon=True)
    t.start()
    print("🚀 Serial thread started")

def read_serial():
    try:
        # 🔧 CHANGE COM PORT IF NEEDED
        ser = serial.Serial("COM5", 9600, timeout=1)
        time.sleep(2)  # allow Arduino to reset
        print("✅ Serial port opened")
    except Exception as e:
        print("❌ Failed to open serial port:", e)
        return

    while True:
        try:
            line = ser.readline().decode("utf-8").strip()
            if not line:
                continue

            # EXPECTED FORMAT: soil,tilt,vibration
            # Example: 56.2,0.031,1.84
            parts = line.split(",")

            if len(parts) != 3:
                print("⚠️ Invalid serial format:", line)
                continue

            soil = float(parts[0])
            tilt = float(parts[1])
            vib  = float(parts[2])

            # ✅ UPDATE (NOT reassignment)
            latest_sensor_data["soil"] = soil
            latest_sensor_data["tilt"] = tilt
            latest_sensor_data["vibration"] = vib

            # 🔍 DEBUG (CONFIRM DATA FLOW)
            print("📡 SENSOR:", latest_sensor_data)

        except Exception as e:
            print("❌ Serial read error:", e)