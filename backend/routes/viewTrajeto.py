from config import db, app
from flask import Blueprint, jsonify, render_template
# from sqlalchemy import select
from datetime import datetime
from models.trajeto import Trajeto
from models.motorista import Motorista

view_trajeto = Blueprint('view_trajeto', __name__)

@view_trajeto.route('/', methods=['GET', 'POST'])
def post_new_route():
    """
    Rota para cadastrar um trajeto mockado no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do trajeto.
        - status error se ocorrer exceção.
    """
    horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)
    
    MOCKTrajeto = Trajeto(
        servicoPrestado='Saúde',
        pontoOrigem='Cerro Corá',
        pontoDestino='Currais Novos',
        horarioEstimado=horarioComeco.time()
        # motoristaResp=1234567890,      # Descomente se o campo existir no modelo
        # idEmbarcado='abc123'           # Descomente se o campo existir no modelo
    )

    try:
        db.session.add(MOCKTrajeto)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Trajeto inserido com sucesso.",
            "trajeto": {
                "servicoPrestado": MOCKTrajeto.servicoPrestado,
                "pontoOrigem": MOCKTrajeto.pontoOrigem,
                "pontoDestino": MOCKTrajeto.pontoDestino,
                "horarioEstimado": str(MOCKTrajeto.horarioEstimado)
                # "motoristaResp": MOCKTrajeto.motoristaResp,   # Inclua se existir
                # "idEmbarcado": MOCKTrajeto.idEmbarcado        # Inclua se existir
            }
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400

@view_trajeto.route('/get-all-trajeto', methods=['GET'])
def get_trajeto():
    """
    Rota para exibir todos os trajetos cadastrados.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos.html' com todos os trajetos cadastrados.
    """
    trajeto_mostrar = Trajeto.query.all()
    
    return render_template('trajetos.html', all_trajetos=trajeto_mostrar)

@view_trajeto.route('/get-especific-trajeto', methods=['GET'])
def get_especific_trajeto():
    """
    Rota para exibir trajetos específicos com informações do motorista.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos_motorista.html' com trajetos filtrados e dados do motorista.
    """
    # trajeto_teste = Trajeto.query(Trajeto.destino, Trajeto.origem, Motorista.nomeCompleto).filter(Trajeto.motoristaResp == Motorista.CNH)
    trajeto_teste = Trajeto.query(Trajeto.destino, Trajeto.origem, Motorista.nomeCompleto).join(Motorista).filter(Trajeto.motoristaResp == Motorista.CNH)

    return render_template('trajetos_motorista.html', especific_trajeto=trajeto_teste)