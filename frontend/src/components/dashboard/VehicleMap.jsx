import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet'; // Importando L para usar ícones customizados

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

// --- ÍCONES CUSTOMIZADOS ---

// Ícone padrão para veículos
const vehicleIcon = new L.Icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
    shadowSize: [41, 41]
});

// Ícone para o PONTO DE INÍCIO (Verde)
const startIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// Ícone para o PONTO FINAL (Vermelho)
const endIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});


function VehicleMap({ vehicles = [], selectedVehicle, children }) { // Adicionado 'children' e valor padrão para vehicles
    // Posição inicial do mapa (Centro de Currais Novos, RN)
    const initialPosition = [-6.2605, -36.5272];

    // Define o centro do mapa com base no veículo selecionado, ou usa a posição inicial
    const mapCenter = selectedVehicle?.position;

    return (
        <MapContainer center={initialPosition} zoom={13} style={{ height: '100%', width: '100%' }}>
            {/* Componente que lida com a mudança de visão */}
            <ChangeView center={mapCenter} zoom={selectedVehicle ? 16 : 13} />
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {/* Renderiza a frota de veículos, se houver */}
            {vehicles.map(vehicle => (
                vehicle.position && // Garante que a posição existe
                <Marker key={vehicle.id} position={vehicle.position} icon={vehicleIcon}>
                    <Popup>
                        <b>{vehicle.name} ({vehicle.id})</b><br />
                        Status: {vehicle.status}
                    </Popup>
                </Marker>
            ))}

            {/* Renderiza qualquer componente filho passado para o VehicleMap */}
            {children}
        </MapContainer>
    );
}

export { vehicleIcon, startIcon, endIcon };
export default VehicleMap;