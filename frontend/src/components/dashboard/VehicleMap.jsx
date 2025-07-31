import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

// Um ícone customizado seria legal aqui no futuro, mas por enquanto o padrão serve.

function VehicleMap({ vehicles }) {
    // Posição inicial do mapa (Centro de Currais Novos, RN)
    const initialPosition = [-6.2605, -36.5272];

    return (
        <MapContainer center={initialPosition} zoom={13} style={{ height: '60vh', width: '100%', borderRadius: '8px' }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {vehicles.map(vehicle => (
                <Marker key={vehicle.id} position={vehicle.position}>
                    <Popup>
                        <b>{vehicle.name}</b><br />
                        Status: {vehicle.status}
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}

export default VehicleMap;