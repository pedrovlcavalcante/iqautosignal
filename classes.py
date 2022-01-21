from datetime import datetime, date
import json


class Sinal():
    def __init__(self, lista) -> None:
        self.hora = lista[0]
        self.par = lista[1]
        self.direcao = lista[2]
        self.expiracao = int(lista[3])
        self.id = 0


class Horario():
    """Retorna Timestamp da hora atual e do sinal"""

    def __init__(self, sinal) -> None:
        self.t = date.today().strftime("%Y-%m-%d") + " " + sinal.hora + ":00"
        hoje = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.hora_atual = datetime.strptime(hoje, "%Y-%m-%d %H:%M:%S")
        self.hora_sinal = datetime.strptime(self.t, "%Y-%m-%d %H:%M:%S")
        self.ts_sinal = datetime.timestamp(self.hora_sinal)
        self.ts_atual = datetime.timestamp(self.hora_atual)
        self.diferenca = self.ts_sinal - self.ts_atual

    def atualiza(self):
        hoje = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.hora_atual = datetime.strptime(hoje, "%Y-%m-%d %H:%M:%S")
        self.ts_atual = datetime.timestamp(self.hora_atual)
        self.diferenca = self.ts_sinal - self.ts_atual
        return self.diferenca


class Operacao():
    def __init__(self, op) -> None:
        self.op = op


def lista_sinais(texto='sinais.txt'):
    sinais = []
    with open(texto, 'r') as lista:
        for line in lista.readlines():
            sinais.append(Sinal(line.split(';')))
    return sinais


def conecta(api):
    check, reason = api.connect()  # connect to iqoption
    while True:
        if check:
            print('Conectado com sucessso!')
            print(api.get_balance_mode())
            print(api.get_balance())
            break
        else:
            if json.loads(reason)['code'] == 'invalid_credentials':
                print('Senha errada')
                break
            else:
                print(json.loads(reason)['code'])
                break


def payout(api, par, tipo, timeframe):
    if tipo == 'binary' or tipo == 'turbo':
        a = api.get_all_profit()
        return int(100 * a[par][tipo])

    elif tipo == 'digital':
        api.subscribe_strike_list(par, timeframe)
        while True:
            d = api.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
        api.unsubscribe_strike_list(par, timeframe)
        return d


def compra(api, valor, sinal, tipo):
    entrada = valor
    expiration = sinal.expiracao
    print('Excutando Sinal')
    if tipo == 'digital':
        check, id = api.buy_digital_spot(
            sinal.par, entrada, sinal.direcao, expiration)
    else:
        check, id = api.buy(entrada, sinal.par,
                            sinal.direcao, expiration)
    return check, id


def martingale(api, valor, sinal, tipo):
    print('Sinal passado para o Gale')
    print('Sinal: ', sinal.par, 'Tipo: ', tipo)
    if tipo == 'digital':
        while True:
            check, win = api.check_win_digital_v2(sinal.id)
            if check:
                break
    else:
        win = api.check_win_v3(sinal.id)
    if win < 0:
        print('Executando Gale')
        check, id = compra(api, valor*2, sinal, tipo)
        if check:
            print('Gale executado com sucesso!')
        else:
            print('Não foi possível executar o Gale!')
    else:
        print('Lucro: R$ ', win)


def aberto(ALL_Asset, sinal, api):
    digital = (ALL_Asset["digital"][sinal.par]["open"])
    turbo = (ALL_Asset["turbo"][sinal.par]["open"])
    binary = (ALL_Asset["binary"][sinal.par]["open"])
    tipos = ['digital', 'turbo', 'binary']
    payouts = {}
    if digital and turbo and binary:
        for tipo in tipos:
            payouts = {tipo: payout(api, sinal.par, tipo, sinal.expiracao)}
    elif digital:
        payouts['digital'] = payout(api, sinal.par, 'digital', sinal.expiracao)
    elif turbo:
        payouts['turbo'] = payout(api, sinal.par, 'turbo', sinal.expiracao)
    elif binary:
        payouts['binary'] = payout(api, sinal.par, 'binary', sinal.expiracao)
    else:
        return None, None

    tipo = max(payouts, key=payouts.get)
    return tipo, payouts[tipo]
