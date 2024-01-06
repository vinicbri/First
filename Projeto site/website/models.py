from . import db        #estou importando do pacote o db que é o banco de dado
from flask_login import UserMixin           #Aqui eu tenho que usar o modulo do flask_login que ajuda a logar o usuario
from sqlalchemy.sql import func
from sqlalchemy import Integer, String

class Note(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #Basicamente aqui eu estou referenciando o user_id com um id já criado, para sempre que uma nota for alterada o programa vai saber o id de quem alterou ela 

class User(db.Model, UserMixin):    #Aqui eu estou definindo meu modelo de banco de dados para o usuario
    id = db.Column(db.Integer, primary_key=True)     #basicamente eu estou transmitindo que o id do meu usuario é unico usano o db.integer
    email = db.Column(db.String(150), unique=True)   
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')     #Toda vez que criamos a nota, vai adicionar o id da nota no notes 