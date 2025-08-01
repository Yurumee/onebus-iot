from config import app, db
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
        carro_placa = data.get('carro-placa')

        # cnh = 9876543219
        # cpf = '123.456.789-00'
        # nome = 'Alice Mock 2'
        # senha = 'senhamuitoforte123'
        # tipo_usuario = 'motorista'
        # carroPlaca = '4N4L1C3'
        # carroPlaca = None

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
            carro_placa=carro_placa,
            senha=senha,
            tipo_usuario=tipo_usuario,
        )

        db.session.add(new_motorista)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Motorista cadastrado com sucesso.",
            "cpf": cpf_motorista,
            "nome": nome_motorista
        }), 201
    
    return render_template('pagina_cadastro_motorista.html'), 302

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

            if new_nome != motorista.nome_completo:
                try:
                    motorista.nome_completo = new_nome
                    db.session.commit()

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":"erro ao realizar update",
                        "error":f"{str(e)}"
                    })
            
            if new_placa != motorista.carro_placa or new_placa != None:
                try:
                    carro_desejado = Carro.query.filter_by(placa=new_placa).first()

                    if carro_desejado:
                        carro_desejado.motorista_cnh.append(motorista)
                        db.session.commit()

                    else:
                        return jsonify({
                            "status":"not found",
                            "message":"esta placa não existe"
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
                "message":"update realizado com sucesso"
            })

        else:
            return jsonify({
                "status":"not found",
                "message":"motorista nao existente"
            })

    else:
        return render_template('motoristas.html'), 302

@view_motorista.route('/motorista-carro', methods=['GET', 'POST'])
def register_carro():
    """
    Rota para associar um carro a um motorista mockado.
    """
    # cnh_motorista = 9876543210
    # placa_motorista = 'S54NT05'

    if request.method == 'POST':
        data = request.get_json()
        cnh_motorista = data.get('motorista-cnh')
        placa_motorista = data.get('placa')

        motorista = Motorista.query.filter_by(cnh=cnh_motorista).first()
        carro_desejado = Carro.query.filter_by(placa=placa_motorista).first()

        if not motorista:
            return jsonify({
                "status": "error",
                "message": "Motorista não encontrado.",
                "cnh": cnh_motorista
            }), 404

        if not carro_desejado:
            return jsonify({
                "status": "error",
                "message": "Carro não encontrado.",
                "placa": placa_motorista
            }), 404

        if motorista.carro_placa == placa_motorista:
            return jsonify({
                "status": "warning",
                "message": "Placa já associada ao motorista.",
                "cnh": cnh_motorista,
                "placa": placa_motorista
            }), 200

        carro_desejado.motorista_cnh.append(motorista)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Carro associado ao motorista com sucesso.",
            "cnh": cnh_motorista,
            "placa": placa_motorista
        }), 200
    
    return render_template('pagina_associar_carro.html'), 302