from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from iq import profits
from threading import Thread, active_count, enumerate

app = Flask(__name__)
app.secret_key = 'supersecret'
# app.config.from_object(__name__)
sess = Session()


@app.route('/', methods=["POST", "GET"])
def home():
    num_threads = active_count()
    for t in enumerate():
        print(t.name)
    print(num_threads)
    if request.method == "POST":

        try:
            valores = request.form["sinal"]
            session['email'] = request.form["email"]
            session['senha'] = request.form["senha"]
            session['valor'] = int(request.form["valor"])
            session['balance'] = request.form["balance"]
            session['meta'] = int(request.form["meta"])
            session['loss'] = int(request.form["loss"])
        except Exception as e:
            print("ERRO NOS DADOS: ", e)
        try:
            session['auto'] = request.form["auto"]
        except:
            session['auto'] = False

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

    return render_template('home.html', num_threads=num_threads)


@app.route('/sinal', methods=["POST", "GET"])
def sinal():
    if request.method == 'GET':

        email = session.get('email')
        senha = session.get('senha')
        auto = session.get('auto')
        if auto:
            valor = 0
        else:
            valor = session.get('valor')
        balance = session.get('balance')
        meta = session.get('meta')
        loss = session.get('loss')
        print("A Executar")
        p1 = Thread(target=profits, args=[
                    email, senha, valor, balance, auto, meta, loss])
        p1.setName(f"Sinal {active_count()}")
        p1.start()

        threads = enumerate()
        num_threads = active_count()

        print("Executado")
    return render_template('home.html', threads=threads, num_threads=num_threads)


if __name__ == '__main__':
    app.secret_key = 'supersecret'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=True)
