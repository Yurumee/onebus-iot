// Cada objeto representa um relatório de uma viagem específica
export const mockHistoricoViagens = [
  {
    id: 'VIAGEM-001',
    placa: 'ONB-001',
    motorista: 'Carlos Silva',
    data: '2025-08-10',
    // Pontos GPS da viagem
    pontos: [
      { lat: -6.255, lng: -36.520, timestamp: '2025-08-10T08:00:00Z' },
      { lat: -6.257, lng: -36.522, timestamp: '2025-08-10T08:02:00Z' },
      { lat: -6.259, lng: -36.525, timestamp: '2025-08-10T08:05:00Z' },
      { lat: -6.261, lng: -36.528, timestamp: '2025-08-10T08:08:00Z' },
    ],
  },
  {
    id: 'VIAGEM-002',
    placa: 'VAN-002',
    motorista: 'Ana Souza',
    data: '2025-08-10',
    pontos: [
      { lat: -6.280, lng: -36.531, timestamp: '2025-08-10T09:15:00Z' },
      { lat: -6.282, lng: -36.533, timestamp: '2025-08-10T09:18:00Z' },
      { lat: -6.285, lng: -36.535, timestamp: '2025-08-10T09:22:00Z' },
    ],
  },
  {
    id: 'VIAGEM-003',
    placa: 'ONB-001',
    motorista: 'Carlos Silva',
    data: '2025-08-09',
    pontos: [
      { lat: -6.275, lng: -36.510, timestamp: '2025-08-09T14:30:00Z' },
      { lat: -6.273, lng: -36.512, timestamp: '2025-08-09T14:33:00Z' },
      { lat: -6.270, lng: -36.515, timestamp: '2025-08-09T14:37:00Z' },
    ],
  },
];