// src/pages/Login.jsx

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Form, Container, Row, Col, Card, InputGroup } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBus, faUser, faLock } from '@fortawesome/free-solid-svg-icons';

// Importando o nosso CSS customizado para esta página
import './Login.css';

function Login() {
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Tentativa de login...');
        navigate('/dashboard');
    };

    return (
        <div className="login-page-container">
            <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
                <Row className="w-100">
                    <Col md={{ span: 6, offset: 3 }} lg={{ span: 4, offset: 4 }}>
                        <Card className="login-card p-3">
                            <Card.Body>
                                <div className="login-header">
                                    <div className="app-logo">
                                        <FontAwesomeIcon icon={faBus} className="app-logo-icon" />
                                        <span className="app-logo-text">OneBus</span>
                                    </div>
                                </div>

                                <Form onSubmit={handleSubmit}>
                                    <Form.Group className="mb-3" controlId="formUsername">
                                        <Form.Label>Usuário</Form.Label>
                                        <InputGroup>
                                            <Form.Control type="text" placeholder="Seu nome de usuário" required className="border-end-0" />
                                            <InputGroup.Text>
                                                <FontAwesomeIcon icon={faUser} />
                                            </InputGroup.Text>
                                        </InputGroup>
                                    </Form.Group>

                                    <Form.Group className="mb-4" controlId="formPassword">
                                        <Form.Label>Senha</Form.Label>
                                        <InputGroup>
                                            <Form.Control type="password" placeholder="Sua senha" required className="border-end-0" />
                                            <InputGroup.Text>
                                                <FontAwesomeIcon icon={faLock} />
                                            </InputGroup.Text>
                                        </InputGroup>
                                    </Form.Group>

                                    <div className="d-grid mt-3">
                                        <Button variant="primary" type="submit">
                                            Entrar
                                        </Button>
                                    </div>
                                </Form>

                                <div className="login-footer">
                                    <a href="#" className="forgot-password-link">Esqueceu sua senha?</a>
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default Login;