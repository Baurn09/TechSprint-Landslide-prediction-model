"""
Injects artificial landslide patterns to test detection.
Not used in production.
"""

def inject_event(sensor_stream, start, duration):
    for i in range(start, start + duration):
        sensor_stream[i]["soil"] += 0.08
        sensor_stream[i]["tilt"] += 0.25
        sensor_stream[i]["vibration"] += 2.0
