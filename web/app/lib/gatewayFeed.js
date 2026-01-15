import { sensorRegistry } from "./sensorRegistry";

export function generateGatewayFeed() {
  return Object.entries(sensorRegistry).map(
    ([sensorId, meta]) => {
      const riskRoll = Math.random();

      let risk = "SAFE";
      if (riskRoll > 0.85) risk = "CRITICAL";
      else if (riskRoll > 0.65) risk = "WARNING";

      return {
        sensorId,
        area: meta.area,
        lat: meta.lat,
        lng: meta.lng,
        risk,
        soilMoisture: Math.floor(50 + Math.random() * 40),
        motion: Number(Math.random().toFixed(3)),
        lastSeen: `${Math.floor(Math.random() * 20)}s ago`,
      };
    }
  );
}
