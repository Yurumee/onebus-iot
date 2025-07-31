// src/components/layout/MainLayout.jsx

import React, { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTachometerAlt, faRoute, faUsers, faAngleLeft, faBus } from '@fortawesome/free-solid-svg-icons';

import styles from './MainLayout.module.css';

function MainLayout() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={styles.layout}>
      <aside className={`${styles.sidebar} ${isCollapsed ? styles.collapsed : ''}`}>

        <header className={styles.sidebarHeader}>
          <div className={styles.sidebarLogo}>
            <div className={styles.sidebarLogoIcon}>
              <FontAwesomeIcon icon={faBus} />
            </div>
            <span className={styles.sidebarLogoText}>OneBus</span>
          </div>
          {/* O BOTÃO VOLTOU PARA DENTRO DO HEADER */}
          <button className={styles.toggleBtn} onClick={toggleSidebar}>
            <FontAwesomeIcon
              icon={faAngleLeft}
              style={{
                transform: isCollapsed ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.3s ease'
              }}
            />
          </button>
        </header>

        <nav className={styles.sidebarMenu}>
          <NavLink to="/dashboard" className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}>
            <div className={styles.menuIcon}>
              <FontAwesomeIcon icon={faTachometerAlt} />
            </div>
            <span className={styles.menuText}>Dashboard</span>
          </NavLink>
          <NavLink to="/rotas" className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}>
            <div className={styles.menuIcon}>
              <FontAwesomeIcon icon={faRoute} />
            </div>
            <span className={styles.menuText}>Rotas</span>
          </NavLink>
          <NavLink to="/motoristas" className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}>
            <div className={styles.menuIcon}>
              <FontAwesomeIcon icon={faUsers} />
            </div>
            <span className={styles.menuText}>Motoristas</span>
          </NavLink>
        </nav>

      </aside>

      <main className={`${styles.mainContent} ${isCollapsed ? styles.expanded : ''}`}>
        <Outlet />
      </main>
    </div>
  );
}

export default MainLayout;