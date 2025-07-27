from config import app, db
from routes.viewIndex import view_index
from routes.viewMotorista import view_motorista
from routes.viewCidadao import view_cidadao
from routes.viewCarro import view_carro
from routes.viewTrajeto import view_trajeto
from routes.viewViagem import view_viagem
from routes.viewAnalise import view_analise

# from models import *
from models.carro import Carro
from models.motorista import Motorista
from models.trajeto  import Trajeto

app.register_blueprint(view_index, url_prefix='/')
app.register_blueprint(view_motorista, url_prefix='/motorista')
app.register_blueprint(view_cidadao, url_prefix='/cidadao')
app.register_blueprint(view_trajeto, url_prefix='/trajeto')
app.register_blueprint(view_carro, url_prefix='/carro')
app.register_blueprint(view_viagem, url_prefix='/viagem')
app.register_blueprint(view_analise, url_prefix='/analise')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)