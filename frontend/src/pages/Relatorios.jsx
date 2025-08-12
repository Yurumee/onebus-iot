import React, { useState, useMemo } from 'react';
import { Container, Row, Col, Card, Form, Button, ListGroup } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faCalendarAlt, faCar, faClock, faRoad } from '@fortawesome/free-solid-svg-icons';

// Importando dados mocados
import { mockHistoricoViagens } from '../mocks/mockHistoricoViagens';
import { mockCarros } from '../mocks/mockCarros';

// Importando o mapa e o componente de rota
import VehicleMap from '../components/dashboard/VehicleMap';
import RoutingMachine from '../components/RoutingMachine';
import styles from './Relatorios.module.css';

// --- Funções Auxiliares para Cálculo ---
const haversineDistance = (coords1, coords2) => {
    const toRad = (x) => (x * Math.PI) / 180;
    const R = 6371; // Raio da Terra em km

    const dLat = toRad(coords2.lat - coords1.lat);
    const dLon = toRad(coords2.lng - coords1.lng);
    const lat1 = toRad(coords1.lat);
    const lat2 = toRad(coords2.lat);

    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c; // Distância em km
};

const calculateTripDetails = (viagem) => {
    let totalDistance = 0;
    for (let i = 0; i < viagem.pontos.length - 1; i++) {
        totalDistance += haversineDistance(viagem.pontos[i], viagem.pontos[i + 1]);
    }

    const startTime = new Date(viagem.pontos[0].timestamp);
    const endTime = new Date(viagem.pontos[viagem.pontos.length - 1].timestamp);
    const durationMinutes = (endTime - startTime) / 60000; // Duração em minutos

    return {
        distancia: totalDistance.toFixed(2),
        duracao: Math.round(durationMinutes),
    };
};


function Relatorios() {
    const [filtros, setFiltros] = useState({ placa: '', data: '' });
    const [viagensFiltradas, setViagensFiltradas] = useState([]);
    const [viagemSelecionada, setViagemSelecionada] = useState(null);

    const handleFilterChange = (e) => {
        setFiltros({ ...filtros, [e.target.name]: e.target.value });
    };

    const handleSearch = () => {
        let resultado = mockHistoricoViagens;

        if (filtros.placa) {
            resultado = resultado.filter(v => v.placa === filtros.placa);
        }
        if (filtros.data) {
            resultado = resultado.filter(v => v.data === filtros.data);
        }
        setViagensFiltradas(resultado);
        setViagemSelecionada(null); // Limpa a seleção ao buscar
    };

    // Calcula os detalhes apenas quando a viagem selecionada mudar
    const detalhesDaViagem = useMemo(() => {
        if (!viagemSelecionada) return null;
        return calculateTripDetails(viagemSelecionada);
    }, [viagemSelecionada]);

    return (
        <div className={styles.reportsPage}>
            <Container fluid>
                <header className={styles.pageHeader}>
                    <h1>Relatórios de Viagens</h1>
                    <p>Analise o histórico de viagens, distâncias percorridas e tempo gasto.</p>
                </header>

                <Row>
                    {/* Coluna de Filtros e Resultados */}
                    <Col lg={4}>
                        <Card className={styles.panelCard}>
                            <Card.Header>Filtros</Card.Header>
                            <Card.Body>
                                <Form>
                                    <Form.Group className="mb-3">
                                        <Form.Label><FontAwesomeIcon icon={faCar} className="me-2" />Veículo</Form.Label>
                                        <Form.Select name="placa" value={filtros.placa} onChange={handleFilterChange}>
                                            <option value="">Todos os veículos</option>
                                            {mockCarros.map(carro => (
                                                <option key={carro.placa} value={carro.placa}>{carro.placa} ({carro.tipo_veiculo})</option>
                                            ))}
                                        </Form.Select>
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label><FontAwesomeIcon icon={faCalendarAlt} className="me-2" />Data da Viagem</Form.Label>
                                        <Form.Control type="date" name="data" value={filtros.data} onChange={handleFilterChange} />
                                    </Form.Group>
                                    <Button variant="primary" onClick={handleSearch} className="w-100">
                                        <FontAwesomeIcon icon={faSearch} className="me-2" />Buscar
                                    </Button>
                                </Form>
                            </Card.Body>
                        </Card>

                        <Card className={`${styles.panelCard} mt-4`}>
                            <Card.Header>Viagens Encontradas ({viagensFiltradas.length})</Card.Header>
                            <ListGroup variant="flush" className={styles.resultsList}>
                                {viagensFiltradas.length > 0 ? viagensFiltradas.map(viagem => (
                                    <ListGroup.Item key={viagem.id} action onClick={() => setViagemSelecionada(viagem)} active={viagemSelecionada?.id === viagem.id}>
                                        <strong>{viagem.placa}</strong> - <small>{new Date(viagem.data).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</small>
                                        <span className="d-block text-muted">{viagem.motorista}</span>
                                    </ListGroup.Item>
                                )) : (
                                    <ListGroup.Item className="text-center text-muted">Nenhuma viagem encontrada.</ListGroup.Item>
                                )}
                            </ListGroup>
                        </Card>
                    </Col>

                    {/* Coluna de Detalhes da Viagem e Mapa */}
                    <Col lg={8}>
                        <Card className={`${styles.panelCard} h-100`}>
                            <Card.Header>Detalhes da Viagem</Card.Header>
                            <Card.Body>
                                {viagemSelecionada && detalhesDaViagem ? (
                                    <div>
                                        <Row className="mb-4">
                                            <Col><div className={styles.detailBox}><FontAwesomeIcon icon={faRoad} /> <div><span>Distância</span><strong>{detalhesDaViagem.distancia} km</strong></div></div></Col>
                                            <Col><div className={styles.detailBox}><FontAwesomeIcon icon={faClock} /> <div><span>Duração</span><strong>{detalhesDaViagem.duracao} min</strong></div></div></Col>
                                        </Row>
                                        <div className={styles.mapContainer}>
                                            <VehicleMap vehicles={[]} selectedVehicle={{ position: viagemSelecionada.pontos[0] }}>
                                                <RoutingMachine points={viagemSelecionada.pontos} isEditing={false} />
                                            </VehicleMap>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="text-center text-muted h-100 d-flex align-items-center justify-content-center">
                                        <p>Selecione uma viagem à esquerda para ver os detalhes.</p>
                                    </div>
                                )}
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default Relatorios;