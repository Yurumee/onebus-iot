import React, {useContext} from "react";
import { Text, View, StyleSheet, Image, TouchableHighlight } from "react-native";
import { AuthContext } from "../utils/authContext";
import { useRouter } from "expo-router";

export default function Index() {
  const authContext = useContext(AuthContext);
  const router = useRouter();

  {/* ALTERAR */}
  const dadosUsuario = {
    nome: 'André Gustavo Silva Dantas'
  }

  return (
    <View style={styles.bg}>
      <View style={styles.container}>
        <Image style={styles.pfp} source={require('../../assets/images/pfp.jpg')} />

        <Text style={styles.nome}>{dadosUsuario.nome}</Text> {/* ALTERAR */}

        <TouchableHighlight style={styles.botaoMapa} onPress={() => {}}>
            <Text style={styles.textoBotao}>VER MAPA</Text>
        </TouchableHighlight>

        <TouchableHighlight underlayColor={'#C0C0C0'} style={styles.botao} onPress={() => router.replace('/motorista',{})}>
            <Text style={styles.textoBotao}>SELECIONAR MOTORISTA</Text>
        </TouchableHighlight>

        <TouchableHighlight underlayColor={'#C0C0C0'} style={styles.botao} onPress={() => {}}>
            <Text style={styles.textoBotao}>CONFIGURAÇÕES</Text>
        </TouchableHighlight>

        <TouchableHighlight underlayColor={'#C0C0C0'} style={styles.botao} onPress={() => {}}>
            <Text style={styles.textoBotao} onPress={authContext.logOut}>SAIR</Text>
        </TouchableHighlight>
      </View>
    </View>
  );
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
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32
  },
  pfp: {
    width: 100,
    height: 100,
    borderRadius: 100,
    marginBottom: 16
  },
  nome: {
    fontWeight: 'bold',
    marginBottom: 16
  },
  botaoMapa: {
    marginTop: 16,
    width: '100%',
    backgroundColor: '#F1D145',
    padding: 8,
    borderRadius: 32
  },
  botao: {
    marginTop: 16,
    width: '100%',
    backgroundColor: '#D0D0D0',
    padding: 8,
    borderRadius: 32
  },
  textoBotao: {
    textAlign: 'center',
    fontWeight: 'bold'
  }
})
