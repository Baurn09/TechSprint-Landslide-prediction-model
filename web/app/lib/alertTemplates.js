export function getAlertMessage(level, area) {
  const time = new Date().toLocaleString();

  if (level === "CRITICAL") {
    return {
      title: "EMERGENCY ALERT – LANDSLIDE RISK",
      body: `
        Location: ${area.toUpperCase()}
        Time: ${time}

        Severe landslide risk detected due to heavy rainfall and ground instability.

        Move away from steep slopes immediately.
        Avoid hill roads.
        Follow instructions from local authorities.
            `,
    };
  }

  if (level === "WARNING") {
    return {
      title: "WARNING – POTENTIAL LANDSLIDE",
      body: `
        Location: ${area.toUpperCase()}
        Time: ${time}

        High rainfall and soil saturation detected.
        Ground movement under observation.

        Prepare for possible evacuation.
        Avoid unnecessary travel near slopes.
            `,
    };
  }

  return null;
}
