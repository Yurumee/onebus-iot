from config import db, app
from flask import Blueprint, jsonify
from models.Carro import Carro

view_carro = Blueprint('view_carro', __name__)

@app.route('/carro', methods=['GET', 'POST'])
def post_new_car():
    MOCKarro = Carro(
        idEmbarcado = 'abc123',
        placa = '4N4L1C3', 
        tipoVeiculo = 'Carro'
    )

    try:
        db.session.add(MOCKarro)
        db.session.commit()
    except Exception as e:
        return jsonify(e)
    
    return 'Carro cadastrado!'