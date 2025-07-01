from config import app, db
from routes.viewMotorista import view_motorista
from routes.viewCidadao import view_cidadao

app.register_blueprint(view_motorista, url_prefix='/')
app.register_blueprint(view_cidadao, url_prefix='/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)