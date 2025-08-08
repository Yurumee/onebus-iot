from config import db, app
from flask import Blueprint, jsonify, render_template, request
# from sqlalchemy import select
from datetime import datetime
# from models.trajeto import Trajeto
from models.carro import Carro
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
        placa_carro = data.get('placa-carro')
        datahora = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S")

        # horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)

        new_ponto_viagem = PontoViagem(
            latitude_ponto=latitude_ponto,
            longitude_ponto=longitude_ponto,
            data=datahora.date(),
            hora=datahora.time()
        )

        try:
            carro_desejado = Carro.query.filter_by(placa=placa_carro).first()
            carro_desejado.viagem_pontos.append(new_ponto_viagem)

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
        
    return render_template('pagina_cadastrar_ponto_viagem.html'), 302

@view_viagem.route('/alterar-ponto', methods=['GET', 'PATCH'])
def edit_ponto_viagem():
    """
    Rota para editar um ponto de viagem específico com o id informado

    Método:
        Get, Patch

    Retorno:
        Página mostrando ponto editado
    """
    if request.method == 'PATCH':
        data = request.get_json()
        id_ponto = data.get('id-ponto-viagem')
        ponto_desejado = PontoViagem.query.filter_by(id_ponto_viagem=id_ponto).first()

        if ponto_desejado:
            latitude_ponto = data.get('latitude')
            longitude_ponto = data.get('longitude')
            new_placa = data.get('placa-carro')
            datahora = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S")

            if latitude_ponto != ponto_desejado.latitude_ponto and latitude_ponto != None:
                ponto_desejado.latitude_ponto = latitude_ponto
                db.session.commit()
            
            if longitude_ponto != ponto_desejado.longitude_ponto and longitude_ponto != None:
                ponto_desejado.longitude_ponto = longitude_ponto
                db.session.commit()

            if datahora.date() != ponto_desejado.data and datahora.date() != None:
                ponto_desejado.data = datahora.date()
                db.session.commit()

            if datahora.time() != ponto_desejado.hora and datahora.time() != None:
                ponto_desejado.hora = datahora.time()
                db.session.commit()

            if new_placa != ponto_desejado.placa_carro and new_placa != None:
                carro_desejado = Carro.query.filter_by(placa=new_placa).first()

                if carro_desejado:
                    carro_desejado.viagem_pontos.append(ponto_desejado)
                    db.session.commit()

                else:
                    return jsonify({
                        "status":"not found",
                        "message":"carro nao encontrado"
                    }), 404
            
            return jsonify({
                "status":"success",
                "message":"updates realizados com sucesso"
            }), 200
        
        else:
            return jsonify({
                "status":"not found",
                "message":"ponto nao encontrado"
            }), 404


    return render_template('editar_ponto_viagem.html'), 302
