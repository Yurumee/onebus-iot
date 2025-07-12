import React, {useContext} from "react";
import { Text, View, StyleSheet, TouchableHighlight, Image, FlatList, ScrollView } from "react-native";
import { AuthContext } from "../utils/authContext";
import { useRouter } from "expo-router";
import FontAwesome from '@expo/vector-icons/FontAwesome';

export default function Index() {
  const authContext = useContext(AuthContext);
  const router = useRouter();

  {/* ALTERAR */}
  const listaMotoristas = [
    {
        nomeCompleto: 'Umberto da Silva',
        CPF: '123.456.789-10'
    },
    {
        nomeCompleto: 'Doisberto da Silva',
        CPF: '024.681.012-14'
    }
  ]

  return (
    <View style={styles.bg}>
      <View style={styles.container}>
        <TouchableHighlight underlayColor={'#FFFFFF'} style={styles.fechar} onPress={() => router.replace('/',{})}>
          <FontAwesome name='close' size={28} />
        </TouchableHighlight>
        <Text style={styles.titulo}>SELECIONE SEU <Text style={styles.destaque}>MOTORISTA</Text></Text>
        <ScrollView style={styles.scroll}>
            <FlatList
              data={listaMotoristas}
              renderItem={({item}) => {
                return <>
                        <TouchableHighlight underlayColor={'#C0C0C0'} style={styles.motoristaCard} onPress={() => {authContext.escolherMotorista(item.CPF)}}>
                            <View style={styles.cardContainer}>
                                <Image style={styles.pfp} source={require('../../assets/images/pfp.jpg')} />
                                <View>
                                    <Text>{item.nomeCompleto}</Text> {/* ALTERAR */}
                                    <Text>{item.CPF}</Text> {/* ALTERAR */}
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
  motoristaCard: {
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