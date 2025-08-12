from config import db
from flask import Blueprint, jsonify, request, render_template
from models.carro import Carro
from models.motorista import Motorista
from models.trajeto import Trajeto
from models.pontoViagem import PontoViagem
from models.trajetos_cidadaos import TrajetosCidadaos

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
            }), 500
        
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

            if data.get('longitude') and data.get('latitude'):
                novo_carro.longitude_atual = data.get('longitude')
                novo_carro.latitude_atual = data.get('latitude')
            
            try:
                db.session.add(novo_carro)
                db.session.commit()

            except Exception as e:
                return jsonify({
                "status":"error",
                "message":f"erro ao inserir no banco de dados: {str(e)}"
                }), 500
            
            return jsonify({
                "status":"created"
            }), 201
    
    # return render_template('pagina_inserir_carro.html'), 302

@view_carro.route('/todos', methods=['GET'])
def get_carro():
    """
    Rota para mostrar todos os carros

    Método:
        Get

    Retorno:
        Página listando todos os carros
    """
    try:
        carros = Carro.query.all()

    except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500
    
    # DEBUG
    resposta_json = {}

    for carro in carros:
        resposta_json[carro.placa] = {"placa":carro.placa, "latitude atual":carro.latitude_atual, "longitude atual":carro.longitude_atual, "tipo veiculo":carro.tipo_veiculo}

    return jsonify({
        "status":"success",
        "data":resposta_json
        }), 200
    # return render_template('todos_carros.html', all_carros=carros), 302

@view_carro.route('/carro-especifico', methods=['GET', 'POST'])
def get_especific_carro():
    """
    Rota para mostrar um carro especifico pela placa informada

    Método:
        Get

    Retorno:
        Página listando carro especifico
    """

    data = request.get_json()
    placa_desejada = data.get('placa-carro')

    try:
        carro = Carro.query.filter_by(placa=placa_desejada).first()
    
    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    if carro:
        resposta_json = {"placa":carro.placa, 
                         "latitude atual":carro.latitude_atual, 
                         "longitude atual":carro.longitude_atual, 
                         "tipo veiculo":carro.tipo_veiculo
                        }
        
        return jsonify({
                "data":resposta_json
                }), 200
        # return render_template('carro_especifico.html', carro=carro), 302
    
    else:
        return jsonify({
            'status':'not found'
        }), 404

@view_carro.route('/alterar-carro', methods=['GET', 'PATCH'])
def edit_carro():
    """
    Rota para editar um carro específico com a placa informada

    Método:
        Get, Patch

    Retorno:
        Página mostrando carro editado
    """

    if request.method == 'PATCH':
        data = request.get_json()
        placa = data.get('placa-carro')

        try:
            carro_desejado = Carro.query.filter_by(placa=placa).first()

        except Exception as e:
            return  jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500
        
        if carro_desejado:
            new_placa = data.get('new-placa-carro')
            new_tipo_veiculo = data.get('tipo-veiculo')

            if new_placa != carro_desejado.placa and new_placa != None:
                trajetos = db.session.query(Trajeto).where(Trajeto.carro_placa == carro_desejado.placa)
                motoristas = db.session.query(Motorista).where(Motorista.carro_placa == carro_desejado.placa)
                carro_desejado.placa = new_placa

                for motorista in motoristas:
                    carro_desejado.motorista_cnh.append(motorista)
                
                for trajeto in trajetos:
                    carro_desejado.trajeto.append(trajeto)

                db.session.commit()

            if new_tipo_veiculo != carro_desejado.tipo_veiculo and new_tipo_veiculo != None:
                carro_desejado.tipo_veiculo = new_tipo_veiculo
                db.session.commit()

            return jsonify({
                "status":"updated"
            }), 204

        else:
            return jsonify({
                "status":"not found"
            }), 404
    
    # return render_template('pagina_editar_motorista.html'), 302

@view_carro.route('/excluir-carro', methods=['GET', 'DELETE'])
def delete_carro():
    
    if request.method == 'DELETE':

        data = request.get_json()
        placa_carro = data.get('placa-carro')

        try:
            carro_desejado = Carro.query.filter_by(placa=placa_carro).first()
        
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500

        if carro_desejado:
            try:
                trajeto = Trajeto.query.filter_by(carro_placa = placa_carro).first()
                ponto = PontoViagem.query.filter_by(carro_placa = placa_carro).first()
                
                if trajeto:
                    db.session.query(Trajeto).where(Trajeto.carro_placa == placa_carro).delete()
                    db.session.query(TrajetosCidadaos).where(TrajetosCidadaos.trajeto_id == trajeto.id_trajeto).delete()
                
                if ponto:
                    db.session.query(PontoViagem).where(PontoViagem.carro_placa == placa_carro).delete()
                
                motoristas = db.session.query(Motorista).where(Motorista.carro_placa == placa_carro)

                for motorista in motoristas:
                    motorista.carro_placa = None

                Carro.query.filter_by(placa=placa_carro).delete()
            
            except Exception as e:
                return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500

            db.session.commit()

            return jsonify({
                "status":"deleted"
            }), 204

        else:
            return jsonify({
                "status":"not found"
            }), 404
    
    # return render_template('pagina_deletar_carro.html'), 302

@view_carro.route('/associar-motorista', methods=['GET', 'POST'])
def register_carro():
    """
    Rota para associar um carro a um motorista
    """

    if request.method == 'POST':
        data = request.get_json()
        cnh_motorista = data.get('motorista-cnh')
        placa_motorista = data.get('placa-carro')

        try:
            motorista = Motorista.query.filter_by(cnh=cnh_motorista).first()
            carro_desejado = Carro.query.filter_by(placa=placa_motorista).first()
        
        except Exception as e:
            return jsonify({
            "status":"error",
            "message":f"{str(e)}"
        }), 500

        if not motorista:
            return jsonify({
                "status": "not found"
            }), 404

        if not carro_desejado:
            return jsonify({
                "status": "not found"
            }), 404

        if motorista.carro_placa == placa_motorista:
            return jsonify({
                "status": "warning",
                "message": "Placa já associada ao motorista"
            }), 409

        carro_desejado.motorista_cnh.append(motorista)
        db.session.commit()

        return jsonify({
            "status": "success"
        }), 201
    
    # return render_template('pagina_associar_carro.html'), 302

@view_carro.route('/post-point-now', methods=['POST'])
def post_point_carro():
    """
    Rota para postar latitude e longitude atual de um carro vindos do embarcado
    
    Método: 
        POST

    Retorno: 
        Nenhum
    """

    data = request.get_json()
    latitude_atual = data.get('latitude')
    longitude_atual = data.get('longitude')
    placa = data.get('placa-carro')

    try:
        carro_desejado = Carro.query.filter_by(placa=placa).first()
    
    except Exception as e:
        return jsonify({
            "status":"error",
            "message":f"{str(e)}"
        }), 500
    
    if carro_desejado:
        try:
            if latitude_atual != carro_desejado.latitude_atual and latitude_atual != None:
                carro_desejado.latitude_atual = latitude_atual

            if longitude_atual != carro_desejado.longitude_atual and longitude_atual != None:
                carro_desejado.longitude_atual = longitude_atual

            db.session.commit()

            # DESCOMENTAR CASO SEJA PREFERÍVEL
            # return jsonify({
            #             "status":"created"
            #         }), 204

            return 204
        
        except Exception as e:
            return jsonify({
            "status":"error",
            "message":f"{str(e)}"
        }), 400

    else:
        return jsonify({
            "status":"not found"
        }), 404
    