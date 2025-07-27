import React, { useState } from 'react';
import { Container, Row, Col, Card, Table, Button, Badge, Form, Modal, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRoute, faClock, faCheckCircle, faSearch, faEdit, faTrashAlt, faPlus } from '@fortawesome/free-solid-svg-icons';

import styles from './Routes.module.css';

// --- Dados Mockados ---
const mockRoutes = [
  { id: 'R01', origin: 'Currais Novos', destination: 'Natal', time: '07:00', service: 'Saúde', vehiclePlate: 'ONB-001', status: 'Agendada' },
  { id: 'R02', origin: 'Lagoa Nova', destination: 'Currais Novos', time: '08:30', service: 'Educação', vehiclePlate: 'VAN-001', status: 'Em Andamento' },
  { id: 'R03', origin: 'Parelhas', destination: 'Caicó', time: '09:00', service: 'Administrativo', vehiclePlate: 'ONB-002', status: 'Concluída' },
  { id: 'R04', origin: 'Acari', destination: 'Natal', time: '13:00', service: 'Saúde', vehiclePlate: 'ONB-003', status: 'Agendada' },
  { id: 'R05', origin: 'Currais Novos', destination: 'Lagoa Nova', time: '17:00', service: 'Educação', vehiclePlate: 'VAN-001', status: 'Concluída' },
];

const mockVehicles = [
  { plate: 'ONB-001', name: 'Ônibus 01' },
  { plate: 'ONB-002', name: 'Ônibus 02' },
  { plate: 'ONB-003', name: 'Ônibus 03' },
  { plate: 'VAN-001', name: 'Van 01' },
  { plate: 'VAN-002', name: 'Van 02 (Disponível)' },
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

function RoutesPage() {
  const scheduledRoutes = mockRoutes.filter(r => r.status === 'Agendada').length;
  const completedRoutes = mockRoutes.filter(r => r.status === 'Concluída').length;

  const [showNewModal, setShowNewModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedRoute, setSelectedRoute] = useState(null);

  const handleShowNewModal = () => setShowNewModal(true);
  const handleCloseNewModal = () => setShowNewModal(false);

  const handleShowEditModal = (route) => {
    setSelectedRoute(route);
    setShowEditModal(true);
  };
  const handleCloseEditModal = () => {
    setShowEditModal(false);
    setSelectedRoute(null);
  };

  const handleShowDeleteModal = (route) => {
    setSelectedRoute(route);
    setShowDeleteModal(true);
  };
  const handleCloseDeleteModal = () => {
    setShowDeleteModal(false);
    setSelectedRoute(null);
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Agendada': return 'primary';
      case 'Em Andamento': return 'warning';
      case 'Concluída': return 'success';
      default: return 'secondary';
    }
  }

  return (
    <div className={styles.routesPage}>
      <Container fluid>
        <header className={styles.pageHeader}>
          <h1 className={styles.pageTitle}>Gerenciamento de Rotas</h1>
          <p className={styles.pageSubtitle}>Planeje, visualize e administre as rotas dos veículos.</p>
        </header>

        <Row className="g-4 mb-4">
          <Col xl={4}><StatCard icon={faRoute} title="Total de Rotas" value={mockRoutes.length} colorClass="total" /></Col>
          <Col xl={4}><StatCard icon={faClock} title="Rotas Agendadas" value={scheduledRoutes} colorClass="online" /></Col>
          <Col xl={4}><StatCard icon={faCheckCircle} title="Rotas Concluídas" value={completedRoutes} colorClass="vehicles" /></Col>
        </Row>

        <Row>
          <Col>
            <Card className={`${styles.mainCard} h-100`}>
              <Card.Header className={styles.cardHeader}>
                <h5 className={styles.cardTitle}>Rotas Programadas</h5>
                <div className={styles.cardHeaderActions}>
                  <div className={styles.searchInputWrapper}>
                    <FontAwesomeIcon icon={faSearch} className={styles.searchIcon} />
                    <Form.Control type="text" placeholder="Buscar por origem, destino..." className={styles.searchInput} />
                  </div>
                  <Button variant="primary" onClick={handleShowNewModal}><FontAwesomeIcon icon={faPlus} className="me-2" />Nova Rota</Button>
                </div>
              </Card.Header>
              <div className={styles.tableWrapper}>
                <Table hover responsive className={styles.customTable}>
                  <thead>
                    <tr>
                      <th>Rota</th>
                      <th>Veículo</th>
                      <th>Horário</th>
                      <th>Serviço</th>
                      <th>Status</th>
                      <th className="text-center">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockRoutes.map(route => (
                      <tr key={route.id}>
                        <td><b>{route.origin}</b> &rarr; <b>{route.destination}</b></td>
                        <td>
                          {route.vehiclePlate
                            ? <Badge className={styles.plateBadge}>{route.vehiclePlate}</Badge>
                            : <Badge bg="secondary">N/A</Badge>
                          }
                        </td>
                        <td>{route.time}</td>
                        <td>{route.service}</td>
                        <td><Badge pill bg={getStatusBadge(route.status)}>{route.status}</Badge></td>
                        <td className="text-center">
                          <OverlayTrigger overlay={<Tooltip>Editar</Tooltip>}>
                            <Button variant="light" className={`${styles.actionButton} ${styles.actionButtonEdit}`} onClick={() => handleShowEditModal(route)}>
                              <FontAwesomeIcon icon={faEdit} />
                            </Button>
                          </OverlayTrigger>
                          <OverlayTrigger overlay={<Tooltip>Excluir</Tooltip>}>
                            <Button variant="light" className={`${styles.actionButton} ${styles.actionButtonDelete}`} onClick={() => handleShowDeleteModal(route)}>
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
        </Row>
      </Container>

      {/* --- MODAIS --- */}
      <Modal show={showNewModal} onHide={handleCloseNewModal} centered>
        <Modal.Header closeButton className={styles.modalHeader}>
          <Modal.Title><FontAwesomeIcon icon={faPlus} className="me-2" />Cadastrar Nova Rota</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Row>
              <Col>
                <Form.Group className="mb-3" controlId="formNewRouteOrigin">
                  <Form.Label>Origem</Form.Label>
                  <Form.Control type="text" placeholder="Cidade de Origem" autoFocus />
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formNewRouteDestination">
                  <Form.Label>Destino</Form.Label>
                  <Form.Control type="text" placeholder="Cidade de Destino" />
                </Form.Group>
              </Col>
            </Row>
            <Form.Group className="mb-3" controlId="formNewRouteVehicle">
              <Form.Label>Veículo</Form.Label>
              <Form.Select>
                <option>Selecione um veículo</option>
                {mockVehicles.map(v => <option key={v.plate} value={v.plate}>{v.name} ({v.plate})</option>)}
              </Form.Select>
            </Form.Group>
            <Row>
              <Col>
                <Form.Group className="mb-3" controlId="formNewRouteTime">
                  <Form.Label>Horário Estimado</Form.Label>
                  <Form.Control type="time" />
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formNewRouteService">
                  <Form.Label>Tipo de Serviço</Form.Label>
                  <Form.Select>
                    <option>Saúde</option>
                    <option>Educação</option>
                    <option>Administrativo</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>
          </Form>
        </Modal.Body>
        <Modal.Footer className={styles.modalFooter}>
          <Button variant="secondary" onClick={handleCloseNewModal}>Cancelar</Button>
          <Button variant="primary" onClick={handleCloseNewModal}>Salvar</Button>
        </Modal.Footer>
      </Modal>

      {selectedRoute && (
        <Modal show={showEditModal} onHide={handleCloseEditModal} centered>
          <Modal.Header closeButton className={styles.modalHeader}>
            <Modal.Title><FontAwesomeIcon icon={faEdit} className="me-2" />Editar Rota</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Row>
                <Col>
                  <Form.Group className="mb-3" controlId="formEditRouteOrigin">
                    <Form.Label>Origem</Form.Label>
                    <Form.Control type="text" defaultValue={selectedRoute.origin} autoFocus />
                  </Form.Group>
                </Col>
                <Col>
                  <Form.Group className="mb-3" controlId="formEditRouteDestination">
                    <Form.Label>Destino</Form.Label>
                    <Form.Control type="text" defaultValue={selectedRoute.destination} />
                  </Form.Group>
                </Col>
              </Row>
              <Form.Group className="mb-3" controlId="formEditRouteVehicle">
                <Form.Label>Veículo</Form.Label>
                <Form.Select defaultValue={selectedRoute.vehiclePlate}>
                  {mockVehicles.map(v => <option key={v.plate} value={v.plate}>{v.name} ({v.plate})</option>)}
                </Form.Select>
              </Form.Group>
              <Row>
                <Col>
                  <Form.Group className="mb-3" controlId="formEditRouteTime">
                    <Form.Label>Horário Estimado</Form.Label>
                    <Form.Control type="time" defaultValue={selectedRoute.time} />
                  </Form.Group>
                </Col>
                <Col>
                  <Form.Group className="mb-3" controlId="formEditRouteService">
                    <Form.Label>Tipo de Serviço</Form.Label>
                    <Form.Select defaultValue={selectedRoute.service}>
                      <option>Saúde</option>
                      <option>Educação</option>
                      <option>Administrativo</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
              </Row>
              <Form.Group className="mb-3" controlId="formEditRouteStatus">
                <Form.Label>Status</Form.Label>
                <Form.Select defaultValue={selectedRoute.status}>
                  <option>Agendada</option>
                  <option>Em Andamento</option>
                  <option>Concluída</option>
                  <option>Cancelada</option>
                </Form.Select>
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer className={styles.modalFooter}>
            <Button variant="secondary" onClick={handleCloseEditModal}>Cancelar</Button>
            <Button variant="primary" onClick={handleCloseEditModal}>Salvar Alterações</Button>
          </Modal.Footer>
        </Modal>
      )}

      {selectedRoute && (
        <Modal show={showDeleteModal} onHide={handleCloseDeleteModal} centered>
          <Modal.Header closeButton className={styles.modalHeader}>
            <Modal.Title><FontAwesomeIcon icon={faTrashAlt} className="me-2" />Confirmar Exclusão</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            Você tem certeza que deseja excluir a rota de <strong>{selectedRoute.origin}</strong> para <strong>{selectedRoute.destination}</strong>?
            <br />
            <small className="text-danger">Esta ação não poderá ser desfeita.</small>
          </Modal.Body>
          <Modal.Footer className={styles.modalFooter}>
            <Button variant="secondary" onClick={handleCloseDeleteModal}>Cancelar</Button>
            <Button variant="danger" onClick={handleCloseDeleteModal}>Confirmar Exclusão</Button>
          </Modal.Footer>
        </Modal>
      )}
    </div>
  );
}

export default RoutesPage;