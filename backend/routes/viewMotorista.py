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

        motorista_existente = Motorista.query.filter_by(cpf=cpf_motorista).first()
        cnh_existente = Motorista.query.filter_by(cnh=cnh_motorista).first()
        if motorista_existente or cnh_existente:
            return jsonify({
                "status": "error",
                "message": "Motorista já cadastrado.",
                "cpf": cpf_motorista,
                # "nome": motorista_existente.nome_completo
            }), 409


        new_motorista = Motorista(
            cnh=cnh_motorista,
            cpf=cpf_motorista,
            nome_completo=nome_motorista,
            # carro_placa=carro_placa,
            senha=senha,
            tipo_usuario=tipo_usuario,
        )

        if carro_placa:
            carro_desejado = Carro.query.filter_by(placa=carro_placa).first()
            carro_desejado.motorista_cnh.append(new_motorista)

        db.session.add(new_motorista)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Motorista cadastrado com sucesso.",
            "cpf": cpf_motorista,
            "nome": nome_motorista
        }), 201
    
    return render_template('pagina_cadastro_motorista.html'), 302

@view_motorista.route('/todos', methods=['GET'])
def get_motorista():
    """
    Rota para mostrar todos os motoristas

    Método:
        Get

    Retorno:
        Página listando todos os motoristas
    """
    motoristas = Motorista.query.all()

    # DEBUG
    resposta_json = {}

    for motorista in motoristas:
        resposta_json[motorista.cpf] = {"nome completo":motorista.nome_completo, "cpf":motorista.cpf, "senha":motorista.senha, "tipo usuario":motorista.tipo_usuario, "placa do carro":motorista.carro_placa, "cnh":motorista.cnh}

    return jsonify({
        "status":"success",
        "message":"motoristas encontrados",
        "json":resposta_json
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
        }), 400
    
    if motorista:
        # DEBUG
        resposta_json = {}
        resposta_json[motorista.cpf] = {"nome completo":motorista.nome_completo, "cpf":motorista.cpf, "senha":motorista.senha, "tipo usuario":motorista.tipo_usuario, "placa do carro":motorista.carro_placa, "cnh":motorista.cnh}

        return jsonify({
            "status":"success",
            "message":"motoristas encontrados",
            "json":resposta_json
        }), 200
        # return render_template('motorista_especifico.html', motorista=motorista), 302
    
    else:
        return jsonify({
            'status':'error',
            'message':f'motorista não encontrado: {str(e)}'
        }), 404
    
# @view_motorista.route('/motorista')

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
        motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()

        if motorista:
            try:
                Motorista.query.filter_by(cpf=cpf_motorista).delete()
                db.session.commit()
                return jsonify({
                    "status":"success",
                    "message":"motorista deletado com sucesso"
                }), 204
            
            except Exception as e:
                return jsonify({
                    "status":"error",
                    "message":f"erro ao deletar motorista: {str(e)}"
                })
        else:
            return jsonify({
                "status":"success",
                "message":"motorista não existe"
            }), 204
        
    return render_template('motoristas.html'), 302

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
        motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()

        if motorista:
            new_nome = data.get('motorista-nome')
            new_placa = data.get('placa-carro')
            # new_cnh = data.get('motorista-cnh')
            # new_tipo_usuario = data.get('tipo-usuario')

            if new_nome != motorista.nome_completo and new_nome != None:
                try:
                    motorista.nome_completo = new_nome
                    db.session.commit()
                    print("status:success, message: update realizado com sucesso")

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":"erro ao realizar update",
                        "error":f"{str(e)}"
                    })
            
            if new_placa != motorista.carro_placa and new_placa != None:
                try:
                    carro_desejado = Carro.query.filter_by(placa=new_placa).first()
                    print(f'carro_desejado.motorista_cnh: {carro_desejado.motorista_cnh}')
                    # print('carro_desejado')

                    if carro_desejado:
                        print(f'carro_desejado.motorista_cnh: {carro_desejado.motorista_cnh}')
                        carro_desejado.motorista_cnh.append(motorista)
                        db.session.commit()
                        print("status:success, message: update realizado com sucesso")

                    else:
                        return jsonify({
                            "status":"not found",
                            "message":"esta placa nao existe"
                        })

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":"erro ao realizar update",
                        "error":f"{str(e)}"
                    })
            
            # db.session.commit()
            return jsonify({
                "status":"success",
                "message":"updates realizados com sucesso"
            })

        else:
            return jsonify({
                "status":"not found",
                "message":"motorista nao existente"
            })

    else:
        return jsonify({'status':"ok"}), 302

