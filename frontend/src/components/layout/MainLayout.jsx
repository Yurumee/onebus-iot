// src/components/layout/MainLayout.jsx

import React from 'react';
import { Outlet, Link } from 'react-router-dom';

// Estilos inline para simplicidade inicial
const styles = {
  layout: {
    display: 'flex',
    minHeight: '100vh',
  },
  sidebar: {
    width: '240px',
    backgroundColor: '#f4f4f4',
    padding: '20px',
    borderRight: '1px solid #ddd',
  },
  content: {
    flexGrow: 1,
    padding: '20px',
  },
  navLink: {
    display: 'block',
    margin: '10px 0',
    textDecoration: 'none',
    color: '#333',
    fontWeight: 'bold',
  }
};

function MainLayout() {
  return (
    <div style={styles.layout}>
      <aside style={styles.sidebar}>
        <h2>OneBus</h2>
        <nav>
          <Link to="/dashboard" style={styles.navLink}>Dashboard</Link>
          <Link to="/rotas" style={styles.navLink}>Rotas</Link>
          <Link to="/motoristas" style={styles.navLink}>Motoristas</Link>
        </nav>
      </aside>
      <main style={styles.content}>
        <Outlet /> {/* O conteúdo da rota atual será renderizado aqui */}
      </main>
    </div>
  );
}

export default MainLayout;