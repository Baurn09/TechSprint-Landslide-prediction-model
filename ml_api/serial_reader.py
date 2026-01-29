import serial
import threading
import time

SERIAL_PORT = "COM3"   # Windows example
# SERIAL_PORT = "/dev/ttyUSB0"  # Linux
BAUD_RATE = 9600

latest_sensor_data = {
    "soil": None,
    "tilt": None,
    "vibration": None
}

def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # allow Arduino reset
        print("✅ Arduino connected via USB")

        while True:
            line = ser.readline().decode().strip()
            if not line:
                continue

            try:
                soil, tilt, vib = map(float, line.split(","))
                latest_sensor_data["soil"] = soil
                latest_sensor_data["tilt"] = tilt
                latest_sensor_data["vibration"] = vib
            except ValueError:
                print("⚠️ Bad serial data:", line)

    except Exception as e:
        print("❌ Serial connection failed:", e)

def start_serial_thread():
    t = threading.Thread(target=read_serial, daemon=True)
    t.start()
