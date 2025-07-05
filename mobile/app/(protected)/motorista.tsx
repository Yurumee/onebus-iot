import React, {useContext} from "react";
import { Text, View, StyleSheet, TouchableHighlight, Image, FlatList } from "react-native";
import { AuthContext } from "../utils/authContext";

export default function Index() {
  const authContext = useContext(AuthContext);

  {/* ALTERAR */}
  const listaMotoristas = [
    {
        nome: 'Umberto da Silva',
        cpf: '123.456.789-10'
    },
    {
        nome: 'Doisberto da Silva',
        cpf: '024.681.012-14'
    }
  ]

  return (
    <View style={styles.bg}>
        <View style={styles.container}>
            <Text style={styles.titulo}>SELECIONE SEU MOTORISTA</Text>
            <FlatList
              data={listaMotoristas}
              renderItem={({item}) => {
                return <>
                        <TouchableHighlight underlayColor={'#C0C0C0'} style={styles.motoristaCard} onPress={() => {}}>
                            <View style={styles.cardContainer}>
                                <Image style={styles.pfp} source={require('../../assets/images/pfp.jpg')} />
                                <View>
                                    <Text>{item.nome}</Text> {/* ALTERAR */}
                                    <Text>{item.cpf}</Text> {/* ALTERAR */}
                                </View>
                            </View>
                        </TouchableHighlight>
                      </>
              }}
            />
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
  container: {
    width: '100%',
    maxWidth: 500,
    height: '100%',
    backgroundColor: '#FFFFFF',
    padding: 32
  },
  titulo: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
    textAlign: 'center'
  },
  motoristaCard: {
    marginTop: 16,
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