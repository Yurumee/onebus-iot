import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';

// Componente para mudar a visão do mapa
function ChangeView({ center, zoom }) {
    const map = useMap();
    useEffect(() => {
        if (center) {
            map.flyTo(center, zoom, {
                animate: true,
                duration: 1.5
            });
        }
    }, [center, zoom, map]);
    return null;
}

function VehicleMap({ vehicles, selectedVehicle }) {
    // Posição inicial do mapa (Centro de Currais Novos, RN)
    const initialPosition = [-6.2605, -36.5272];

    // Define o centro do mapa com base no veículo selecionado, ou usa a posição inicial
    const mapCenter = selectedVehicle ? selectedVehicle.position : initialPosition;

    return (
        <MapContainer center={initialPosition} zoom={13} style={{ height: '100%', width: '100%' }}>
            {/* Componente que lida com a mudança de visão */}
            <ChangeView center={selectedVehicle?.position} zoom={16} />
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {vehicles.map(vehicle => (
                <Marker key={vehicle.id} position={vehicle.position}>
                    <Popup>
                        <b>{vehicle.name} ({vehicle.id})</b><br />
                        Status: {vehicle.status}
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}

export default VehicleMap;