from config import app, db
from flask import Blueprint, request
from models.motorista import Motorista
from models.carro import Carro

view_motorista = Blueprint('view_motorista', __name__)

@app.route('/motorista', methods=['GET', 'POST'])
def cadastrar_motorista():
    # cnh = 1234567890
    cnh = 9876543210
    # cnh = 7418529630
    cpf = '123.456.987-00'
    nome = 'Alice Mock 2'
    senhaTop = 'senhamuitoforte123'
    tipoUsuario = 'motorista'

    if Motorista.query.filter_by(CPF=cpf).first():
        return 'MOTORISTA JÁ CADASTRADO'

    MOCKtorista = Motorista(
        cnh=cnh,
        CPF=cpf,
        nomeCompleto=nome,
        senha=senhaTop,
        tipoUsuario=tipoUsuario
    )

    db.session.add(MOCKtorista)
    db.session.commit()

    return "Página principal do motorista"

@app.route('/motorista-carro', methods=['GET', 'POST'])
def incluir_carro():
    # cnh_motorista = request.form.get('cnh')
    # placa = request.form.get('placa')
    cnh_motorista = 9876543210
    placa_motorista = '4N4L1C3'

    motorista = Motorista.query.filter_by(cnh=cnh_motorista).first()
    placa = Carro.query.filter_by(placa=placa_motorista).first()
    
    if motorista:
        if motorista.veiculoUsado:
            print(f'Veiculo = {motorista.veiculoUsado}')
            print(f'Motorista = {placa.motorista_cnh}')
            return 'PLACA JÁ ASSOCIADA AO MOTORISTA'
        else:
            motorista.veiculoUsado = placa
            
            # placa.motorista_cnh.append(motorista.cnh)

            db.session.commit()
            print(motorista.veiculoUsado)
            print(placa.motorista_cnh)
            return 'OK'
