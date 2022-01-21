from flask import Flask, render_template, request
from iq import profits
from threading import Thread

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        valores = request.form["sinal"]
        email = request.form["email"]
        senha = request.form["senha"]
        valor = int(request.form["valor"])
        with open('sinais.txt', 'w') as lista:
            for sinal in valores.split(' '):
                lista.write(f'{sinal}\n')
                print(sinal)
        # print(sinais)
        print("A Executar")
        p1 = Thread(target=profits, args=[email, senha, valor])
        p1.start()
        print("Executado")
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
