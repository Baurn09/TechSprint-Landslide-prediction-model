#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"
#include <math.h>

MPU6050 accelgyro;

// Raw acceleration
int16_t ax, ay, az;
int16_t prev_ax = 0, prev_ay = 0, prev_az = 0;

// MPU6050 sensitivity (LSB/g for default ±2g)
const float ACCEL_SCALE = 16384.0;

// 🔥 Placeholder soil moisture (since sensor not available)
const float SOIL_PLACEHOLDER = 50.0;

void setup() {
    Wire.begin();
    Serial.begin(9600);

    accelgyro.initialize();

    if (!accelgyro.testConnection()) {
        Serial.println("MPU6050 FAIL");
    }

    delay(1000); // allow sensor to stabilize
}

void loop() {
    // ---------------- MPU6050 READ ----------------
    accelgyro.getAcceleration(&ax, &ay, &az);

    // Convert to g-force
    float axg = ax / ACCEL_SCALE;
    float ayg = ay / ACCEL_SCALE;
    float azg = az / ACCEL_SCALE;

    // ---------------- TILT CALCULATION ----------------
    float tiltX = atan2(ayg, azg) * 180.0 / M_PI;
    float tiltY = atan2(axg, azg) * 180.0 / M_PI;
    float tiltResultant = sqrt(tiltX * tiltX + tiltY * tiltY);

    // ---------------- VIBRATION CALCULATION ----------------
    long dx = abs(ax - prev_ax);
    long dy = abs(ay - prev_ay);
    long dz = abs(az - prev_az);

    float vibration = (dx + dy + dz) / 500.0;  // scaled for stability

    prev_ax = ax;
    prev_ay = ay;
    prev_az = az;

    // ---------------- SERIAL OUTPUT (STRICT FORMAT) ----------------
    // soil,tilt,vibration
    Serial.print(SOIL_PLACEHOLDER, 1);
    Serial.print(",");
    Serial.print(tiltResultant, 3);
    Serial.print(",");
    Serial.println(vibration, 3);

    // 2 samples per second
    delay(100);
}