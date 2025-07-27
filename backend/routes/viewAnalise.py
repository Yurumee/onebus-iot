from flask import Blueprint, jsonify
from config import db
from models.carro import Carro
from models.motorista import Motorista
from models.trajeto import Trajeto
from models.pontoTrajeto import PontoTrajeto
import datetime
import random

view_analise = Blueprint('view_analise', __name__)

@view_analise.route('/gerar-dados-teste/<int:pontos>', methods=['POST'])
def gerar_dados_teste(pontos):
    """
    Rota de teste para simular um cenário completo:
    1. Cria um carro e um motorista (se não existirem).
    2. Associa o motorista ao carro.
    3. Cria um novo trajeto para o carro.
    4. Gera uma quantidade definida de pontos para esse trajeto.
    
    Parâmetro na URL:
        - pontos: a quantidade de pontos de trajeto a serem gerados.
    """
    try:
        # --- 1. Obter ou Criar Carro ---
        placa_teste = 'TESTE001'
        carro = db.session.query(Carro).filter_by(placa=placa_teste).first()
        if not carro:
            carro = Carro(placa=placa_teste, tipoVeiculo='Van de Teste')
            db.session.add(carro)

        # --- 2. Obter ou Criar Motorista ---
        cnh_teste = 1122334455
        motorista = db.session.query(Motorista).filter_by(cnh=cnh_teste).first()
        if not motorista:
            motorista = Motorista(
                cnh=cnh_teste,
                cpf='111.222.333-44',
                nomeCompleto='Motorista de Teste',
                senha='teste',
                tipoUsuario='motorista'
            )
            db.session.add(motorista)

        # Persiste o carro e o motorista para poder associá-los
        db.session.commit()

        # --- 3. Associar Motorista ao Carro ---
        # Lógica corrigida para seguir o modelo de relação 1-N
        if motorista not in carro.motorista_cnh:
            carro.motorista_cnh.append(motorista)
            
        # --- 4. Criar um novo Trajeto ---
        novo_trajeto = Trajeto(
            servicoPrestado="Saúde (Teste)",
            pontoOrigem="Currais Novos",
            pontoDestino="Natal",
            carro_placa=carro.placa,  # Associa o trajeto ao carro
            horarioEstimado=datetime.datetime.now().time()
        )
        db.session.add(novo_trajeto)
        
        # Persiste a associação e o novo trajeto
        db.session.commit()

        # --- 5. Gerar Pontos para o Trajeto ---
        pontos_gerados_coords = []
        base_lat = -5.9844
        base_lon = -36.5333

        for _ in range(pontos):
            ponto = PontoTrajeto(
                latitude=str(base_lat + (random.random() - 0.5) * 0.1),
                longitude=str(base_lon + (random.random() - 0.5) * 0.1),
                trajeto_id=novo_trajeto.idTrajeto # Associa o ponto ao trajeto
            )
            db.session.add(ponto)
            pontos_gerados_coords.append({
                "latitude": ponto.latitude,
                "longitude": ponto.longitude
            })
        
        # Persiste todos os novos pontos de uma vez para melhor performance
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"{pontos} pontos de teste gerados com sucesso.",
            "carro_placa": carro.placa,
            "motorista_cnh": motorista.cnh,
            "trajeto_id": novo_trajeto.idTrajeto,
            "primeiro_ponto": pontos_gerados_coords[0] if pontos_gerados_coords else None
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"Erro durante a geração de dados de teste: {str(e)}"
        }), 500