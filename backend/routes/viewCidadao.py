from config import app, db
from flask import Blueprint, request, jsonify
from models.cidadao import Cidadao

view_cidadao = Blueprint('view_cidadao', __name__)

@view_cidadao.route('/')
def post_new_cidadao():
    """
    Rota para cadastrar um cidadão mockado no banco de dados.

    Método:
        GET

    Retorno:
        - status, message e dados do cidadão.
        - status error se o cidadão já existe.
    """
    cpf = '789.456.123-00'
    nome = 'Alice Mock'
    senhaTop = 'senhaforte123'

    cidadao_existente = Cidadao.query.filter_by(cpf=cpf).first()
    if cidadao_existente:
        return jsonify({
            "status": "error",
            "message": "Cidadão já cadastrado.",
            "cpf": cpf,
            "nome": cidadao_existente.nomeCompleto
        }), 409

    MOCKCidadao = Cidadao(
        cpf=cpf,
        nomeCompleto=nome,
        senha=senhaTop,
        tipoUsuario='cidadao'
    )

    db.session.add(MOCKCidadao)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Cidadão cadastrado com sucesso.",
        "cpf": cpf,
        "nome": nome
    }), 201

@app.route('/signin', methods=['GET', 'POST'])
def singin():
    """
    Rota para autenticação de cidadão.

    Métodos:
        GET, POST

    Parâmetros esperados (via formulário):
        - cpf: cpf do cidadão
        - senha: Senha do cidadão

    Retorno:
        - status, message e dados do cidadão.
        - status error se usuário não existir ou senha estiver incorreta.
    """
    cpf = request.form.get('cpf')
    password = request.form.get('senha')

    user = Cidadao.query.filter_by(cpf=cpf).first()

    if user:
        if user.senha == password:
            return jsonify({
                "status": "success",
                "message": "Autenticação realizada com sucesso.",
                "cpf": cpf,
                "nome": user.nomeCompleto
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Senha incorreta.",
                "cpf": cpf
            }), 401

    return jsonify({
        "status": "error",
        "message": "Usuário não encontrado.",
        "cpf": cpf
    }), 404