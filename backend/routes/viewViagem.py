from config import db, app
from flask import Blueprint, jsonify, render_template, request
# from sqlalchemy import select
# from datetime import datetime
from models.trajeto import Trajeto
from models.pontoTrajeto import PontoTrajeto

view_viagem = Blueprint('view_viagem', __name__)

@view_viagem.route('/', methods=['GET', 'POST'])
def post_new_ponto_viagem():
    """
    Rota para cadastrar um ponto de trajeto no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do trajeto.
        - status error se ocorrer exceção.
    """

    if request.method == 'POST':
        data = request.get_json()
        id_trajeto = data.get('id-trajeto')

        try:
            trajeto_desejado = Trajeto.query.filter_by(trajeto_id=id_trajeto).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400
        
        if trajeto_desejado:
            
            latitude_ponto = data.get('latitude')
            longitude_ponto = data.get('longitude')
            tipo_ponto = data.get('tipo-ponto')

            try:
                new_ponto_trajeto = PontoTrajeto(
                latitude_ponto=latitude_ponto,
                longitude_ponto=longitude_ponto,
                tipo_ponto=tipo_ponto
                )

                trajeto_desejado.trajeto_ponto.append(new_ponto_trajeto)

                db.session.add(new_ponto_trajeto)
                db.session.commit()

                return jsonify({
                    "status": "success",
                    "message": "Trajeto inserido com sucesso.",
                    "trajeto": {
                        "latitude_ponto": new_ponto_trajeto.latitude_ponto,
                        "longitude_ponto": new_ponto_trajeto.longitude_ponto,
                        "tipo": new_ponto_trajeto.tipo_ponto
                    }
                }), 201
        
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": f"Erro ao inserir novo ponto de trajeto: {str(e)}"
                }), 400

        else:
            return jsonify({
                "status":"not found",
                "message":"o trajeto desejado nao existe"
            }), 404
        
    return render_template('pagina_cadastrar_ponto_trajeto.html'), 302

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
