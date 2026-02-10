#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include <math.h>

// ---------------- MPU6050 ----------------
MPU6050 accelgyro;

// ---------------- PIN DEFINITIONS ----------------
const int SOIL_PIN = A0;   // Soil sensor analog pin

// LoRa pins (Arduino Uno / Nano example)
#define LORA_SS   10
#define LORA_RST  9
#define LORA_DIO0 2

// ---------------- ACCEL DATA ----------------
int16_t ax, ay, az;
int16_t prev_ax = 0, prev_ay = 0, prev_az = 0;

// MPU6050 sensitivity (±2g)
const float ACCEL_SCALE = 16384.0;

// ---------------- SOIL CALIBRATION ----------------
const int AirValue   = 600;   // dry
const int WaterValue = 250;   // wet

void setup() {
  Wire.begin();
  Serial.begin(115200);     // ✅ MATCHES PYTHON
  delay(2000);

  // ---- MPU6050 ----
  accelgyro.initialize();
  if (!accelgyro.testConnection()) {
    Serial.println("MPU6050 FAIL");
  } else {
    Serial.println("MPU6050 OK");
  }

  // ---- LoRa ----
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed");
    while (1);
  }
  Serial.println("LoRa OK");

  pinMode(SOIL_PIN, INPUT);
}

void loop() {

  // -------- SOIL MOISTURE --------
  int rawSoil = analogRead(SOIL_PIN);
  float soilMoisture = map(rawSoil, AirValue, WaterValue, 0, 100);
  soilMoisture = constrain(soilMoisture, 0, 100);

  // -------- MPU6050 --------
  accelgyro.getAcceleration(&ax, &ay, &az);

  float axg = ax / ACCEL_SCALE;
  float ayg = ay / ACCEL_SCALE;
  float azg = az / ACCEL_SCALE;

  // -------- TILT --------
  float tiltX = atan2(ayg, azg) * 180.0 / M_PI;
  float tiltY = atan2(axg, azg) * 180.0 / M_PI;
  float tiltResultant = sqrt(tiltX * tiltX + tiltY * tiltY);

  // -------- VIBRATION --------
  long dx = abs(ax - prev_ax);
  long dy = abs(ay - prev_ay);
  long dz = abs(az - prev_az);
  float vibration = (dx + dy + dz) / 500.0;

  prev_ax = ax;
  prev_ay = ay;
  prev_az = az;

  // -------- SERIAL OUTPUT (MATCHED FORMAT) --------
  // Raw Data: soil,tilt,vibration
  Serial.print("Raw Data: ");
  Serial.print(soilMoisture, 1);
  Serial.print(",");
  Serial.print(tiltResultant, 3);
  Serial.print(",");
  Serial.println(vibration, 3);

  // -------- LORA TRANSMIT --------
  LoRa.beginPacket();
  LoRa.print(soilMoisture, 1);
  LoRa.print(",");
  LoRa.print(tiltResultant, 3);
  LoRa.print(",");
  LoRa.print(vibration, 3);
  LoRa.endPacket();

  delay(1000);
}
