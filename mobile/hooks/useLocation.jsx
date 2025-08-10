import React, { useEffect, useState } from 'react';
import * as Location from 'expo-location';

const useLocation = () => {
    const [errorMsg, setErrorMsg] = useState('');
    const [latitude, setLatitude] = useState(0);
    const [longitude, setLongitude] = useState(0);

    const getUserPermission = async () => {
        let {status} = await Location.requestForegroundPermissionsAsync();

        if (status !== 'granted') {
            setErrorMsg("Permissão para localização não foi concedida.");
            return;
        };

        let {coords} = await Location.getCurrentPositionAsync();

        if (coords) {
            const { latitude, longitude } = coords;
            console.log('Latitude e longitude: ', latitude, longitude)
            setLatitude(parseFloat(latitude))
            setLongitude(parseFloat(longitude))
        };
    };

    useEffect(() => {
        getUserPermission();
    }, []);

    return {latitude, longitude, errorMsg}
};

export default useLocation