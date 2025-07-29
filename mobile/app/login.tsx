import React, {useState, useContext} from "react";
import { View, StyleSheet, Image, TextInput, TouchableHighlight, Text } from "react-native";
import { AuthContext } from "./utils/authContext";

export default function Login() {
    //() => authContext.logIn(cpf)
    const [cpf, setCpf] = useState('');
    const [senha, setSenha] = useState('');

    const handleEnvio = async () => {
        const url = 'http://localhost:5000/signin'

        let resultado = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({cpf:cpf, senha:senha})
        });

        if (resultado.ok) {
            resultado = await resultado.json()
            authContext.logIn(resultado.cpf, resultado.nome)
        };
    };

    const authContext = useContext(AuthContext);

    return (
        <View style={styles.bg}>
            <View style={styles.container}>
                <Image style={styles.logo} source={require('../assets/images/logotipo.png')} />

                <TextInput style={styles.input} placeholder="CPF" value={cpf} onChangeText={(text) => {setCpf(text)}} />
                
                <TextInput style={styles.input} placeholder="Senha" secureTextEntry={true} value={senha} onChangeText={(text) => {setSenha(text)}} />

                <TouchableHighlight style={styles.botao} onPress={handleEnvio}>
                    <Text style={styles.textoBotao}>ENTRAR</Text>
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
    logo: {
        width: '100%',
        height: 'undefined',
        aspectRatio: 1103/230,
        marginBottom: 16
    },
    input: {
        borderWidth: 1,
        marginBottom: 16,
        width: '100%',
        padding: 8,
        borderRadius: 32,
    },
    botao: {
        width: '100%',
        backgroundColor: '#F1D145',
        padding: 8,
        borderRadius: 32
    },
    textoBotao: {
        textAlign: 'center',
        fontWeight: 'bold'
    }
})