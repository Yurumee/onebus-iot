from config import db
from flask import Blueprint, jsonify, request, render_template
from models.carro import Carro
from models.motorista import Motorista
from models.trajeto import Trajeto
from models.pontoViagem import PontoViagem

view_carro = Blueprint('view_carro', __name__)

@view_carro.route('/', methods=['GET', 'POST'])
def post_new_car():
    """
    Rota para cadastrar carros no banco de dados.

    Método:
        GET, POST

    Retorno:
        carros cadastrados no banco de dados
    
    """
    if request.method == 'POST':
        data = request.get_json()
        placa_carro = data.get('placa-carro')
        tipo_carro = data.get('tipo-veiculo')
        
        try:
            carro_existente = Carro.query.filter_by(placa=placa_carro).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400
        
        if carro_existente:
            return jsonify({
                "status":"error",
                "message":"carro ja cadastrado"
            }), 409
        
        else:
            novo_carro = Carro(
                placa=placa_carro,
                tipo_veiculo=tipo_carro
            )

            if data.get('longitude-atual') and data.get('latitude-atual'):
                novo_carro.longitude_atual = data.get('longitude-atual')
                novo_carro.latitude_atual = data.get('latitude-atual')
            
            try:
                db.session.add(novo_carro)
                db.session.commit()

            except Exception as e:
                return jsonify({
                "status":"error",
                "message":f"erro ao inserir no banco de dados: {str(e)}"
                }), 400
            
            return jsonify({
                "status":"success",
                "message":"carro cadastrado com sucesso"
                }), 201
    
    return render_template('pagina_inserir_carro.html'), 302

@view_carro.route('/alterar-carro', methods=['GET', 'PATCH'])
def edit_carro():

    if request.method == 'PATCH':
        data = request.get_json()
        placa = data.get('placa-carro')

        try:
            carro_desejado = Carro.query.filter_by(placa=placa).first()
        except Exception as e:
            return  jsonify({
                "status":"error",
                "message":f"houve um erro {str(e)}"
            })
        
        if carro_desejado:
            new_placa = data.get('new-placa-carro')
            new_tipo_veiculo = data.get('tipo-veiculo')

            if new_placa != carro_desejado.placa and new_placa != None:
                trajetos = db.session.query(Trajeto).where(Trajeto.carro_placa == carro_desejado.placa)
                motoristas = db.session.query(Motorista).where(Motorista.carro_placa == carro_desejado.placa)
                carro_desejado.placa = new_placa

                for motorista in motoristas:
                    # motorista.carro_placa = new_placa
                    carro_desejado.motorista_cnh.append(motorista)
                
                for trajeto in trajetos:
                    carro_desejado.trajeto.append(trajeto)

                db.session.commit()

            if new_tipo_veiculo != carro_desejado.tipo_veiculo and new_tipo_veiculo != None:
                carro_desejado.tipo_veiculo = new_tipo_veiculo
                db.session.commit()

            return jsonify({
                "status":"success",
                "message":"updates realizados com sucesso"
            }), 200

        else:
            return jsonify({
                "status":"not found",
                "message":"carro nao encontrado"
            }), 404
    
    return render_template('pagina_editar_motorista.html'), 302

@view_carro.route('/excluir-carro', methods=['GET', 'DELETE'])
def delete_carro():
    
    if request.method == 'DELETE':
        # delete from motoristas
        # delete from trajetos
        # delete from pontos de trajeto

        data = request.get_json()
        placa_carro = data.get('placa-carro')

        try:
            carro_desejado = Carro.query.filter_by(placa=placa_carro).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400

        if carro_desejado:
            try:
                db.session.query(Trajeto).where(Trajeto.carro_placa == placa_carro).delete()
                db.session.query(PontoViagem).where(PontoViagem.carro_placa == placa_carro).delete()
                Carro.query.filter_by(placa=placa_carro).delete()
            
            except Exception as e:
                return jsonify({
                "status":"error",
                "message":f"houve um erro {str(e)}"
            }), 400

            return jsonify({
                "status":"deleted",
                "message":"carro deletado com sucesso"
            }), 200

        else:
            return jsonify({
                "status":"not found",
                "message":"carro nao encontrado"
            }), 404
    
    return render_template('pagina_deletar_carro.html'), 302