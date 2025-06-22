import React, {useState, useContext} from "react";
import { View, StyleSheet, Image, TextInput, TouchableHighlight, Text } from "react-native";
import { AuthContext } from "./utils/authContext";

export default function Login() {
    const [cpf, setCpf] = useState('');
    const [senha, setSenha] = useState('');
    const inputCpf = (event:any) => {
        setCpf(event.target.value)
    };
    const inputSenha = (event:any) => {
        setSenha(event.target.value)
    };

    const authContext = useContext(AuthContext);

    return (
        <View style={styles.bg}>
            <View style={styles.container}>
                <Image style={styles.logo} source={require('../assets/images/logotipo.png')} />

                <TextInput style={styles.input} placeholder="CPF" value={cpf} onChange={inputCpf} />
                
                <TextInput style={styles.input} placeholder="Senha" secureTextEntry={true} value={senha} onChange={inputSenha} />

                <TouchableHighlight style={styles.botao} onPress={authContext.logIn}>
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