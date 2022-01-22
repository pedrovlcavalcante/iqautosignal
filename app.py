from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from iq import profits
from threading import Thread

app = Flask(__name__)

# app.config.from_object(__name__)
sess = Session()


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":

        valores = request.form["sinal"]
        session['email'] = request.form["email"]
        session['senha'] = request.form["senha"]
        session['valor'] = int(request.form["valor"])
        with open('sinais.txt', 'w') as lista:
            for sinal in valores.split(' '):
                lista.write(f'{sinal}\n')
                print(sinal)
        # print(sinais)
        return redirect('/sinal')
        # print("A Executar")
        # p1 = Thread(target=profits, args=[email, senha, valor])
        # p1.start()
        # print("Executado")
    return render_template('home.html')


@app.route('/sinal', methods=["POST", "GET"])
def sinal():
    if request.method == 'GET':

        email = session.get('email')
        senha = session.get('senha')
        valor = session.get('valor')
        print("A Executar")
        p1 = Thread(target=profits, args=[email, senha, valor])
        p1.start()
        print("Executado")
    return 'Oi'


if __name__ == '__main__':
    app.secret_key = 'supersecret'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=True)
