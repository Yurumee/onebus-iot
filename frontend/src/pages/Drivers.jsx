// src/pages/Drivers.jsx

import React, { useState } from 'react';
import { Container, Row, Col, Card, Table, Button, Badge, InputGroup, Form, Modal } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUsers, faTruck, faUserCheck, faSearch, faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';

import styles from './Drivers.module.css';

// --- Dados Mockados ---
const mockDrivers = [
  { id: 1, name: 'Carlos Silva', cnh: '12345678900', vehiclePlate: 'ONB-001', status: 'Ativo' },
  { id: 2, name: 'Ana Souza', cnh: '98765432101', vehiclePlate: 'ONB-002', status: 'Ativo' },
  { id: 3, name: 'João Pereira', cnh: '11122233344', vehiclePlate: 'ONB-003', status: 'Ativo' },
  { id: 4, name: 'Mariana Lima', cnh: '44455566677', vehiclePlate: null, status: 'Inativo' },
  { id: 5, name: 'Ricardo Alves', cnh: '77788899900', vehiclePlate: 'VAN-001', status: 'Ativo' },
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

function Drivers() {
  const activeDrivers = mockDrivers.filter(d => d.status === 'Ativo').length;

  // --- Estados para controle dos Modais ---
  const [showNewModal, setShowNewModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedDriver, setSelectedDriver] = useState(null);

  // --- Funções para manipular os Modais ---
  const handleShowNewModal = () => setShowNewModal(true);
  const handleCloseNewModal = () => setShowNewModal(false);

  const handleShowEditModal = (driver) => {
    setSelectedDriver(driver);
    setShowEditModal(true);
  };
  const handleCloseEditModal = () => {
    setShowEditModal(false);
    setSelectedDriver(null);
  };

  const handleShowDeleteModal = (driver) => {
    setSelectedDriver(driver);
    setShowDeleteModal(true);
  };
  const handleCloseDeleteModal = () => {
    setShowDeleteModal(false);
    setSelectedDriver(null);
  };

  // Funções de Ação (simuladas)
  const handleSaveChanges = () => {
    console.log("Salvando alterações para:", selectedDriver);
    handleCloseEditModal();
  };

  const handleCreateDriver = () => {
    console.log("Criando novo motorista...");
    handleCloseNewModal();
  };

  const handleDeleteDriver = () => {
    console.log("Deletando motorista:", selectedDriver);
    handleCloseDeleteModal();
  };


  return (
    <div className={styles.driversPage}>
      <Container fluid>
        {/* --- Cabeçalho --- */}
        <header className={styles.pageHeader}>
          <h1 className={styles.pageTitle}>Motoristas e Frota</h1>
          <p className={styles.pageSubtitle}>Gerencie seus motoristas e a alocação de veículos.</p>
        </header>

        {/* --- Cards de Resumo --- */}
        <Row className="g-4 mb-4">
          <Col md={4}><StatCard icon={faUsers} title="Total de Motoristas" value={mockDrivers.length} colorClass="total" /></Col>
          <Col md={4}><StatCard icon={faUserCheck} title="Motoristas Ativos" value={activeDrivers} colorClass="online" /></Col>
          <Col md={4}><StatCard icon={faTruck} title="Total de Veículos" value={mockDrivers.filter(d => d.vehiclePlate).length} colorClass="vehicles" /></Col>
        </Row>

        {/* --- Tabela de Motoristas --- */}
        <Row>
          <Col>
            <Card className={styles.mainCard}>
              <Card.Header>
                <div className={styles.cardHeaderContent}>
                  <span>Motoristas Cadastrados</span>
                  <div className="d-flex align-items-center">
                    <InputGroup size="sm" style={{ maxWidth: '250px' }}>
                      <InputGroup.Text><FontAwesomeIcon icon={faSearch} /></InputGroup.Text>
                      <Form.Control placeholder="Buscar motorista..." />
                    </InputGroup>
                    <Button variant="primary" size="sm" className="ms-3" onClick={handleShowNewModal}>Novo Motorista</Button>
                  </div>
                </div>
              </Card.Header>
              <div className={styles.tableWrapper}>
                <Table hover responsive className={styles.customTable}>
                  <thead>
                    <tr>
                      <th>Nome</th>
                      <th>CNH</th>
                      <th>Veículo Alocado</th>
                      <th>Status</th>
                      <th>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockDrivers.map(driver => (
                      <tr key={driver.id}>
                        <td><b>{driver.name}</b></td>
                        <td>{driver.cnh}</td>
                        <td>
                          {driver.vehiclePlate
                            ? <Badge bg="light" text="dark">{driver.vehiclePlate}</Badge>
                            : <Badge bg="secondary" text="white">Nenhum</Badge>
                          }
                        </td>
                        <td><Badge pill bg={driver.status === 'Ativo' ? 'success' : 'danger'}>{driver.status}</Badge></td>
                        <td>
                          <Button variant="outline-secondary" size="sm" className={styles.actionButton} onClick={() => handleShowEditModal(driver)}>
                            <FontAwesomeIcon icon={faEdit} />
                          </Button>
                          <Button variant="outline-danger" size="sm" className={styles.actionButton} onClick={() => handleShowDeleteModal(driver)}>
                            <FontAwesomeIcon icon={faTrashAlt} />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* --- MODAL DE NOVO MOTORISTA --- */}
      <Modal show={showNewModal} onHide={handleCloseNewModal} centered>
        <Modal.Header closeButton>
          <Modal.Title>Cadastrar Novo Motorista</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="formNewDriverName">
              <Form.Label>Nome Completo</Form.Label>
              <Form.Control type="text" placeholder="Digite o nome do motorista" autoFocus />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formNewDriverCNH">
              <Form.Label>CNH</Form.Label>
              <Form.Control type="text" placeholder="Digite a CNH" />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseNewModal}>Cancelar</Button>
          <Button variant="primary" onClick={handleCreateDriver}>Salvar</Button>
        </Modal.Footer>
      </Modal>

      {/* --- MODAL DE EDITAR MOTORISTA --- */}
      {selectedDriver && (
        <Modal show={showEditModal} onHide={handleCloseEditModal} centered>
          <Modal.Header closeButton>
            <Modal.Title>Editar Motorista</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group className="mb-3" controlId="formEditDriverName">
                <Form.Label>Nome Completo</Form.Label>
                <Form.Control type="text" defaultValue={selectedDriver.name} autoFocus />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formEditDriverCNH">
                <Form.Label>CNH</Form.Label>
                <Form.Control type="text" defaultValue={selectedDriver.cnh} />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formEditDriverStatus">
                <Form.Label>Status</Form.Label>
                <Form.Select defaultValue={selectedDriver.status}>
                  <option>Ativo</option>
                  <option>Inativo</option>
                </Form.Select>
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseEditModal}>Cancelar</Button>
            <Button variant="primary" onClick={handleSaveChanges}>Salvar Alterações</Button>
          </Modal.Footer>
        </Modal>
      )}

      {/* --- MODAL DE DELETAR MOTORISTA --- */}
      {selectedDriver && (
        <Modal show={showDeleteModal} onHide={handleCloseDeleteModal} centered>
          <Modal.Header closeButton>
            <Modal.Title>Confirmar Exclusão</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            Você tem certeza que deseja excluir o motorista <strong>{selectedDriver.name}</strong>?
            <br />
            <small className="text-danger">Esta ação não poderá ser desfeita.</small>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseDeleteModal}>Cancelar</Button>
            <Button variant="danger" onClick={handleDeleteDriver}>Confirmar Exclusão</Button>
          </Modal.Footer>
        </Modal>
      )}
    </div>
  );
}

export default Drivers;