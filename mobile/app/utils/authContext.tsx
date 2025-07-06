import { useRouter } from "expo-router";
import { createContext, PropsWithChildren, useEffect, useState } from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';

type AuthState = {
    isLoggedIn: boolean,
    isReady: boolean,
    cpf: any,
    motoristaCpf: any,
    logIn: (cpf:any) => void,
    logOut: () => void,
    escolherMotorista: (motoristaCpf:any) => void
};

const authStorageKey = 'auth-key';
const motoristaStorageKey = 'motorista-key';

export const AuthContext = createContext<AuthState>({
    isLoggedIn: false,
    isReady: false,
    cpf: '',
    motoristaCpf: '',
    logIn: (cpf:any) => {},
    logOut: () => {},
    escolherMotorista: (motoristaCpf:any) => {}
});

export function AuthProvider({ children }: PropsWithChildren) {
    const [isReady, setIsReady] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [cpf, setCpf] = useState('');
    const [motoristaCpf, setMotoristaCpf] = useState({});
    const router = useRouter();

    const storeAuthState = async (newState: {isLoggedIn: boolean, cpf: any}) => {
        try {
            const jsonValue = JSON.stringify(newState);
            await AsyncStorage.setItem(authStorageKey, jsonValue);
        } catch (error) {
            console.log('Error saving.', error);
        };
    };

    const storeMotoristaCpf = async (newState: {motoristaCpf: any}) => {
        try {
            const jsonValue = JSON.stringify(newState);
            await AsyncStorage.setItem(motoristaStorageKey, jsonValue);
        } catch (error) {
            console.log('Error saving.', error);
        }
    };

    const deleteAuthState = async () => {
        try {
            await AsyncStorage.removeItem(authStorageKey);
            await AsyncStorage.removeItem(motoristaStorageKey);
        } catch (error) {
            console.log('Error deleting.', error);
        }
    }

    const logIn = (cpf:any) => {
        setIsLoggedIn(true);
        setCpf(cpf);
        storeAuthState({ isLoggedIn: true, cpf: cpf });
        router.replace('/',{});
    };

    const logOut = () => {
        setIsLoggedIn(false);
        deleteAuthState()
        router.replace('/login');
    };

    const escolherMotorista = (motoristaCpf:any) => {
        setMotoristaCpf(motoristaCpf);
        storeMotoristaCpf({motoristaCpf: motoristaCpf});
        router.replace('/',{});
    };

    useEffect(() => {
        const getAuthFromStorage = async () => {
            try {
                const value = await AsyncStorage.getItem(authStorageKey);
                const valueMotorista = await AsyncStorage.getItem(motoristaStorageKey);
                if (value !== null) {
                    const auth = JSON.parse(value);
                    setIsLoggedIn(auth.isLoggedIn);
                    setCpf(auth.cpf);
                };
                if (valueMotorista !== null) {
                    const auth = JSON.parse(valueMotorista);
                    setMotoristaCpf(auth.motoristaCpf)
                };
            } catch (error) {
                console.log('Error fetching from storage.', error);
            };
            setIsReady(true);
        };
        getAuthFromStorage();
    }, []);

    return (
        <AuthContext.Provider value={{ isLoggedIn, isReady, cpf, motoristaCpf, logIn, logOut, escolherMotorista }}>
            {children}
        </AuthContext.Provider>
    );
}