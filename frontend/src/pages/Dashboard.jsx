// src/pages/Dashboard.jsx

import React from 'react';
import { Container, Row, Col, Card, Table, Badge } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTruck, faSatelliteDish, faRoute, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

import VehicleMap from '../components/dashboard/VehicleMap';
import styles from './Dashboard.module.css';

// Registrando os componentes necessários para o Chart.js
ChartJS.register(ArcElement, Tooltip, Legend);

const mockVehicles = [
  { id: 'ONB-001', name: 'Ônibus 01', driver: 'Carlos Silva', status: 'Em Rota', position: [-6.255, -36.520] },
  { id: 'ONB-002', name: 'Ônibus 02', driver: 'Ana Souza', status: 'Parado', position: [-6.265, -36.535] },
  { id: 'ONB-003', name: 'Ônibus 03', driver: 'João Pereira', status: 'Em Rota', position: [-6.260, -36.515] },
  { id: 'ONB-004', name: 'Van 01', driver: 'Maria Costa', status: 'Offline', position: [-6.270, -36.540] },
];

// Componente para o Card de Estatística
const StatCard = ({ icon, title, value, colorClass }) => (
  <div className={`${styles.statCard} ${styles[colorClass]}`}>
    <div className={styles.statIconWrapper}>
      <FontAwesomeIcon icon={icon} className={styles.statIcon} />
    </div>
    <div className={styles.statInfo}>
      <span className={styles.statTitle}>{title}</span>
      <span className={styles.statValue}>{value}</span>
    </div>
  </div>
);

function Dashboard() {
  const onlineVehicles = mockVehicles.filter(v => v.status !== 'Offline');
  const statusCounts = mockVehicles.reduce((acc, vehicle) => {
    acc[vehicle.status] = (acc[vehicle.status] || 0) + 1;
    return acc;
  }, {});

  const chartData = {
    labels: ['Em Rota', 'Parado', 'Offline'],
    datasets: [{
      label: 'Status da Frota',
      data: [statusCounts['Em Rota'] || 0, statusCounts['Parado'] || 0, statusCounts['Offline'] || 0],
      backgroundColor: ['#106F4C', '#636A73', '#d0d4da'],
      borderColor: '#FFFFFF',
      borderWidth: 3,
      hoverOffset: 4,
    }],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
        labels: { padding: 20, usePointStyle: true, pointStyle: 'circle' },
      },
    },
  };

  return (
    <div className={styles.dashboardPage}>
      <Container fluid>
        <header className={styles.welcomeHeader}>
          <h1 className={styles.welcomeTitle}>Bem-vindo de volta, Yago!</h1>
          <p className={styles.welcomeSubtitle}>Aqui está o resumo da sua frota hoje, 19 de Julho de 2025.</p>
        </header>

        {/* Linha principal com altura alinhada */}
        <Row className="g-4">
          {/* Coluna Esquerda (Mapa) */}
          <Col lg={8}>
            <Card className={`${styles.mainCard} h-100 d-flex flex-column`}>
              <Card.Header>Localização da Frota em Tempo Real</Card.Header>
              <Card.Body className={`${styles.mapCardBody} flex-grow-1`}>
                <VehicleMap vehicles={mockVehicles} />
              </Card.Body>
            </Card>
          </Col>

          {/* Coluna Direita (Informações) */}
          <Col lg={4}>
            {/* Contêiner flex vertical para alinhar os itens da coluna */}
            <div className="h-100 d-flex flex-column">
              <div className={styles.statsGrid}>
                <StatCard icon={faTruck} title="Frota Total" value={mockVehicles.length} colorClass="total" />
                <StatCard icon={faSatelliteDish} title="Online" value={onlineVehicles.length} colorClass="online" />
              </div>
              <Card className={`${styles.mainCard} mt-4 flex-grow-1 d-flex flex-column`}>
                <Card.Header>Status dos Veículos</Card.Header>
                <Card.Body className="d-flex flex-grow-1">
                  <Doughnut data={chartData} options={chartOptions} />
                </Card.Body>
              </Card>
            </div>
          </Col>
        </Row>

        {/* Tabela de Veículos em uma nova linha */}
        <Row className="mt-4">
          <Col>
            <Card className={styles.mainCard}>
              <Card.Header>Veículos Ativos</Card.Header>
              <div className={styles.tableWrapper}>
                <Table hover responsive className={styles.vehicleTable}>
                  <thead>
                    <tr>
                      <th>Veículo</th>
                      <th>Motorista</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {onlineVehicles.map(v => (
                      <tr key={v.id}>
                        <td><b>{v.id}</b><br /><small className={styles.vehicleName}>{v.name}</small></td>
                        <td>{v.driver}</td>
                        <td><Badge pill bg={v.status === 'Em Rota' ? 'success' : 'secondary'} className={styles.statusBadge}>{v.status}</Badge></td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Dashboard;