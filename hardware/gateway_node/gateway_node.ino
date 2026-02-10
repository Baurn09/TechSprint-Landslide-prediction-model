#include <LoRa.h>
#include <SPI.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"
#include <math.h>

MPU6050 accelgyro;

// --- PIN DEFINITIONS ---
const int SOIL_PIN = A0; // Connect the AO pin of soil sensor to A0 on Arduino

// Raw acceleration
int16_t ax, ay, az;
int16_t prev_ax = 0, prev_ay = 0, prev_az = 0;

// MPU6050 sensitivity (LSB/g for default ±2g)
const float ACCEL_SCALE = 16384.0;

// Calibration values for Soil Sensor (Adjust these based on testing)
const int AirValue = 600;   // Value in dry air
const int WaterValue = 250; // Value in a cup of water

void setup() {
    Wire.begin();
    Serial.begin(9600);

    accelgyro.initialize();

    if (!accelgyro.testConnection()) {
        Serial.println("MPU6050 FAIL");
    }

    LoRa.setPins(10, 9, 2);
    if (!LoRa.begin(433E6)) {
        Serial.println("Starting LoRa failed!");
        while (1) yield();
    }
    
    // Set pin mode for soil sensor
    pinMode(SOIL_PIN, INPUT);
    
    delay(1000); 
}

void loop() {
    // ---------------- SOIL MOISTURE READ ----------------
    int rawSoil = analogRead(SOIL_PIN);
    // Map the raw value to a 0-100% scale
    // Note: Most soil sensors are inverse (lower voltage = wetter)
    float soilMoisture = map(rawSoil, AirValue, WaterValue, 0, 100);
    
    // Constrain the value between 0 and 100
    if(soilMoisture > 100) soilMoisture = 100;
    if(soilMoisture < 0) soilMoisture = 0;

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

    float vibration = (dx + dy + dz) / 500.0;  

    prev_ax = ax;
    prev_ay = ay;
    prev_az = az;

    // ---------------- OUTPUTS ----------------
    // Format: soil,tilt,vibration
    Serial.print(soilMoisture, 1);
    Serial.print(","); Serial.print(tiltResultant, 3);
    Serial.print(","); Serial.println(vibration, 3);

    LoRa.beginPacket();
    LoRa.print(soilMoisture, 1); LoRa.print(",");
    LoRa.print(tiltResultant, 3); LoRa.print(",");
    LoRa.print(vibration, 3);
    
    int state = LoRa.endPacket();

    if (state == 1) {
        Serial.println(" -> Packet Sent Successfully!");
    } else {
        Serial.println(" -> Transmission Failed!");
    }

    delay(1000);
}