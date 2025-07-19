// src/App.jsx

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Importe o novo layout
import MainLayout from './components/layout/MainLayout';

// Importe suas páginas
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import RoutesPage from './pages/Routes';
import Drivers from './pages/Drivers';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota de Login não usa o MainLayout */}
        <Route path="/" element={<Login />} />

        {/* Rotas que USAM o MainLayout */}
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/rotas" element={<RoutesPage />} />
          <Route path="/motoristas" element={<Drivers />} />
        </Route>
        
        {/* Você pode adicionar outras rotas aqui, como uma página 404 */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;