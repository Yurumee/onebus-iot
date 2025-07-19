from config import app, db
from flask import Blueprint, request, jsonify
from models.motorista import Motorista
from models.carro import Carro

view_motorista = Blueprint('view_motorista', __name__)

@view_motorista.route('/', methods=['GET', 'POST'])
def cadastrar_motorista():
    """
    Rota para cadastrar um motorista mockado no banco de dados.
    """
    cnh = 9876543210
    cpf = '321.456.789-00'
    nome = 'Alice Mock 2'
    senhaTop = 'senhamuitoforte123'
    tipoUsuario = 'motorista'

    motorista_existente = Motorista.query.filter_by(CPF=cpf).first()
    if motorista_existente:
        return jsonify({
            "status": "error",
            "message": "Motorista já cadastrado.",
            "cpf": cpf,
            "nome": motorista_existente.nomeCompleto
        }), 409

    MOCKtorista = Motorista(
        cnh=cnh,
        CPF=cpf,
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

@view_motorista.route('/motorista-carro', methods=['GET', 'POST'])
def incluir_carro():
    """
    Rota para associar um carro mockado a um motorista mockado.
    """
    cnh_motorista = 9876543210
    placa_motorista = '4N4L1C3'

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