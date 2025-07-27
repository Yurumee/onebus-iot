from config import db, app
from flask import Blueprint, jsonify, render_template
# from sqlalchemy import select
from datetime import datetime
from models.trajeto import Trajeto
from models.pontoViagem import PontoViagem

view_viagem = Blueprint('view_viagem', __name__)

@view_viagem.route('/', methods=['GET', 'POST'])
def post_ponto_viagem():
    """
    Rota para cadastrar um ponto de viagem mockado no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do trajeto.
        - status error se ocorrer exceção.
    """
    horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)
    
    MOCKPontoV = PontoViagem(
        latitudePonto='10.000001',
        longitudePonto='-11.000002',
        data=horarioComeco.date(),
        hora=horarioComeco.time()
        # motoristaResp=1234567890,      # Descomente se o campo existir no modelo
        # idEmbarcado='abc123'           # Descomente se o campo existir no modelo
    )

    try:
        db.session.add(MOCKPontoV)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Trajeto inserido com sucesso.",
            "trajeto": {
                "latitudePonto": MOCKPontoV.latitudePonto,
                "longitudePonto": MOCKPontoV.longitudePonto,
                "data": MOCKPontoV.data,
                "hora": MOCKPontoV.hora,
                # "horarioEstimado": str(MOCKPontoV.horarioEstimado)
                # "motoristaResp": MOCKTrajeto.motoristaResp,   # Inclua se existir
                # "idEmbarcado": MOCKTrajeto.idEmbarcado        # Inclua se existir
            }
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400