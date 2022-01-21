from flask import Flask, render_template, request, redirect
from iq import profits
from threading import Thread

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":

        valores = request.form["sinal"]
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
    if request.method == 'POST':

        email = request.form["email"]
        senha = request.form["senha"]
        valor = int(request.form["valor"])
        print("A Executar")
        p1 = Thread(target=profits, args=[email, senha, valor])
        p1.start()
        print("Executado")
    return 'Oi'


if __name__ == '__main__':
    app.run(debug=True)
