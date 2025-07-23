from config import db, app
from flask import Blueprint, jsonify, render_template, request
# from sqlalchemy import select
from datetime import datetime
from models.trajeto import Trajeto
from models.pontoTrajeto import PontoTrajeto
from models.trajetos_cidadaos import TrajetosCidadaos
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
    servico_prestado = request.form.get('servico-prestado')
    origem = request.form.get('origem')
    destino = request.form.get('destino')
    placa = request.form.get('placa')
    datahora_estimado = request.form.get('datahora-estimado')
    # print("datahora_estimado (datetime)=", datetime.strptime(datahora_estimado, "%Y-%m-%dT%H:%M:%S")) # Debugging
    datahora_estimado_datetime = datetime.strptime(datahora_estimado, "%Y-%m-%dT%H:%M:%S")

    # servico_prestado = 'Saude'
    # origem = 'Cerro Corá'
    # destino = 'Currais Novos'
    # placa = '4N4L1C3'
    # datahora_estimado = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)

    # horarioComeco = datetime(year=2025, month=7, day=4, hour=13, minute=30, second=0)
    
    MOCKTrajeto = Trajeto(
        servicoPrestado=servico_prestado,
        pontoOrigem=origem,
        pontoDestino=destino,
        carro_placa=placa,
        horarioEstimado=datahora_estimado_datetime.time()
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

@view_trajeto.route('/post-point', methods=['GET', 'POST'])
def post_point_trajeto():
    """
    Rota para postar pontos de um trajeto vindos do embarcado
    
    Método: 
        POST

    Retorno: 
        Nenhum

    OBS: O GET está presente apenas para debug. Necessário retirar
    """

    # data = request #Id do trajeto ao qual o ponto pertence
    # trajeto_desejado = Trajeto.query.filter_by(idTrajeto=id_trajeto).first() # Objeto Trajeto do id correspondente
    # latitude = request # latitude passada pelo embarcado
    # longitude = request # longitude passada pelo embarcado

    id_trajeto = 1 #Id do trajeto ao qual o ponto pertence
    trajeto_desejado = Trajeto.query.filter_by(idTrajeto=id_trajeto).first()
    # print(trajeto_desejado.trajeto_ponto)

    MOCKPontoTrajeto = PontoTrajeto(
        latitude='-14.000026',
        longitude='15.000047',
        trajeto=trajeto_desejado,
        # horarioEstimado=horarioComeco.time()
        # motoristaResp=1234567890,      # Descomente se o campo existir no modelo
        # idEmbarcado='abc123'           # Descomente se o campo existir no modelo
    )

    try:
        db.session.add(MOCKPontoTrajeto)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Ponto de Trajeto inserido com sucesso.",
            "trajeto": {
                "latitude": MOCKPontoTrajeto.latitude,
                "longitude": MOCKPontoTrajeto.longitude,
                "id do trajeto": MOCKPontoTrajeto.trajeto_id,
                # "horarioEstimado": str(MOCKTrajeto.horarioEstimado)
                # "motoristaResp": MOCKTrajeto.motoristaResp,   # Inclua se existir
                # "idEmbarcado": MOCKTrajeto.idEmbarcado        # Inclua se existir
            }
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao inserir trajeto: {str(e)}"
        }), 400