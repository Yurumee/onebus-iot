import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTruck, faSatelliteDish, faRoute, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';

// 1. AQUI IMPORTAMOS O COMPONENTE DO MAPA
import VehicleMap from '../components/dashboard/VehicleMap';

import styles from './Dashboard.module.css';

const mockVehicles = [
  { id: 'ONB-001', name: 'Ônibus 01', status: 'Em Rota', position: [-6.255, -36.520] },
  { id: 'ONB-002', name: 'Ônibus 02', status: 'Parado', position: [-6.265, -36.535] },
  { id: 'ONB-003', name: 'Ônibus 03', status: 'Em Rota', position: [-6.260, -36.515] },
  { id: 'ONB-004', name: 'Van 01', status: 'Offline', position: [-6.270, -36.540] },
];

function Dashboard() {
  const onlineVehicles = mockVehicles.filter(v => v.status !== 'Offline').length;

  return (
    <div className={styles.dashboardPage}>
      <Container fluid>
        <h1 className={`h3 mb-4 ${styles.dashboardTitle}`}>Dashboard de Operações</h1>

        {/* Linha dos Cartões de Estatísticas */}
        <Row>
          {/* ... Colunas com os Cards de estatísticas ... */}
          <Col md={6} xl={3} className="mb-4">
            <Card className={`${styles.statCard} ${styles.total}`}>
              <Card.Body>
                <div className={styles.statCardTitle}>Frota Total</div>
                <div className={styles.statCardValue}>{mockVehicles.length}</div>
                <FontAwesomeIcon icon={faTruck} className={styles.statCardIconBg} />
              </Card.Body>
            </Card>
          </Col>

          <Col md={6} xl={3} className="mb-4">
            <Card className={`${styles.statCard} ${styles.online}`}>
              <Card.Body>
                <div className={styles.statCardTitle}>Veículos Online</div>
                <div className={styles.statCardValue}>{onlineVehicles}</div>
                <FontAwesomeIcon icon={faSatelliteDish} className={styles.statCardIconBg} />
              </Card.Body>
            </Card>
          </Col>

          <Col md={6} xl={3} className="mb-4">
            <Card className={`${styles.statCard} ${styles.routes}`}>
              <Card.Body>
                <div className={styles.statCardTitle}>Rotas Ativas</div>
                <div className={styles.statCardValue}>2</div>
                <FontAwesomeIcon icon={faRoute} className={styles.statCardIconBg} />
              </Card.Body>
            </Card>
          </Col>

          <Col md={6} xl={3} className="mb-4">
            <Card className={`${styles.statCard} ${styles.alerts}`}>
              <Card.Body>
                <div className={styles.statCardTitle}>Alertas</div>
                <div className={styles.statCardValue}>1</div>
                <FontAwesomeIcon icon={faTriangleExclamation} className={styles.statCardIconBg} />
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Linha do Mapa */}
        <Row>
          <Col>
            <Card className={styles.mapCard}>
              <Card.Header>Localização da Frota em Tempo Real</Card.Header>
              <Card.Body className="p-0">
                {/* 2. AQUI USAMOS O COMPONENTE, PASSANDO OS DADOS DOS VEÍCULOS */}
                <VehicleMap vehicles={mockVehicles} />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Dashboard;