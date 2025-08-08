from config import db, app
from flask import Blueprint, jsonify, render_template, request
# from sqlalchemy import select
from datetime import datetime
from models.trajeto import Trajeto
from models.pontoViagem import PontoViagem

view_viagem = Blueprint('view_viagem', __name__)

@view_viagem.route('/', methods=['GET', 'POST'])
def post_new_ponto_viagem():
    """
    Rota para cadastrar um ponto de viagem no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do trajeto.
        - status error se ocorrer exceção.
    """

    if request.method == 'POST':
        data = request.get_json()
        latitude_ponto = data.get('latitude')
        longitude_ponto = data.get('longitude')
        datahora = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S")

        # horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)

        new_ponto_viagem = PontoViagem(
            latitude_ponto=latitude_ponto,
            longitude_ponto=longitude_ponto,
            data=datahora.date(),
            hora=datahora.time()
        )

        try:
            db.session.add(new_ponto_viagem)
            db.session.commit()
            return jsonify({
                "status": "success",
                "message": "Trajeto inserido com sucesso.",
                "trajeto": {
                    "latitude_ponto": new_ponto_viagem.latitude_ponto,
                    "longitude_ponto": new_ponto_viagem.longitude_ponto,
                    "data": new_ponto_viagem.data,
                    "hora": new_ponto_viagem.hora
                }
            }), 201
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Erro ao inserir novo ponto de viagem: {str(e)}"
            }), 400