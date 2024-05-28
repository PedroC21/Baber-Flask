import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância do aplicativo Flask
app = Flask(__name__)
app.static_folder = 'static/'
app.secret_key = 'supersecretkey'

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agendamentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de dados para os agendamentos
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(8), nullable=False)
    servico = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Agendamento {self.id}>'

# Define a rota padrão e sua função correspondente
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/services.html")
def services():
    return render_template("services.html")

@app.route("/portfolio.html")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/agendamento.html")
def agendamento():
    return render_template("agendamento.html")

@app.route('/agendamentos')
def visualizar_agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template('visualizar_agendamentos.html', agendamentos=agendamentos)


# Rota para lidar com o envio do formulário
@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    data = request.form['data']
    horario = request.form['horario']
    servico = request.form['servico']
    
    # Crie um novo objeto de agendamento
    novo_agendamento = Agendamento(nome=nome, telefone=telefone, email=email, data=data, horario=horario, servico=servico)
    
    # Adicione o novo agendamento ao banco de dados
    try:
        db.session.add(novo_agendamento)
        db.session.commit()
        flash(f"Agendamento de {nome} adicionado com sucesso!", 'success')
    except Exception as e:
        flash(f"Erro ao adicionar agendamento: {e}", 'danger')
    
    return redirect(url_for('agendamento'))

# Executa o aplicativo Flask
if __name__ == '__main__':
    # Criação das tabelas no banco de dados
    with app.app_context():
        try:
            db.create_all()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
    app.run(debug=True)
