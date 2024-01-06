from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()       #Estou definindo meu banco de dados sendo .db o objeto
DB_NAME = "database.db"     #Nome do meu banco de dados

#Criando um server flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ' in a hole in the ground there lived a hobbit '
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #Meu sql está localizado no sqlite://{DB_NAME}
    db.init_app(app) #Aqui eu inicializo meu banco de dados



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def login_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database created')