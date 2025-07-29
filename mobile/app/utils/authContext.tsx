import { useRouter } from "expo-router";
import { createContext, PropsWithChildren, useEffect, useState } from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

type AuthState = {
    isLoggedIn: boolean,
    isReady: boolean,
    cpf: any,
    nome: any,
    trajetoId: any,
    logIn: (cpf:any, nome:any) => void,
    logOut: () => void,
    escolherTrajeto: (trajetoId:any) => void
};

const authStorageKey = 'auth-key';
const trajetoStorageKey = 'trajeto-key';

export const AuthContext = createContext<AuthState>({
    isLoggedIn: false,
    isReady: false,
    cpf: '',
    nome: '',
    trajetoId: '',
    logIn: (cpf:any, nome:any) => {},
    logOut: () => {},
    escolherTrajeto: (trajetoId:any) => {}
});

export function AuthProvider({ children }: PropsWithChildren) {
    const [isReady, setIsReady] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [cpf, setCpf] = useState('');
    const [nome, setNome] = useState('');
    const [trajetoId, setTrajetoId] = useState('');
    const router = useRouter();

    const storeAuthState = async (newState: {isLoggedIn: boolean, cpf: any, nome: any}) => {
        try {
            const jsonValue = JSON.stringify(newState);
            await AsyncStorage.setItem(authStorageKey, jsonValue);
        } catch (error) {
            console.log('Error saving.', error);
        };
    };

    const storeTrajetoId = async (newState: {trajetoId: any}) => {
        try {
            const jsonValue = JSON.stringify(newState);
            await AsyncStorage.setItem(trajetoStorageKey, jsonValue);
        } catch (error) {
            console.log('Error saving.', error);
        }
    };

    const deleteAuthState = async () => {
        try {
            await AsyncStorage.removeItem(authStorageKey);
            await AsyncStorage.removeItem(trajetoStorageKey);
        } catch (error) {
            console.log('Error deleting.', error);
        }
    }

    const logIn = (cpf:any, nome:any) => {
        setIsLoggedIn(true);
        setCpf(cpf);
        setNome(nome);
        storeAuthState({ isLoggedIn: true, cpf: cpf, nome: nome });
        router.replace('/',{});
    };

    const logOut = async () => {
        setIsLoggedIn(false);
        setTrajetoId('')
        deleteAuthState();
        router.replace('/login');
    };

    const escolherTrajeto = (trajetoId:any) => {
        setTrajetoId(trajetoId);
        storeTrajetoId({trajetoId: trajetoId});
        router.replace('/',{});
    };

    useEffect(() => {
        const getAuthFromStorage = async () => {
            try {
                const value = await AsyncStorage.getItem(authStorageKey);
                const valueTrajeto = await AsyncStorage.getItem(trajetoStorageKey);
                if (value !== null) {
                    const auth = JSON.parse(value);
                    setIsLoggedIn(auth.isLoggedIn);
                    setCpf(auth.cpf);
                    setNome(auth.nome);
                };
                if (valueTrajeto !== null) {
                    const auth = JSON.parse(valueTrajeto);
                    setTrajetoId(auth.trajetoId)
                };
            } catch (error) {
                console.log('Error fetching from storage.', error);
            };
            setIsReady(true);
        };
        getAuthFromStorage();
    }, []);

    return (
        <AuthContext.Provider value={{ isLoggedIn, isReady, cpf, nome, trajetoId, logIn, logOut, escolherTrajeto }}>
            {children}
        </AuthContext.Provider>
    );
}