from config import app, db
from flask import Blueprint, request
from models.motorista import Motorista
from models.carro import Carro

view_motorista = Blueprint('view_motorista', __name__)

@app.route('/motorista', methods=['GET', 'POST'])
def cadastrar_motorista():
    # cnh = 1234567890
    # cpf = '123.456.789-00'
    cnh = 9876543210
    cpf = '321.456.789-00'
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
    
    # cnh_motorista = 1234567890
    cnh_motorista = 9876543210
    placa_motorista = '4N4L1C3'

    motorista = Motorista.query.filter_by(cnh=cnh_motorista).first()
    print(motorista)
    carro_desejado = Carro.query.filter_by(placa=placa_motorista).first()
    print(carro_desejado)
    
    if motorista:
        if motorista.carro_placa == placa_motorista:
            print(f'{carro_desejado.motorista_cnh = }')
            print(f'{motorista.carro = }')
            return 'PLACA JÁ ASSOCIADA AO MOTORISTA'
        
        else:
            # carro_desejado = Carro.query.filter_by(placa=placa_motorista).first()
            print(f'{carro_desejado.motorista_cnh = }')
            print(f'{motorista.cnh = }')

            carro_desejado.motorista_cnh.append(motorista)
            # carro_desejado.motorista_cnh = motorista
            db.session.commit()

            print(f'{carro_desejado.motorista_cnh = }')
            print(f'{motorista.carro = }')
            return 'OK'
    else:
        return 'Motorista não existe'