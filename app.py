import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


# Cria uma instância do aplicativo Flask
app = Flask(__name__)
app.static_folder = 'static/'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:jesusdreams213@localhost/baber'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#

#db = SQLAlchemy(app)#

#class Agendamento(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    nome = db.Column(db.String(100))
#    telefone = db.Column(db.String(20))
#    email = db.Column(db.String(100))
#    data = db.Column(db.Date)
#    horario = db.Column(db.Time)
#    servico = db.Column(db.String(50))

#db.create_all()

#@app.route('/agendar', methods=['POST'])
#def agendar():
#    if request.method == 'POST':
#        nome = request.form['nome']
#        telefone = request.form['telefone']
#        email = request.form['email']
#        data = request.form['data']
#        horario = request.form['horario']
#        servico = request.form['servico']
#
#        # Crie um novo objeto de agendamento
#        novo_agendamento = Agendamento(nome=nome, telefone=telefone, email=email, data=data, horario=horario, servico=servico)
#
#        # Adicione o novo agendamento ao banco de dados
#        db.session.add(novo_agendamento)
#        db.session.commit()
#
#        return 'Agendamento confirmado!'


# Define a rota padrão e sua função correspondente
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/services.html")
def Serviços():
    return render_template("services.html")

@app.route("/portifolio.html")
def Portifolio():
    return render_template("portifolio.html")

@app.route("/contact.html")
def Contatos():
    return render_template("contact.html")

@app.route("/agendamento.html")
def Agendamento():
    return render_template("agendamento.html")

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)