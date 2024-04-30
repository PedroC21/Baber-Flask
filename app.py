import os
from flask import Flask, render_template, request

# Cria uma instância do aplicativo Flask
app = Flask(__name__)
app.static_folder = 'static/'


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