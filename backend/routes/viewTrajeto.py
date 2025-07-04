from config import db, app
from flask import Blueprint, jsonify
from datetime import datetime
from models.Trajeto import Trajeto
from models.Motorista import Motorista

view_trajeto = Blueprint('view_trajeto', __name__)

@app.route('/trajeto', methods=['GET', 'POST'])
def post_new_route():

    horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)
    horarioFim = datetime(year=2025, month=7, day=4, hour=19, minute=30, second=0)
    MOCKTrajeto = Trajeto(
        servicoPrestado = 'Saúde',
        origem = 'Cerro Corá',
        destino = 'Currais Novos',
        kmEstimado = 40,
        horarioInicio = horarioComeco.time(),
        horarioFim = horarioFim.time(),
        motoristaResp = 1234567890,
        idEmbarcado = 'abc123'
    )

    try:
        db.session.add(MOCKTrajeto)
        db.session.commit()
    except Exception as e:
        return f'{e}'
    
    return 'Trajeto inserido!'

@app.route('/get-trajeto', methods=['GET'])
def get_trajeto():
    try:
        teste = Trajeto.query.join(
            Motorista, Trajeto.motoristaResp == Motorista.CNH
        )
    except Exception as e:
        return f'{e}'
    
    return teste

