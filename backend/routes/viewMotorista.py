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
    # cnh = request.form.get('cnh') # Pega os dados enviados pelo body
    # cpf = request.form.get('cpf') # Pega os dados enviados pelo body
    # nome = request.form.get('nome-motorista') # Pega os dados enviados pelo body
    # senhaTop = request.form.get('senha') # Pega os dados enviados pelo body
    # tipoUsuario = request.form.get('tipo-usuario') # Pega os dados enviados pelo body

    cnh = 9876543210
    cpf = '321.456.789-00'
    nome = 'Alice Mock 2'
    senhaTop = 'senhamuitoforte123'
    tipoUsuario = 'motorista'

    motorista_existente = Motorista.query.filter_by(cpf=cpf).first()
    if motorista_existente:
        return jsonify({
            "status": "error",
            "message": "Motorista já cadastrado.",
            "cpf": cpf,
            "nome": motorista_existente.nomeCompleto
        }), 409

    MOCKtorista = Motorista(
        cnh=cnh,
        cpf=cpf,
        nomeCompleto=nome,
        senha=senhaTop,
        tipoUsuario=tipoUsuario
    )

    db.session.add(MOCKtorista)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Motorista cadastrado com sucesso.",
        "cpf": cpf,
        "nome": nome
    }), 201

@view_motorista.route('/excluir-motorista', methods=['GET', 'POST'])
def delete_motorista():
    """
    Rota para deletar um motorista específico com o cpf informado

    Método:
        Get, Post

    Retorno:
        Página indicando motorista deletado
    """
    if request.method == 'POST':
        cpf_motorista = request.form.get('motorista-cpf')
        motorista = Motorista.query.filter_by(cpf=cpf_motorista).first()

        if motorista:
            try:
                Motorista.query.filter_by(cpf=cpf_motorista).delete()
                db.session.commit()
                return jsonify({
                    "status":"success",
                    "message":"motorista deletado com sucesso"
                }), 200
            
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

@view_motorista.route('/motorista-carro', methods=['GET', 'POST'])
def register_carro():
    """
    Rota para associar um carro mockado a um motorista mockado.
    """
    cnh_motorista = 9876543210
    placa_motorista = 'S54NT05'

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