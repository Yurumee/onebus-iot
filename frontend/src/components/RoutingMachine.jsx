import { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';
import 'leaflet-routing-machine';
import { useMap } from 'react-leaflet';

const RoutingMachine = ({ points, isEditing }) => {
    const map = useMap();

    useEffect(() => {
        if (!map || points.length < 2) return;

        const waypoints = points.map(p => L.latLng(p.lat, p.lng));

        const routingControl = L.Routing.control({
            waypoints: waypoints,
            routeWhileDragging: false,
            addWaypoints: false, // Não permite adicionar pontos arrastando a rota
            draggableWaypoints: false,
            fitSelectedRoutes: true,
            show: false, // Esconde o painel de instruções de rota
            createMarker: () => null, // Não cria os marcadores padrão A e B
            lineOptions: {
                styles: [{
                    color: isEditing ? 'orange' : '#0d6efd', // Cor diferente no modo de edição
                    opacity: 0.8,
                    weight: 6
                }]
            }
        }).addTo(map);

        // Função de limpeza para remover a rota antiga ao atualizar
        return () => map.removeControl(routingControl);
    }, [map, points, isEditing]);

    return null;
};

export default RoutingMachine;