import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Cria uma instância do aplicativo Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.static_folder = 'static/'

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agendamentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de dados para os agendamentos
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data = db.Column(db.String(10))
    horario = db.Column(db.String(8))
    servico = db.Column(db.String(50))

    def __repr__(self):
        return f'<Agendamento {self.id}>'

# Modelo de dados para o administrador
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Crie as tabelas no banco de dados
with app.app_context():
    db.create_all()

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
def agendamento():
    agendamentos = Agendamento.query.all()
    horarios_agendados = [(agendamento.data, agendamento.horario) for agendamento in agendamentos]
    return render_template("agendamento.html", horarios_agendados=horarios_agendados)

# Rota para lidar com o envio do formulário
@app.route('/agendar', methods=['POST'])
def agendar():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        data = request.form['data']
        horario = request.form['horario']
        servico = request.form['servico']

       # Verifique se já existe um agendamento com a mesma data e horário
        agendamento_existente = Agendamento.query.filter_by(data=data, horario=horario).first()
        if agendamento_existente:
            flash('Já existe um agendamento para essa data e horário. Por favor, escolha outro horário.')
            return redirect(url_for('agendamento'))
        
        # Crie um novo objeto de agendamento
        novo_agendamento = Agendamento(nome=nome, telefone=telefone, email=email, data=data, horario=horario, servico=servico)
        
        # Adicione o novo agendamento ao banco de dados
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Agendamento confirmado!')
        return redirect(url_for('homepage'))

# Rota para o login do administrador
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f'Tentativa de login com usuário: {username}')  # Adicione esta linha
        admin = Admin.query.filter_by(username=username).first()
        if admin:
            print(f'Usuário encontrado: {admin.username}')  # Adicione esta linha
            if admin.check_password(password):
                return redirect(url_for('visualizar_agendamentos'))
            else:
                print('Senha incorreta')  # Adicione esta linha
        else:
            print('Usuário não encontrado')  # Adicione esta linha
        return 'Login inválido'
    return render_template('admin_login.html')


# Rota para logout do administrador
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# Rota para visualizar os agendamentos
@app.route('/admin')
def visualizar_agendamentos():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    agendamentos = Agendamento.query.all()
    return render_template('visualizar_agendamentos.html', agendamentos=agendamentos)

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
