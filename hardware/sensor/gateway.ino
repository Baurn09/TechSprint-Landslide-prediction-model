#include <SPI.h>
#include <LoRa.h>

// Define pins for ESP32
#define ss 5
#define rst 14
#define dio0 26

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("LoRa Receiver Starting...");

  // Override the default LoRa pins for ESP32
  LoRa.setPins(ss, rst, dio0);

  // Use the same frequency as your transmitter (433E6)
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  
  Serial.println("LoRa Initialized OK!");
}

void loop() {
  // Try to parse packet
  int packetSize = LoRa.parsePacket();
  
  if (packetSize) {
    // Received a packet
    String incoming = "";

    while (LoRa.available()) {
      incoming += (char)LoRa.read();
    }

    // Print raw data and signal strength (RSSI)
    Serial.print("Raw Data: ");
    Serial.println(incoming);
    //Serial.print("RSSI: ");
    //Serial.println(LoRa.packetRssi());

    // --- Parsing the comma-separated data ---
    // Format sent: "soil,tilt,vibration"
    int firstComma = incoming.indexOf(',');
    int secondComma = incoming.indexOf(',', firstComma + 1);

    if (firstComma != -1 && secondComma != -1) {
      String soil = incoming.substring(0, firstComma);
      String tilt = incoming.substring(firstComma + 1, secondComma);
      
      String vib = incoming.substring(secondComma + 1);

      //Serial.println("--- Decoded Data ---");
      //Serial.println("Soil Moisture: " + soil + "%");
      //Serial.println("Tilt Angle: " + tilt + "°");
      //Serial.println("Vibration: " + vib);
      //Serial.println("--------------------");
    }
  }
}