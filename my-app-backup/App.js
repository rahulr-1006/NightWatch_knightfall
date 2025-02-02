import React from "react";
import { View, Text, StyleSheet } from "react-native";
import useYOLODetection from "./hooks/useYOLODetection";

export default function App() {
  const detection = useYOLODetection();

  return (
    <View style={styles.container}>
      <Text style={styles.text}>
        {detection.person_detected ? `Person detected! (${detection.proximity})` : "No one detected"}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    fontSize: 20,
    fontWeight: "bold",
  },
});
