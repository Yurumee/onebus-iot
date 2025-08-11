import React, { useState, useContext, useEffect } from "react";
import { Text, View, StyleSheet, TouchableHighlight, Image, FlatList, ScrollView } from "react-native";
import { AuthContext } from "../utils/authContext";
import { useRouter } from "expo-router";
import FontAwesome from '@expo/vector-icons/FontAwesome';

export default function Index() {
  const authContext = useContext(AuthContext);
  const router = useRouter();
  const [listaTrajetos, setListaTrajetos] = useState([]);

  const handleTrajetos = async () => {
    const url = 'http://localhost:5000/cidadao/trajetos'

    let resultado = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({'cidadao-cpf':authContext.cpf})
    });

    if (resultado.ok) {
        resultado = await resultado.json()
        setListaTrajetos(Object.values(resultado.trajetos))
    };
  };

  useEffect(() => {
    handleTrajetos()
  }, [])

  return (
    <View style={styles.bg}>
      <View style={styles.container}>
        {/* ALTERAR onPress para remover o trajeto do contexto */}
        <TouchableHighlight underlayColor={'#FFFFFF'} style={styles.fechar} onPress={() => router.replace('/',{})}>
          <FontAwesome name='close' size={28} />
        </TouchableHighlight>
        <Text style={styles.titulo}>SELECIONE SEU <Text style={styles.destaque}>TRAJETO</Text></Text>
        <ScrollView style={styles.scroll}>
            <FlatList
              data={listaTrajetos}
              renderItem={({item}) => {
                return <>
                        <TouchableHighlight underlayColor={'#C0C0C0'} style={styles.trajetoCard} onPress={() => {authContext.escolherTrajeto(item.trajeto_id, item.carro_placa)}}>
                            <View style={styles.cardContainer}>
                                <Image style={styles.pfp} source={require('../../assets/images/pfp.jpg')} />
                                <View>
                                    <Text>Origem: {item.ponto_origem}</Text> {/* ALTERAR */}
                                    <Text>Destino: {item.ponto_destino}</Text> {/* ALTERAR */}
                                    <Text>Placa do veículo: {item.carro_placa}</Text> {/* ALTERAR */}
                                </View>
                            </View>
                        </TouchableHighlight>
                      </>
              }}
            />
            
        </ScrollView>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  bg: {
    backgroundColor: '#FFFFFF',
    height: '100%',
    width: '100%',
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  scroll: {
    width: '100%'
  },
  container: {
    width: '100%',
    maxWidth: 500,
    height: '100%',
    backgroundColor: '#FFFFFF',
    padding: 32
  },
  fechar: {
    position: 'fixed',
    zIndex: 1,
    left: 16,
    top: 16
  },
  titulo: {
    fontSize: 20,
    fontWeight: 'bold',
    paddingBottom: 32,
    textAlign: 'center'
  },
  destaque: {
    color: '#F1D145'
  },
  trajetoCard: {
    marginBottom: 16,
    width: '100%',
    backgroundColor: '#D0D0D0',
    borderRadius: 8
  },
  cardContainer: {
    padding: 8,
    borderRadius: 32,
    flex: 1,
    flexDirection: 'row',
    gap: 8
  },
  pfp: {
    width: 64,
    height: 64,
    borderRadius: 64
  }
})