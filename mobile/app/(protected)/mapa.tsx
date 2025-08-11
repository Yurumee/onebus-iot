import React, {useContext, useEffect, useState} from "react";
import { Text, View, StyleSheet, Image, TouchableHighlight } from "react-native";
import { AuthContext } from "../utils/authContext";
import { useRouter } from "expo-router";
import Map, { Marker, Polyline } from 'react-native-maps'
import useLocation from "@/hooks/useLocation";

export default function Mapa() {
  const {latitude, longitude, errorMsg} = useLocation();
  const authContext = useContext(AuthContext);
  const router = useRouter();
  const [carroLatitude, setCarroLatitude] = useState(0);
  const [carroLongitude, setCarroLongitude] = useState(0);

  const handleCarro = async () => {
    const url = 'http://localhost:5000/carro/carro-especifico'
  
    let resultado = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({'placa-carro':authContext.carroId})
    });
  
    if (resultado.ok) {
        resultado = await resultado.json()
        setCarroLatitude(parseFloat(resultado.resposta_json["latitude atual"]))
        setCarroLongitude(parseFloat(resultado.resposta_json["longitude atual"]))
    };
  };

  const MINUTE_MS = 60000;

  useEffect(() => {
    handleCarro();
    const interval = setInterval(() => {
      handleCarro();
    }, MINUTE_MS);

    return () => clearInterval(interval);
  }, [])

  return (
    <View style={styles.container}>
        <TouchableHighlight underlayColor={'#FFFFFF'} style={styles.botaoHome} onPress={() => router.replace('/',{})}>
          <Image style={styles.home} source={require('../../assets/images/onebus-home.png')} />
        </TouchableHighlight>
        <Map
          style={StyleSheet.absoluteFill}
          initialRegion={{
            latitude: -6.262140,
            longitude: -36.514332,
            latitudeDelta: 0.02,
            longitudeDelta: 0.02
          }}
        >
          <Marker pinColor={"navy"} coordinate={{latitude: latitude, longitude: longitude}}/>
          <Marker pinColor={"yellow"} coordinate={{latitude: carroLatitude, longitude: carroLongitude}}/>
          <Polyline
            coordinates={[{latitude: -6.261005625698471, longitude: -36.51917365752614}, {latitude: -6.2598641808347, longitude: -36.52014332697427}]}
            strokeColor="#000"
            strokeWidth={4}
          /> {/* Teste */}
        </Map>
    </View>
  );
};

const styles = StyleSheet.create({
    container: {
        flex: 1
    },
    botaoHome: {
        position: 'absolute',
        zIndex: 1,
        left: 16,
        top: 32,
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        width: 64,
        height: 64,
        backgroundColor: '#FFFFFF',
        borderRadius: 64
    },
    home: {
        width: 50,
        height: 33
    }
});