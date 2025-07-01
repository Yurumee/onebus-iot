import { useRouter } from "expo-router";
import { createContext, PropsWithChildren, useEffect, useState } from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';

type AuthState = {
    isLoggedIn: boolean,
    isReady: boolean,
    cpf: any,
    logIn: (cpf:any) => void,
    logOut: () => void
};

const authStorageKey = 'auth-key';

export const AuthContext = createContext<AuthState>({
    isLoggedIn: false,
    isReady: false,
    cpf: '',
    logIn: (cpf:any) => {},
    logOut: () => {}
});

export function AuthProvider({ children }: PropsWithChildren) {
    const [isReady, setIsReady] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [cpf, setCpf] = useState('');
    const router = useRouter();

    const storeAuthState = async (newState: {isLoggedIn: boolean, cpf: any}) => {
        try {
            const jsonValue = JSON.stringify(newState);
            await AsyncStorage.setItem(authStorageKey, jsonValue);
        } catch (error) {
            console.log('Error saving.', error);
        };
    };

    const deleteAuthState = async () => {
        try {
            await AsyncStorage.removeItem(authStorageKey)
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

    useEffect(() => {
        const getAuthFromStorage = async () => {
            try {
                const value = await AsyncStorage.getItem(authStorageKey);
                if (value !== null) {
                    const auth = JSON.parse(value);
                    setIsLoggedIn(auth.isLoggedIn);
                    setCpf(auth.cpf);
                };
            } catch (error) {
                console.log('Error fetching from storage.', error);
            };
            setIsReady(true);
        };
        getAuthFromStorage();
    }, []);

    return (
        <AuthContext.Provider value={{ isLoggedIn, isReady, cpf, logIn, logOut }}>
            {children}
        </AuthContext.Provider>
    );
}