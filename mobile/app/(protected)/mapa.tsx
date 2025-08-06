import React, {useContext} from "react";
import { Text, View, StyleSheet, Image, TouchableHighlight } from "react-native";
import { AuthContext } from "../utils/authContext";
import { useRouter } from "expo-router";
import Map, { Marker, Polyline } from 'react-native-maps'

export default function Mapa() {
  const authContext = useContext(AuthContext);
  const router = useRouter();

  return (
    <View style={styles.container}>
        <Map
          style={StyleSheet.absoluteFill}
          initialRegion={{
            latitude: -6.263355590562354,
            longitude: -36.51601747810453,
            latitudeDelta: 0.005,
            longitudeDelta: 0.005
          }}
        >
          <Marker coordinate={{latitude: -6.263355590562354, longitude: -36.51601747810453}}/>
          <Polyline
            coordinates={[{latitude: -6.261005625698471, longitude: -36.51917365752614}, {latitude: -6.2598641808347, longitude: -36.52014332697427}]}
            strokeColor="#000"
            strokeWidth={6}
          />
        </Map>
    </View>
  );
};

const styles = StyleSheet.create({
    container: {
        flex: 1
    }
});