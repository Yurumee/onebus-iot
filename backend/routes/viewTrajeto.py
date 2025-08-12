from config import db
from flask import Blueprint, jsonify, render_template, request
from datetime import datetime
from models.trajeto import Trajeto
from models.pontoViagem import PontoViagem
from models.trajetos_cidadaos import TrajetosCidadaos
from models.motorista import Motorista
from models.carro import Carro
from models.cidadao import Cidadao

view_trajeto = Blueprint('view_trajeto', __name__)

@view_trajeto.route('/', methods=['GET', 'POST'])
def post_new_trajeto():
    """
    Rota para cadastrar um trajeto mockado no banco de dados.

    Métodos:
        GET, POST

    Retorno:
        - status, message e dados do trajeto.
        - status error se ocorrer exceção.
    """
    if request.method == 'POST':
        data = request.get_json()

        servico_prestado = data.get('servico-prestado')
        origem = data.get('origem')
        destino = data.get('destino')
        placa = data.get('placa-carro')
        datahora_estimado = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S")
        
        try:
            new_trajeto = Trajeto(
                servico_prestado=servico_prestado,
                ponto_origem=origem,
                ponto_destino=destino,
                horario_estimado=datahora_estimado.time()
            )

            carro_desejado = Carro.query.filter_by(placa=placa).first()
            carro_desejado.trajeto.append(new_trajeto)
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"{str(e)}"
            }), 500

        try:
            db.session.add(new_trajeto)
            db.session.commit()

            return jsonify({
                "status": "created"
            }), 201
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"{str(e)}"
            }), 500
    
    # return render_template('pagina_cadastrar_projeto.html'), 302

@view_trajeto.route('/alterar-trajeto', methods=['GET', 'PATCH'])
def edit_trajeto():
    """
    Rota para editar um trajeto específico com o id informado

    Método:
        Get, Patch

    Retorno:
        Página mostrando trajeto editado
    """

    if request.method == 'PATCH':
        data = request.get_json()
        trajeto_id = data.get('trajeto-id')
        
        try:
            trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()
        
        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            }), 500

        if trajeto_desejado:
            new_servico = data.get('servico-prestado')
            new_ponto_origem = data.get('ponto-origem')
            new_ponto_destino = data.get('ponto-destino')
            new_horario = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S").time()
            new_placa = data.get('placa-carro')

            if new_servico != trajeto_desejado.servico_prestado and new_servico != None:
                try:
                    trajeto_desejado.servico_prestado = new_servico
                    db.session.commit()
                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
            
            if new_ponto_origem != trajeto_desejado.ponto_origem and new_ponto_origem != None:
                
                try:
                    trajeto_desejado.ponto_origem = new_ponto_origem
                    db.session.commit()
                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
            
            if new_ponto_destino != trajeto_desejado.ponto_destino and new_ponto_destino != None:
                
                try:
                    trajeto_desejado.ponto_destino = new_ponto_destino
                    db.session.commit()
                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500

            if new_horario != trajeto_desejado.horario_estimado and new_horario != None:
                
                try:
                    trajeto_desejado.horario_estimado = new_horario
                    db.session.commit()
                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500
                
            if new_placa != trajeto_desejado.carro_placa and new_placa != None:
                try:
                    carro_desejado = Carro.query.filter_by(placa=new_placa).first()

                except Exception as e:
                    return jsonify({
                        "status":"error",
                        "message":f"{str(e)}"
                    }), 500

                if carro_desejado:
                    try:
                        carro_desejado.trajeto.append(trajeto_desejado)
                        db.session.commit()
                    except Exception as e:
                        return jsonify({
                            "status":"error",
                            "message":f"{str(e)}"
                        }), 500

                else:
                    return jsonify({
                        "status":"not found",
                    }), 404

            return jsonify({
                "status":"updated",
            }), 204

        else:
            return jsonify({
                "status":"not found"
            }), 404
    
    # return render_template('pagina_editar_trajeto.html'), 302

@view_trajeto.route('/excluir-trajeto', methods=['GET','DELETE'])
def delete_trajeto():
    if request.method == 'DELETE':
        
        data = request.get_json()
        trajeto_id = data.get('trajeto-id')

        try:
            trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()

        except Exception as e:
            return jsonify({
                "status":"error",
                "message":f"{str(e)}"
            })
        
        if trajeto_desejado:
            try:
                db.session.query(TrajetosCidadaos).where(TrajetosCidadaos.trajeto_id == trajeto_desejado.id_trajeto).delete()
                Trajeto.query.filter_by(id_trajeto=trajeto_id).delete()

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

@view_trajeto.route('/todos', methods=['GET'])
def get_trajeto():
    """
    Rota para exibir todos os trajetos cadastrados.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos.html' com todos os trajetos cadastrados.
    """
    try:
        trajetos = Trajeto.query.all()

    except Exception as e:
        return jsonify({
            "status":"error",
            "message":f"{str(e)}"
        }), 500
    
    resposta_json = {}

    for trajeto in trajetos:
        resposta_json[trajeto.id_trajeto] = {
            "id":trajeto.id_trajeto, 
            "serviço prestado":trajeto.servico_prestado, 
            "ponto de origem":trajeto.ponto_origem, 
            "ponto de destino":trajeto.ponto_destino, 
            "horario estimado":str(trajeto.horario_estimado), 
            "placa carro":trajeto.carro_placa
            }

    return jsonify({
        "status":"success",
        "data":resposta_json
    }), 200
    
    # return render_template('trajetos.html', all_trajetos=trajeto_mostrar), 302

@view_trajeto.route('/rota-motorista', methods=['GET', 'POST'])
def get_especific_trajeto():
    """
    Rota para exibir trajetos específicos com informações de um motorista específico.

    Método:
        GET

    Retorno:
        Renderiza o template 'trajetos_motorista.html' com trajetos filtrados e dados do motorista.
    """
    data = request.get_json()
    cnh_desejado = data.get('motorista-cnh')

    try:
        motorista_desejado = Motorista.query.filter_by(cnh=cnh_desejado).first()
    except Exception as e:
        return jsonify({
            "status":"error",
            "message":f"{str(e)}"
        }), 500

    if motorista_desejado:
        try:
            trajeto = db.session.query(Trajeto, Motorista).join(Motorista, Trajeto.carro_placa == Motorista.carro_placa).where(Motorista.carro_placa == motorista_desejado.carro_placa)
            
        except Exception as e:
            return jsonify({
            "status": "error",
            "message": f"{str(e)}"
        }), 500

        resposta_json = {}
        for trajeto in trajeto:
            resposta_json[trajeto[0].id_trajeto] = {"trajeto_id": trajeto[0].id_trajeto, "carro_placa": trajeto[0].carro_placa, "ponto_origem": trajeto[0].ponto_origem, "ponto_destino": trajeto[0].ponto_destino, "horario_estimado": str(trajeto[0].horario_estimado), "motorista responsavel": trajeto[1].nome_completo, "cnh": trajeto[1].cnh}

        return jsonify({
            "status": "success",
            "data": resposta_json,
        }), 200

        # return render_template('trajetos_motorista.html', especific_trajeto=trajeto), 302
    
    else:
        return jsonify({
                    "status":"not found"
                }), 404


@view_trajeto.route('/vincular-cidadao', methods=['GET', 'POST'])
def register_cidadao():
    """
    Rota para vincular um cidadao específico a um trajeto especifico.

    Método:
        GET, POST

    Retorno:
        Renderiza o template 'trajeto-cidadao.html' com o trajeto do cidadao desejado.
    """

    if request.method == 'POST':
        data = request.get_json()
        cpf_desejado = data.get('cidadao-cpf')
        trajeto_id = data.get('id-trajeto')

        try:
            trajeto_desejado = Trajeto.query.filter_by(id_trajeto=trajeto_id).first()
            cidadao_desejado = Cidadao.query.filter_by(cpf=cpf_desejado).first()

        except Exception as e:
            return jsonify({
            "status": "error",
            "message": f"{str(e)}"
        }), 500

        if cidadao_desejado == None or trajeto_desejado == None:
            return jsonify({
                'status':'not found'
            }), 404
        
        else:

            if TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_desejado, TrajetosCidadaos.trajeto_id==trajeto_id).first():
                return jsonify({
                    'status':'conflict',
                }), 409
            
            else:
                try:
                    trajeto_vinculado = TrajetosCidadaos(
                        cidadao=cidadao_desejado,
                        trajeto=trajeto_desejado
                    )

                    db.session.add(trajeto_vinculado)
                    db.session.commit()
                    
                    # return render_template('pagina_vincular_cidadao.html'), 302
                    return jsonify({
                        'status':'success',
                    }), 201
                
                except Exception as e:
                    return jsonify({
                        'status':'error',
                        'message':f'{str(e)}'
                    }), 500
                
    # return render_template('pagina_vincular_cidadao.html'), 302

@view_trajeto.route('/desvincular-cidadao', methods=['GET', 'POST'])
def delete_vinculo_cidadao():
    
    if request.method == 'POST':
        data = request.get_json()
        cpf_cidadao = data.get('cidadao-cpf')
        trajeto_id = data.get('id-trajeto')

        try:
            vinculo_desejado = TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_cidadao, TrajetosCidadaos.trajeto_id==trajeto_id).first()

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"{str(e)}"
            }), 500

        if vinculo_desejado:
            try:
                TrajetosCidadaos.query.filter(TrajetosCidadaos.cidadao_cpf==cpf_cidadao, TrajetosCidadaos.trajeto_id==trajeto_id).delete()
                db.session.commit()
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": f"{str(e)}"
                    }), 500

            return jsonify({
                'status':'deleted',
            }), 204
        
        else:
            return jsonify({
                'status':'not found'
            }), 404

    # return render_template('pagina_deletar_vinculo.html'), 302

@view_trajeto.route('/post-point', methods=['POST'])
def post_ponto_viagem():
    """
    Rota para postar pontos de uma viagem realizada vindos do embarcado
    
    Método: 
        POST

    Retorno: 
        Nenhum

    OBS: O GET está presente apenas para debug. Necessário retirar
    """

    data = request.get_json()
    latitude_ponto = data.get('latitude')
    longitude_ponto = data.get('longitude')
    placa_carro = data.get('placa-carro')
    datahora = datetime.strptime(data.get('datahora-estimado'), "%Y-%m-%dT%H:%M:%S") # possivel refactor

    try:
        new_ponto_viagem = PontoViagem(
            latitude_ponto=latitude_ponto,
            longitude_ponto=longitude_ponto,
            data=datahora.date(),
            hora=datahora.time()
        )
    
        carro_desejado = Carro.query.filter_by(placa=placa_carro).first()
        carro_desejado.viagem_pontos.append(new_ponto_viagem)
        db.session.add(new_ponto_viagem)
        db.session.commit()
        
        # DESCOMENTAR CASO SEJA PREFERÍVEL
        # return jsonify({
        #             "status":"created"
        #         }), 204
        return 204
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"{str(e)}"
        }), 500