from config import db, app
from flask import Blueprint, jsonify, render_template, request
# from sqlalchemy import select
# from datetime import datetime
from models.trajeto import Trajeto
from models.pontoTrajeto import PontoTrajeto

view_viagem = Blueprint('view_viagem', __name__)

@view_viagem.route('/', methods=['GET', 'POST'])
def post_new_ponto_trajeto():
    """
    Rota para cadastrar um ponto de trajeto no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do ponto.
        - status error se ocorrer exceção.
    """

    if request.method == 'POST':
        data = request.get_json()
        id_trajeto = data.get('id-trajeto')

        try:
            trajeto_desejado = Trajeto.query.filter_by(id_trajeto=id_trajeto).first()
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 400
        
        if trajeto_desejado:
            
            latitude_ponto = data.get('latitude')
            longitude_ponto = data.get('longitude')
            tipo_ponto = data.get('tipo-ponto')

            try:
                new_ponto_trajeto = PontoTrajeto(
                latitude=latitude_ponto,
                longitude=longitude_ponto,
                tipo_ponto=tipo_ponto
                )

                trajeto_desejado.trajeto_ponto.append(new_ponto_trajeto)

                db.session.add(new_ponto_trajeto)
                db.session.commit()
        
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": f"Erro ao inserir novo ponto de trajeto: {str(e)}"
                }), 400
            
            return jsonify({
                    "status": "success",
                    "message": "Trajeto inserido com sucesso.",
                    "trajeto": {
                        "latitude_ponto": new_ponto_trajeto.latitude,
                        "longitude_ponto": new_ponto_trajeto.longitude,
                        "tipo": new_ponto_trajeto.tipo_ponto
                    }
                }), 201

        else:
            return jsonify({
                "status":"not found",
                "message":"o trajeto desejado nao existe"
            }), 404
        
    return render_template('pagina_cadastrar_ponto_trajeto.html'), 302

@view_viagem.route('/alterar-ponto', methods=['GET', 'PATCH'])
def edit_ponto_trajeto():
    """
    Rota para editar um ponto de trajeto específico com o id informado

    Método:
        Get, Patch

    Retorno:
        Página mostrando ponto editado
    """
    if request.method == 'PATCH':
        data = request.get_json()
        id_ponto = data.get('id-ponto-trajeto')
        ponto_desejado = PontoTrajeto.query.filter_by(id_ponto_traj=id_ponto).first()

        if ponto_desejado:
            latitude_ponto = data.get('latitude')
            longitude_ponto = data.get('longitude')
            new_trajeto = data.get('trajeto-id')
            tipo_ponto = data.get('tipo-ponto')

            if latitude_ponto != ponto_desejado.latitude and latitude_ponto != None:
                ponto_desejado.latitude = latitude_ponto
                db.session.commit()

            if longitude_ponto != ponto_desejado.longitude and longitude_ponto != None:
                ponto_desejado.longitude = longitude_ponto
                db.session.commit()

            if tipo_ponto != ponto_desejado.tipo_ponto and tipo_ponto != None:
                ponto_desejado.tipo_ponto = tipo_ponto
                db.session.commit()

            if new_trajeto != ponto_desejado.trajeto_id and new_trajeto != None:
                trajeto_desejado = Trajeto.query.filter_by(id_trajeto=new_trajeto).first()

                if trajeto_desejado:
                    trajeto_desejado.trajeto_ponto.append(ponto_desejado)
                    db.session.commit()

                else:
                    return jsonify({
                        "status":"not found",
                        "message":"trajeto nao encontrado"
                    }), 404
            
            return jsonify({
                "status":"success",
                "message":"updates realizados com sucesso"
            }), 200
        
        else:
            return jsonify({
                "status":"not found",
                "message":"ponto nao encontrado"
            }), 404


    return render_template('editar_ponto_trajeto.html'), 302

@view_viagem.route('/rota-especifica', methods=['GET', 'POST'])
def get_pontos_trajeto():
    """
    Rota para listar todos os ponto de trajeto de um trajeto específico com o id informado

    Método:
        Get, Post

    Retorno:
        Página mostrando pontos do trajeto desejado
    """

    data = request.get_json()
    trajeto_id = data.get('trajeto-id')
    trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()

    if trajeto_desejado:
        # pontos_trajeto = db.session.query(PontoTrajeto, Trajeto).join(Trajeto, Trajeto.id_trajeto == trajeto_id).all()
        pontos_trajeto = db.session.query(PontoTrajeto).where(PontoTrajeto.trajeto_id == trajeto_id).all()

        print(pontos_trajeto)

        resposta_json = {}
        for ponto in pontos_trajeto:
            resposta_json[ponto.id_ponto_traj] = {"id_trajeto": ponto.trajeto_id,
                                                  "latitude": ponto.latitude,
                                                  "longitude": ponto.longitude,
                                                  "tipo ponto": ponto.tipo_ponto,  
                                                  }

        return jsonify({
            "status": "success",
            "message": "pontos de trajeto encontrados.",
            "trajetos": resposta_json,
        }), 200

    else:
        return jsonify({
            "status":"not found",
            "message":"trajeto nao encontrado"
        }), 404


    # return render_template('pagina_pontos_trajeto.html'), 302

@view_viagem.route('/todos', methods=['GET'])
def get_all_pontos_trajeto():
    """
    Rota para listar todos os ponto de trajeto, independente do trajeto que pertencem

    Método:
        Get

    Retorno:
        Página mostrando todos os pontos
    """

    # data = request.get_json()
    # trajeto_id = data.get('trajeto-id')
    pontos_trajeto = PontoTrajeto.query.all()

    if pontos_trajeto:
        # pontos_trajeto = db.session.query(PontoTrajeto, Trajeto).join(Trajeto, Trajeto.id_trajeto == trajeto_id).all()
        # pontos_trajeto = db.session.query(PontoTrajeto).where(PontoTrajeto.trajeto_id == trajeto_id).all()

        print(pontos_trajeto)

        resposta_json = {}
        for ponto in pontos_trajeto:
            resposta_json[ponto.id_ponto_traj] = {"trajeto_id": ponto.trajeto_id,
                                                  "latitude": ponto.latitude,
                                                  "longitude": ponto.longitude,
                                                  "tipo ponto": ponto.tipo_ponto,  
                                                  }

        return jsonify({
            "status": "success",
            "message": "pontos de trajeto encontrados.",
            "trajetos": resposta_json,
        }), 200

    else:
        return jsonify({
            "status":"not found",
            "message":"trajeto nao encontrado"
        }), 404


    # return render_template('pagina_pontos_trajeto.html'), 302

@view_viagem.route('/excluir-ponto', methods=['GET', 'DELETE', 'POST'])
def delete_pontos_trajeto():
    """
    Rota para deletar um ponto de trajeto especifico

    Método:
        Get, Delete, Post

    Retorno:
        Página para deletar ponto
    """

    data = request.get_json()
    id_ponto = data.get('id-ponto')
    ponto_trajeto = PontoTrajeto.query.filter_by(id_ponto_traj=id_ponto).first()

    if ponto_trajeto:
        db.session.query(PontoTrajeto).filter(PontoTrajeto.id_ponto_traj==id_ponto).delete()
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "ponto de trajeto deletado.",
            # "trajetos": resposta_json,
        }), 200

    else:
        return jsonify({
            "status":"not found",
            "message":"ponto nao encontrado"
        }), 404


    # return render_template('pagina_pontos_trajeto.html'), 302

@view_viagem.route('/excluir-todos', methods=['GET', 'DELETE', 'POST'])
def delete_all_pontos_trajeto():
    """
    Rota para deletar todos os pontos de trajeto de um trajeto especifico

    Método:
        Get, Delete, Post

    Retorno:
        Página para deletar pontos
    """

    data = request.get_json()
    id_trajeto = data.get('id-trajeto')
    pontos_trajeto = PontoTrajeto.query.filter_by(trajeto_id=id_trajeto).all()
    print(pontos_trajeto)

    if pontos_trajeto:
        db.session.query(PontoTrajeto).where(PontoTrajeto.trajeto_id == id_trajeto).delete()
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "pontos de trajeto deletado.",
            # "trajetos": resposta_json,
        }), 200

    else:
        return jsonify({
            "status":"not found",
            "message":"pontos nao encontrados"
        }), 404


    # return render_template('pagina_pontos_trajeto.html'), 302