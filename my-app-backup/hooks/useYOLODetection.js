import { useEffect, useState } from "react";
import { Audio } from "expo-av";

const useYOLODetection = () => {
  const [detection, setDetection] = useState({ person_detected: false, proximity: "none" });

  useEffect(() => {
    const socket = new WebSocket("ws://192.168.1.100:8000"); // Change to local server IP

    socket.onopen = () => console.log("✅ WebSocket connected");
    socket.onmessage = async (event) => {
      const data = JSON.parse(event.data);
      console.log("📡 YOLO Data:", data);
      setDetection(data);

      if (data.person_detected) {
        const { proximity } = data;
        const sound = new Audio.Sound();
        await sound.loadAsync(require("../assets/beep.mp3"));

        if (proximity === "far") {
          await sound.playAsync();
        } else if (proximity === "close") {
          await sound.playAsync();
          setTimeout(() => sound.playAsync(), 500);
        } else if (proximity === "very_close") {
          await sound.playAsync();
          setTimeout(() => sound.playAsync(), 300);
          setTimeout(() => sound.playAsync(), 600);
        }
      }
    };

    socket.onerror = (error) => console.log("❌ WebSocket Error:", error);
    socket.onclose = () => console.log("🔌 WebSocket Disconnected");

    return () => socket.close();
  }, []);

  return detection;
};

export default useYOLODetection;
