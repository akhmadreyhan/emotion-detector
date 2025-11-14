navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    console.log("Video input devices:");
    devices.forEach(device => {
      if (device.kind === "videoinput") {
        console.log(device.label || "Unnamed camera", device.deviceId);
      }
    });
  })
  .catch(err => {
    console.error("enumerateDevices() failed:", err);
  });
