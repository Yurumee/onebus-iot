// src/pages/Drivers.jsx

import React, { useState } from 'react';
import { Container, Row, Col, Card, Table, Button, Badge, Form, Modal, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUsers, faTruck, faUserCheck, faSearch, faEdit, faTrashAlt, faPlus, faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';

import styles from './Drivers.module.css';

// --- Dados Mockados ---
const mockDrivers = [
  { id: 1, name: 'Carlos Silva', cnh: '12345678900', vehiclePlate: 'ONB-001', status: 'Ativo' },
  { id: 2, name: 'Ana Souza', cnh: '98765432101', vehiclePlate: 'ONB-002', status: 'Ativo' },
  { id: 3, name: 'João Pereira', cnh: '11122233344', vehiclePlate: 'ONB-003', status: 'Ativo' },
  { id: 4, name: 'Mariana Lima', cnh: '44455566677', vehiclePlate: null, status: 'Inativo' },
  { id: 5, name: 'Ricardo Alves', cnh: '77788899900', vehiclePlate: 'VAN-001', status: 'Ativo' },
];

const mockVehicles = [
  { plate: 'ONB-001', name: 'Ônibus 01', type: 'Ônibus', driverId: 1, status: 'Em Rota' },
  { plate: 'ONB-002', name: 'Ônibus 02', type: 'Ônibus', driverId: 2, status: 'Parado' },
  { plate: 'ONB-003', name: 'Ônibus 03', type: 'Ônibus', driverId: 3, status: 'Em Rota' },
  { plate: 'VAN-001', name: 'Van 01', type: 'Van', driverId: 5, status: 'Manutenção' },
  { plate: 'VAN-002', name: 'Van 02', type: 'Van', driverId: null, status: 'Disponível' },
];


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

  const [showNewModal, setShowNewModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showNewVehicleModal, setShowNewVehicleModal] = useState(false);
  const [selectedDriver, setSelectedDriver] = useState(null);

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

  const handleShowNewVehicleModal = () => setShowNewVehicleModal(true);
  const handleCloseNewVehicleModal = () => setShowNewVehicleModal(false);

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

  const handleCreateVehicle = () => {
    console.log("Criando novo veículo...");
    handleCloseNewVehicleModal();
  }

  const getDriverName = (driverId) => {
    if (!driverId) return null;
    const driver = mockDrivers.find(d => d.id === driverId);
    return driver ? driver.name : 'Desconhecido';
  }


  return (
    <div className={styles.driversPage}>
      <Container fluid>
        <header className={styles.pageHeader}>
          <h1 className={styles.pageTitle}>Motoristas e Frota</h1>
          <p className={styles.pageSubtitle}>Gerencie seus motoristas e a alocação de veículos.</p>
        </header>

        <Row className="g-4 mb-4">
          <Col xl={4}><StatCard icon={faUsers} title="Total de Motoristas" value={mockDrivers.length} colorClass="total" /></Col>
          <Col xl={4}><StatCard icon={faUserCheck} title="Motoristas Ativos" value={activeDrivers} colorClass="online" /></Col>
          <Col xl={4}><StatCard icon={faTruck} title="Total de Veículos" value={mockVehicles.length} colorClass="vehicles" /></Col>
        </Row>

        <Row>
          <Col lg={8} className="mb-4 mb-lg-0">
            <Card className={`${styles.mainCard} h-100`}>
              <Card.Header className={styles.cardHeader}>
                <h5 className={styles.cardTitle}>Motoristas Cadastrados</h5>
                <div className={styles.cardHeaderActions}>
                  <div className={styles.searchInputWrapper}>
                    <FontAwesomeIcon icon={faSearch} className={styles.searchIcon} />
                    <Form.Control type="text" placeholder="Buscar motorista..." className={styles.searchInput} />
                  </div>
                  <Button variant="primary" onClick={handleShowNewModal}><FontAwesomeIcon icon={faPlus} className="me-2" />Novo Motorista</Button>
                </div>
              </Card.Header>
              <div className={styles.tableWrapper}>
                <Table hover responsive className={styles.customTable}>
                  <thead>
                    <tr>
                      <th>Nome</th>
                      <th>Veículo Alocado</th>
                      <th>Status</th>
                      <th className="text-center">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockDrivers.map(driver => (
                      <tr key={driver.id}>
                        <td><b>{driver.name}</b><br /><small className="text-muted">CNH: {driver.cnh}</small></td>
                        <td>
                          {driver.vehiclePlate
                            ? <Badge className={styles.plateBadge}>{driver.vehiclePlate}</Badge>
                            : <Badge bg="secondary">Nenhum</Badge>
                          }
                        </td>
                        <td><Badge pill bg={driver.status === 'Ativo' ? 'success' : 'secondary'}>{driver.status}</Badge></td>
                        <td className="text-center">
                          <OverlayTrigger overlay={<Tooltip>Editar</Tooltip>}>
                            <Button variant="light" className={`${styles.actionButton} ${styles.actionButtonEdit}`} onClick={() => handleShowEditModal(driver)}>
                              <FontAwesomeIcon icon={faEdit} />
                            </Button>
                          </OverlayTrigger>
                          <OverlayTrigger overlay={<Tooltip>Excluir</Tooltip>}>
                            <Button variant="light" className={`${styles.actionButton} ${styles.actionButtonDelete}`} onClick={() => handleShowDeleteModal(driver)}>
                              <FontAwesomeIcon icon={faTrashAlt} />
                            </Button>
                          </OverlayTrigger>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Card>
          </Col>

          <Col lg={4}>
            <Card className={`${styles.mainCard} h-100`}>
              <Card.Header className={styles.cardHeader}>
                <h5 className={styles.cardTitle}>Frota de Veículos</h5>
                <Button variant="outline-primary" size="sm" onClick={handleShowNewVehicleModal}><FontAwesomeIcon icon={faPlus} className="me-1" /> Novo</Button>
              </Card.Header>
              <div className={styles.tableWrapper}>
                <Table hover responsive className={styles.customTable}>
                  <thead>
                    <tr>
                      <th>Veículo</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockVehicles.map(vehicle => (
                      <tr key={vehicle.plate}>
                        <td><b>{vehicle.plate}</b><br /><small className="text-muted">{getDriverName(vehicle.driverId) || 'Disponível'}</small></td>
                        <td>
                          <Badge pill bg={vehicle.driverId ? 'success' : 'light'} text={vehicle.driverId ? 'white' : 'dark'}>
                            <FontAwesomeIcon icon={vehicle.driverId ? faCircleCheck : faCircleXmark} className="me-1" />
                            {vehicle.driverId ? 'Em Uso' : 'Livre'}
                          </Badge>
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

      {/* --- MODAIS --- */}
      <Modal show={showNewModal} onHide={handleCloseNewModal} centered>
        <Modal.Header closeButton className={styles.modalHeader}>
          <Modal.Title><FontAwesomeIcon icon={faPlus} className="me-2" />Cadastrar Novo Motorista</Modal.Title>
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
        <Modal.Footer className={styles.modalFooter}>
          <Button variant="secondary" onClick={handleCloseNewModal}>Cancelar</Button>
          <Button variant="primary" onClick={handleCreateDriver}>Salvar</Button>
        </Modal.Footer>
      </Modal>

      {selectedDriver && (
        <Modal show={showEditModal} onHide={handleCloseEditModal} centered>
          <Modal.Header closeButton className={styles.modalHeader}>
            <Modal.Title><FontAwesomeIcon icon={faEdit} className="me-2" />Editar Motorista</Modal.Title>
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
            <Modal.Footer className={styles.modalFooter}>
              <Button variant="secondary" onClick={handleCloseEditModal}>Cancelar</Button>
              <Button variant="primary" onClick={handleSaveChanges}>Salvar Alterações</Button>
            </Modal.Footer>
          </Modal.Body>
        </Modal>
      )}

      {selectedDriver && (
        <Modal show={showDeleteModal} onHide={handleCloseDeleteModal} centered>
          <Modal.Header closeButton className={styles.modalHeader}>
            <Modal.Title><FontAwesomeIcon icon={faTrashAlt} className="me-2" />Confirmar Exclusão</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            Você tem certeza que deseja excluir o motorista <strong>{selectedDriver.name}</strong>?
            <br />
            <small className="text-danger">Esta ação não poderá ser desfeita.</small>
          </Modal.Body>
          <Modal.Footer className={styles.modalFooter}>
            <Button variant="secondary" onClick={handleCloseDeleteModal}>Cancelar</Button>
            <Button variant="danger" onClick={handleDeleteDriver}>Confirmar Exclusão</Button>
          </Modal.Footer>
        </Modal>
      )}

      <Modal show={showNewVehicleModal} onHide={handleCloseNewVehicleModal} centered>
        <Modal.Header closeButton className={styles.modalHeader}>
          <Modal.Title><FontAwesomeIcon icon={faTruck} className="me-2" />Cadastrar Novo Veículo</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="formNewVehiclePlate">
              <Form.Label>Placa do Veículo</Form.Label>
              <Form.Control type="text" placeholder="Ex: ABC-1234" autoFocus />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formNewVehicleName">
              <Form.Label>Nome/Modelo do Veículo</Form.Label>
              <Form.Control type="text" placeholder="Ex: Ônibus 04" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formNewVehicleType">
              <Form.Label>Tipo</Form.Label>
              <Form.Select>
                <option>Ônibus</option>
                <option>Van</option>
                <option>Carro</option>
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className={styles.modalFooter}>
          <Button variant="secondary" onClick={handleCloseNewVehicleModal}>Cancelar</Button>
          <Button variant="primary" onClick={handleCreateVehicle}>Salvar</Button>
        </Modal.Footer>
      </Modal>

    </div>
  );
}

export default Drivers;