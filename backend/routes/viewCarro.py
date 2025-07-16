from config import db, app
from flask import Blueprint, jsonify
from models.carro import Carro

view_carro = Blueprint('view_carro', __name__)

@app.route('/carro', methods=['GET', 'POST'])
def post_new_car():
    MOCKarro = Carro(
        placa = '4N4L1C3', 
        tipoVeiculo = 'Carro'
    )

    MOCKarro2 = Carro(
        placa = 'S54NT05', 
        tipoVeiculo = 'Van'
    )

    # try:
    db.session.add(MOCKarro)
    db.session.add(MOCKarro2)
    db.session.commit()
    # except Exception as e:
    #     return e
    
    return 'Carro cadastrado!'