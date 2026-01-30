"""
Learns normal sensor behavior AFTER deployment.
No dataset required.
"""

import numpy as np
from collections import deque

WINDOW = 120

soil_buf = deque(maxlen=WINDOW)
tilt_buf = deque(maxlen=WINDOW)
vib_buf = deque(maxlen=WINDOW)

def update_baseline(soil, tilt, vib):
    soil_buf.append(soil)
    tilt_buf.append(tilt)
    vib_buf.append(vib)

    if len(soil_buf) < WINDOW:
        return None

    return {
        "soil_mean": np.mean(soil_buf),
        "soil_std": np.std(soil_buf),
        "tilt_mean": np.mean(tilt_buf),
        "tilt_std": np.std(tilt_buf),
        "vib_mean": np.mean(vib_buf),
        "vib_std": np.std(vib_buf)
    }
