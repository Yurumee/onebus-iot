from config import db
from flask import Blueprint, request, jsonify, render_template
from models.motorista import Motorista
from models.carro import Carro

view_motorista = Blueprint('view_motorista', __name__)

@view_motorista.route('/', methods=['GET', 'POST'])
def post_new_motorista():
    """
    Rota para cadastrar um motorista mockado no banco de dados.
    """

    if request.method == 'POST':
        data = request.get_json() # pega todos os dados passados pelo body

        cnh_motorista = data.get('motorista-cnh') 
        cpf_motorista = data.get('motorista-cpf') 
        nome_motorista = data.get('motorista-nome') 
        senha = data.get('senha') 
        tipo_usuario = data.get('tipo-usuario') 
        carro_placa = data.get('placa-carro')

        try:
            motorista_existente = Motorista.query.filter_by(cpf=cpf_motorista).first()
            cnh_existente = Motorista.query.filter_by(cnh=cnh_motorista).first()

        except Exception as e:
            return jsonify({
                'status':'error',
                'message':f'{str(e)}'
            }), 500
        
        if motorista_existente or cnh_existente:
            return jsonify({
                "status": "conflict"
            }), 409

        try:
            new_motorista = Motorista(
                cnh=cnh_motorista,
                cpf=cpf_motorista,
                nome_completo=nome_motorista,
                senha=senha,
                tipo_usuario=tipo_usuario,
            )

            if carro_placa:
                try:
                    carro_desejado = Carro.query.filter_by(placa=carro_placa).first()
                
                except Exception as e:
                    return jsonify({
                        'status':'error',
                        'message':f'{str(e)}'
                    }), 500
                
                carro_desejado.motorista_cnh.append(new_motorista)

            db.session.add(new_motorista)
            db.session.commit()
        
        except Exception as e:
            return jsonify({
                'status':'error',
                'message':f'{str(e)}'
            }), 500
        
        return jsonify({
            "status": "created"
        }), 201
    
    # return render_template('pagina_cadastro_motorista.html'), 302

@view_motorista.route('/todos', methods=['GET'])
def get_motorista():
    """
    Rota para mostrar todos os motoristas

    Método:
        Get

    Retorno:
        Página listando todos os motoristas
    """
    try:
        motoristas = Motorista.query.all()

    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    resposta_json = {}

    for motorista in motoristas:
        resposta_json[motorista.cpf] = {"nome completo":motorista.nome_completo, "cpf":motorista.cpf, "senha":motorista.senha, "tipo usuario":motorista.tipo_usuario, "placa do carro":motorista.carro_placa, "cnh":motorista.cnh}

    return jsonify({
        "status":"success",
        "data":resposta_json
        }), 200
    # return render_template('todos_motoristas.html', all_motoristas=motoristas), 302

@view_motorista.route('/motorista-especifico', methods=['GET', 'POST'])
def get_especific_motorista():
    """
    Rota para mostrar um motorista especifico pela cnh informada

    Método:
        Get

    Retorno:
        Página listando motorista especifico
    """

    data = request.get_json()
    cnh_desejado = data.get('motorista-cnh')

    try:
        motorista = Motorista.query.filter_by(cnh=cnh_desejado).first()

    except Exception as e:
        return jsonify({
            'status':'error',
            'message':f'{str(e)}'
        }), 500
    
    if motorista:
        resposta_json = {"nome completo":motorista.nome_completo, "cpf":motorista.cpf, "senha":motorista.senha, "tipo usuario":motorista.tipo_usuario, "placa do carro":motorista.carro_placa, "cnh":motorista.cnh}

        return jsonify({
            "status":"success",
            "data":resposta_json
        }), 200
        # return render_template('motorista_especifico.html', motorista=motorista), 302
    
    else:
        return jsonify({
            'status':'not found'
        }), 404

@view_motorista.route('/excluir-motorista', methods=['GET', 'DELETE'])
def delete_motorista():
    """
    Rota para deletar um motorista específico com o cpf informado

    Método:
        Get, Post

    Retorno:
        Página indicando motorista deletado
    """
    if request.method == 'DELETE':
        cpf_motorista = request.form.get('motorista-cpf')
        
        try:
            motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()
        
        except Exception as e:
            return jsonify({
                'status':'error',
                'message':f'{str(e)}'
            }), 500
        
        if motorista:
            try:
                Motorista.query.filter_by(cpf=cpf_motorista).delete()
                db.session.commit()
            
            except Exception as e:
                return jsonify({
                    "status":"error",
                    "message":f"{str(e)}"
                }), 500
            
            return jsonify({
                "status":"deleted"
            }), 204
        
        else:
            return jsonify({
                "status":"not found"
            }), 404
        
    # return render_template('motoristas.html'), 302

@view_motorista.route('/alterar-motorista', methods=['GET', 'PATCH'])
def edit_motorista():
    """
    Rota para editar um motorista específico com o cpf informado

    Método:
        Get, Patch

    Retorno:
        Página mostrando motorista editado
    """

    if request.method == 'PATCH':
        data = request.get_json()
        cpf_motorista = data.get('motorista-cpf')
        
        try:
            motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()

        except Exception as e:
            return jsonify({
                'status':'error',
                'message':f'{str(e)}'
            }), 500
        
        if motorista:
            new_nome = data.get('motorista-nome')
            new_placa = data.get('placa-carro')
            # new_cnh = data.get('motorista-cnh')
            # new_tipo_usuario = data.get('tipo-usuario')

            if new_nome != motorista.nome_completo and new_nome != None:
                try:
                    motorista.nome_completo = new_nome
                    db.session.commit()

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
            
            if new_placa != motorista.carro_placa and new_placa != None:
                try:
                    carro_desejado = Carro.query.filter_by(placa=new_placa).first()

                    if carro_desejado:
                        carro_desejado.motorista_cnh.append(motorista)
                        db.session.commit()

                    else:
                        return jsonify({
                            "status":"not found",
                        }), 404

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
            
            # db.session.commit()
            return jsonify({
                "status":"updated",
            }), 204

        else:
            return jsonify({
                "status":"not found",
            }), 404
