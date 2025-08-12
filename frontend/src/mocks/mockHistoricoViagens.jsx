// Cada objeto representa um relatório de uma viagem específica
export const mockHistoricoViagens = [
    {
        // ROTA 1
        id: 'VIAGEM-001',
        placa: 'ONB-001',
        motorista: 'Carlos Silva',
        data: '2025-07-19',
        pontos: [
            { lat: -6.255, lng: -36.520, timestamp: '2025-07-19T08:00:00Z' },
            { lat: -6.257, lng: -36.522, timestamp: '2025-07-19T08:02:00Z' },
            { lat: -6.259, lng: -36.525, timestamp: '2025-07-19T08:05:00Z' },
            { lat: -6.261, lng: -36.528, timestamp: '2025-07-19T08:08:00Z' },
        ],
    },
    {
        // --- ROTA 2 ATUALIZADA (TRAJETO PELO CENTRO DA CIDADE) ---
        id: 'VIAGEM-002',
        placa: 'VAN-002',
        motorista: 'Ana Souza',
        data: '2025-07-19',
        pontos: [
            { lat: -6.258, lng: -36.536, timestamp: '2025-07-19T09:15:00Z' }, // Ponto inicial (Ex: Av. Cel. José Bezerra)
            { lat: -6.259, lng: -36.533, timestamp: '2025-07-19T09:18:00Z' }, // Entrando na área central
            { lat: -6.256, lng: -36.530, timestamp: '2025-07-19T09:22:00Z' }, // Ponto central (Ex: Perto da Praça Cristo Rei)
            { lat: -6.254, lng: -36.527, timestamp: '2025-07-19T09:25:00Z' }, // Ponto final (Ex: Perto da Matriz de Sant'Ana)
        ],
    },
    {
        // ROTA 3
        id: 'VIAGEM-003',
        placa: 'ONB-001',
        motorista: 'Carlos Silva',
        data: '2025-07-18',
        pontos: [
            { lat: -6.2480, lng: -36.5190, timestamp: '2025-07-18T14:30:00Z' },
            { lat: -6.2550, lng: -36.5245, timestamp: '2025-07-18T14:35:00Z' },
            { lat: -6.2585, lng: -36.5330, timestamp: '2025-07-18T14:40:00Z' },
            { lat: -6.2650, lng: -36.5390, timestamp: '2025-07-18T14:45:00Z' },
        ],
    },
];