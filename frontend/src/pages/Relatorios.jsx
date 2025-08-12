import React, { useState, useMemo } from 'react';
// IMPORTAÇÕES DE REACT-BOOTSTRAP (Marker e Popup foram removidos daqui)
import { Container, Row, Col, Card, Form, Button, ListGroup } from 'react-bootstrap';
// IMPORTAÇÕES DE REACT-LEAFLET (Marker e Popup foram adicionados aqui)
import { Marker, Popup } from 'react-leaflet';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faClock, faRoad, faInfoCircle } from '@fortawesome/free-solid-svg-icons';

import { mockHistoricoViagens } from '../mocks/mockHistoricoViagens';
import { mockCarros } from '../mocks/mockCarros';
// Importando o mapa E OS NOVOS ÍCONES
import VehicleMap, { startIcon, endIcon } from '../components/dashboard/VehicleMap';
import RoutingMachine from '../components/RoutingMachine';
import styles from './Relatorios.module.css';

// --- Funções e Componentes auxiliares (sem alterações) ---
const haversineDistance = (coords1, coords2) => {
    const toRad = (x) => (x * Math.PI) / 180;
    const R = 6371;
    const dLat = toRad(coords2.lat - coords1.lat);
    const dLon = toRad(coords2.lng - coords1.lng);
    const lat1 = toRad(coords1.lat);
    const lat2 = toRad(coords2.lat);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
};

const calculateTripDetails = (viagem) => {
    if (!viagem || viagem.pontos.length === 0) return { distancia: 0, duracao: 0 };
    let totalDistance = 0;
    for (let i = 0; i < viagem.pontos.length - 1; i++) {
        totalDistance += haversineDistance(viagem.pontos[i], viagem.pontos[i + 1]);
    }
    const startTime = new Date(viagem.pontos[0].timestamp);
    const endTime = new Date(viagem.pontos[viagem.pontos.length - 1].timestamp);
    const durationMinutes = (endTime - startTime) / 60000;
    return {
        distancia: totalDistance.toFixed(2),
        duracao: Math.round(durationMinutes),
    };
};

const DetailStatCard = ({ icon, title, value, unit, colorClass }) => (
    <div className={`${styles.detailStatCard} ${styles[colorClass]}`}>
        <div className={styles.statIconWrapper}>
            <FontAwesomeIcon icon={icon} />
        </div>
        <div className={styles.statInfo}>
            <span className={styles.statTitle}>{title}</span>
            <span className={styles.statValue}>
                {value} <span className={styles.statUnit}>{unit}</span>
            </span>
        </div>
    </div>
);
// --- Fim das funções auxiliares ---


function Relatorios() {
    const [filtros, setFiltros] = useState({ placa: '', data: '' });
    const [viagensFiltradas, setViagensFiltradas] = useState([]);
    const [viagemSelecionada, setViagemSelecionada] = useState(null);
    const [buscou, setBuscou] = useState(false);

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
        setViagemSelecionada(null);
        setBuscou(true);
    };

    const detalhesDaViagem = useMemo(() => {
        if (!viagemSelecionada) return null;
        return calculateTripDetails(viagemSelecionada);
    }, [viagemSelecionada]);

    const pontoInicial = viagemSelecionada?.pontos[0];
    const pontoFinal = viagemSelecionada?.pontos[viagemSelecionada.pontos.length - 1];

    return (
        <div className={styles.reportsPage}>
            <Container fluid>
                <header className={styles.pageHeader}>
                    <h1>Relatórios de Viagens</h1>
                    <p>Analise o histórico de viagens, distâncias percorridas e tempo gasto.</p>
                </header>

                <Row className="g-4">
                    <Col lg={4} className="d-flex flex-column g-4">
                        {/* Painel de Busca */}
                        <Card className={styles.panelCard}>
                            <Card.Header><FontAwesomeIcon icon={faSearch} className="me-2" />Painel de Busca</Card.Header>
                            <Card.Body>
                                <Form>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Veículo</Form.Label>
                                        <Form.Select name="placa" value={filtros.placa} onChange={handleFilterChange}>
                                            <option value="">Todos os veículos</option>
                                            {mockCarros.map(carro => (
                                                <option key={carro.placa} value={carro.placa}>{carro.placa} ({carro.tipo_veiculo})</option>
                                            ))}
                                        </Form.Select>
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Data da Viagem</Form.Label>
                                        <Form.Control type="date" name="data" value={filtros.data} onChange={handleFilterChange} />
                                    </Form.Group>
                                    <Button variant="primary" onClick={handleSearch} className="w-100 fw-bold">
                                        Buscar Relatórios
                                    </Button>
                                </Form>
                            </Card.Body>
                        </Card>
                        {/* Resultados */}
                        {buscou && (
                            <Card className={`${styles.panelCard} flex-grow-1`}>
                                <Card.Header>Resultados ({viagensFiltradas.length})</Card.Header>
                                <ListGroup variant="flush" className={styles.resultsList}>
                                    {viagensFiltradas.length > 0 ? viagensFiltradas.map(viagem => (
                                        <ListGroup.Item key={viagem.id} action onClick={() => setViagemSelecionada(viagem)} active={viagemSelecionada?.id === viagem.id}>
                                            <strong>{viagem.placa}</strong> - <span>{viagem.motorista}</span>
                                            <small className="d-block text-muted">{new Date(viagem.data).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</small>
                                        </ListGroup.Item>
                                    )) : (
                                        <div className={styles.emptyState}><p>Nenhuma viagem encontrada.</p></div>
                                    )}
                                </ListGroup>
                            </Card>
                        )}
                    </Col>

                    {/* Mapa e Detalhes */}
                    <Col lg={8}>
                        <Card className={`${styles.panelCard} h-100`}>
                            <Card.Header>Detalhes da Viagem Selecionada</Card.Header>
                            <Card.Body className="d-flex flex-column">
                                {viagemSelecionada && detalhesDaViagem ? (
                                    <>
                                        <div className={styles.detailsHeader}>
                                            <div>
                                                <h3 className={styles.detailsTitle}>{viagemSelecionada.placa}</h3>
                                                <p className={styles.detailsSubtitle}>
                                                    Motorista: {viagemSelecionada.motorista} | Data: {new Date(viagemSelecionada.data).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}
                                                </p>
                                            </div>
                                            <div className={styles.statsGrid}>
                                                <DetailStatCard icon={faRoad} title="Distância" value={detalhesDaViagem.distancia} unit="km" colorClass="distance" />
                                                <DetailStatCard icon={faClock} title="Duração" value={detalhesDaViagem.duracao} unit="min" colorClass="duration" />
                                            </div>
                                        </div>

                                        <div className={styles.mapContainer}>
                                            <VehicleMap selectedVehicle={{ position: pontoInicial }}>
                                                {viagemSelecionada.pontos.length > 1 && (
                                                    <RoutingMachine points={viagemSelecionada.pontos} isEditing={false} />
                                                )}

                                                {/* USA O ÍCONE DE INÍCIO (VERDE) */}
                                                {pontoInicial && (
                                                    <Marker position={[pontoInicial.lat, pontoInicial.lng]} icon={startIcon}>
                                                        <Popup><b>Início da Viagem</b><br />{new Date(pontoInicial.timestamp).toLocaleTimeString('pt-BR')}</Popup>
                                                    </Marker>
                                                )}

                                                {/* USA O ÍCONE DE FIM (VERMELHO) */}
                                                {pontoFinal && pontoFinal.lat !== pontoInicial.lat && (
                                                    <Marker position={[pontoFinal.lat, pontoFinal.lng]} icon={endIcon}>
                                                        <Popup><b>Fim da Viagem</b><br />{new Date(pontoFinal.timestamp).toLocaleTimeString('pt-BR')}</Popup>
                                                    </Marker>
                                                )}
                                            </VehicleMap>
                                        </div>
                                    </>
                                ) : (
                                    <div className={styles.emptyState}>
                                        <FontAwesomeIcon icon={faInfoCircle} size="3x" className="mb-3" />
                                        <h4>Nenhuma viagem selecionada</h4>
                                        <p>Faça uma busca e selecione uma viagem para ver seus detalhes.</p>
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