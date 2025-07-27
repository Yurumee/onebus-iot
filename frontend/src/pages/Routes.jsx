import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, ListGroup, Badge } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRoute, faPlus, faEdit, faTrashAlt, faMapMarkerAlt, faDotCircle, faTimes, faSave, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import { MapContainer, TileLayer, Marker, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';

// --- IMPORTAÇÕES PARA DRAG AND DROP ---
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { SortablePointItem } from '../components/SortablePointItem'; // Importa nosso novo componente

import styles from './Routes.module.css';
import 'leaflet/dist/leaflet.css';
import RoutingMachine from '../components/RoutingMachine';

// --- Ícones Customizados para o Mapa ---
const stopIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
});
const streetIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
});
// --- DADOS MOCKADOS ---
const mockInitialRoutes = [
  { id: 'R01', name: 'Rota Saúde - Manhã', service: 'Saúde', vehiclePlate: 'ONB-001', points: [{ id: 1, lat: -6.2603, lng: -36.5196, type: 'stop' }, { id: 2, lat: -6.2573, lng: -36.5222, type: 'street' }, { id: 3, lat: -6.2523, lng: -36.5247, type: 'stop' }] },
  { id: 'R02', name: 'Rota Educação - Manhã', service: 'Educação', vehiclePlate: 'VAN-001', points: [{ id: 4, lat: -6.28, lng: -36.52, type: 'stop' }, { id: 5, lat: -6.29, lng: -36.53, type: 'street' }, { id: 6, lat: -6.2525, lng: -36.5335, type: 'stop' }] }
];
const mockVehicles = [{ plate: 'ONB-001', name: 'Ônibus 01' }, { plate: 'VAN-001', name: 'Van 01' }, { plate: 'VAN-002', name: 'Van 02' }];

// Componente para interações do mapa
const MapEvents = ({ onMapClick, isEditing }) => {
  useMapEvents({ click(e) { if (isEditing) { onMapClick(e.latlng); } }, });
  return null;
};
// Componente para ajustar a visão do mapa
const ChangeMapView = ({ points }) => {
  const map = useMap();
  useEffect(() => { if (points && points.length > 0) { const bounds = L.latLngBounds(points.map(p => [p.lat, p.lng])); map.fitBounds(bounds, { padding: [50, 50] }); } }, [points, map]);
  return null;
}

function RoutesPage() {
  const [routes, setRoutes] = useState(mockInitialRoutes);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [editingRoute, setEditingRoute] = useState(null);
  const [pointType, setPointType] = useState('stop');

  // --- CONFIGURAÇÃO DO DND-KIT ---
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleSelectRoute = (route) => { setSelectedRoute(route); setEditingRoute(null); };
  const handleStartNewRoute = () => { setSelectedRoute(null); setEditingRoute({ id: `R${Date.now()}`, name: '', service: 'Saúde', vehiclePlate: '', points: [] }); };
  const handleEditRoute = (route) => { setSelectedRoute(route); setEditingRoute({ ...route }); };
  const handleCancel = () => { setEditingRoute(null); setSelectedRoute(routes[0] || null); };
  const handleFormChange = (e) => { const { name, value } = e.target; setEditingRoute(prev => ({ ...prev, [name]: value })); };


  const handleMapClick = (latlng) => {
    if (editingRoute) {
      // --- Adiciona um ID único a cada ponto ---
      const newPoint = { id: Date.now(), ...latlng, type: pointType };
      setEditingRoute(prev => ({ ...prev, points: [...prev.points, newPoint] }));
    }
  };

  const handleRemovePoint = (indexToRemove) => {
    setEditingRoute(prev => ({
      ...prev,
      points: prev.points.filter((_, index) => index !== indexToRemove)
    }));
  };

  // --- NOVA FUNÇÃO: Lida com o fim do arraste ---
  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (active.id !== over.id) {
      setEditingRoute(prev => {
        const oldIndex = prev.points.findIndex(p => p.id === active.id);
        const newIndex = prev.points.findIndex(p => p.id === over.id);
        return { ...prev, points: arrayMove(prev.points, oldIndex, newIndex) };
      });
    }
  };

  const pointsOnMap = editingRoute ? editingRoute.points : (selectedRoute ? selectedRoute.points : []);

  return (
    <div className={styles.routesPage}>
      <Container fluid>
        <Row>
          {/* COLUNA ESQUERDA - LISTA E FORMULÁRIO */}
          <Col lg={4} className={styles.leftPanel}>
            {!editingRoute ? (
              // ... (Modo de visualização, com os botões de editar/excluir) ...
              <Card className={styles.panelCard}>
                <Card.Header className={styles.panelHeader}>
                  <h5 className={styles.panelTitle}>Rotas Cadastradas</h5>
                  <Button variant="primary" size="sm" onClick={handleStartNewRoute}><FontAwesomeIcon icon={faPlus} className="me-2" />Nova Rota</Button>
                </Card.Header>
                <ListGroup variant="flush" className={styles.routeList}>
                  {routes.map(route => (
                    <ListGroup.Item key={route.id} action onClick={() => handleSelectRoute(route)} active={selectedRoute?.id === route.id} className="d-flex justify-content-between align-items-center">
                      <div>
                        <strong>{route.name}</strong>
                        <small className="d-block text-muted">{route.points.length} pontos</small>
                      </div>
                      <div>
                        <Button variant="light" size="sm" className="me-2" onClick={(e) => { e.stopPropagation(); handleEditRoute(route); }}><FontAwesomeIcon icon={faEdit} /></Button>
                        <Button variant="light" size="sm" className={styles.deleteButton}><FontAwesomeIcon icon={faTrashAlt} /></Button>
                      </div>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              </Card>
            ) : (
              // --- MODO DE EDIÇÃO ATUALIZADO ---
              <Card className={styles.panelCard}>
                <Card.Header className={styles.panelHeader}>
                  <Button variant="light" size="sm" onClick={handleCancel} className="me-2"><FontAwesomeIcon icon={faArrowLeft} /></Button>
                  <h5 className={styles.panelTitle}>{editingRoute.id.startsWith('R') && editingRoute.name ? 'Editar Rota' : 'Nova Rota'}</h5>
                </Card.Header>
                <Card.Body className={styles.formPanel}>
                  {/* ... (Formulário de nome, serviço, veículo como antes) ... */}
                  <Form>
                    <Form.Group className="mb-3"><Form.Label>Nome da Rota</Form.Label><Form.Control type="text" name="name" value={editingRoute.name} onChange={handleFormChange} /></Form.Group>
                    <Row><Col><Form.Group className="mb-3"><Form.Label>Serviço</Form.Label><Form.Select name="service" value={editingRoute.service} onChange={handleFormChange}><option>Saúde</option><option>Educação</option><option>Administrativo</option></Form.Select></Form.Group></Col><Col><Form.Group className="mb-3"><Form.Label>Veículo</Form.Label><Form.Select name="vehiclePlate" value={editingRoute.vehiclePlate} onChange={handleFormChange}><option value="">Selecione</option>{mockVehicles.map(v => <option key={v.plate} value={v.plate}>{v.name}</option>)}</Form.Select></Form.Group></Col></Row>
                    <hr />
                    <Form.Group className="mb-3"><Form.Label>Adicionar Pontos</Form.Label><div className={styles.pointTypeSelector}><Form.Check type="radio" id="type-stop" label={<><FontAwesomeIcon icon={faMapMarkerAlt} className="text-danger" /> Parada</>} name="pointType" inline checked={pointType === 'stop'} onChange={() => setPointType('stop')} /><Form.Check type="radio" id="type-street" label={<><FontAwesomeIcon icon={faDotCircle} className="text-secondary" /> Rua</>} name="pointType" inline checked={pointType === 'street'} onChange={() => setPointType('street')} /></div></Form.Group>

                    {/* --- LISTA DE PONTOS REORDENÁVEL --- */}
                    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
                      <ListGroup className={styles.pointList}>
                        <SortableContext items={editingRoute.points} strategy={verticalListSortingStrategy}>
                          {editingRoute.points.map((point, index) => (
                            <SortablePointItem key={point.id} point={point} index={index} onRemove={handleRemovePoint} />
                          ))}
                        </SortableContext>
                      </ListGroup>
                    </DndContext>
                  </Form>
                </Card.Body>
                <Card.Footer className="text-end">
                  <Button variant="secondary" className="me-2" onClick={handleCancel}>Cancelar</Button>
                  <Button variant="primary"><FontAwesomeIcon icon={faSave} className="me-2" />Salvar Rota</Button>
                </Card.Footer>
              </Card>
            )}
          </Col>

          {/* COLUNA DIREITA - MAPA */}
          <Col lg={8} className={styles.rightPanel}>
            <MapContainer center={[-6.26, -36.52]} zoom={14} className={styles.mapContainer}>
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap' />
              <MapEvents onMapClick={handleMapClick} isEditing={!!editingRoute} />
              <RoutingMachine points={pointsOnMap} isEditing={!!editingRoute} />
              {pointsOnMap.map((point, index) => (
                <Marker key={point.id} position={[point.lat, point.lng]} icon={point.type === 'stop' ? stopIcon : streetIcon} />
              ))}
              <ChangeMapView points={pointsOnMap} />
            </MapContainer>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default RoutesPage;