from ejtraderIQ.stable_api import IQ_Option
from classes import Horario, lista_sinais, conecta, payout, martingale, compra, aberto
# from concurrent.futures import ThreadPoolExecutor
from threading import Thread
# from classes import *
from os import system
# from iqoptionapi.iqoptionapi.stable_api import IQ_Option


def profits(email, senha, valor, balance, auto, meta, loss):

    sinais = lista_sinais()

    api = IQ_Option(email, senha)

    # if api.check_connect():
    #     print('Já conectado')
    # else:
    conecta(api, balance)
    api.update_ACTIVES_OPCODE()
    inicio = api.get_balance()
    print("auto", auto)
    for sinal in sinais:
        if auto:
            valor = 0.01*api.get_balance()
            if valor < 2:
                valor = 2
        print(f'Valor do investimento: {valor}')
        print(f'Meta: {meta}% | R$ {0.01*meta*inicio}')
        print(f'Stop: {-loss}% | R$ {0.01*loss*inicio}')
        # Verificação de meta diária

        if ((api.get_balance() - inicio) / inicio)*100 >= meta:
            print("Objetivo diário atingido")
            break
        elif ((api.get_balance() - inicio) / inicio)*100 <= -loss:
            print("Stop Loss diário atingido")
            break
        print(
            f'Aguardando Sinal: {sinal.par}, {sinal.hora}, {sinal.direcao}, {sinal.expiracao}')
        horario = Horario(sinal)
        print(horario.diferenca)
        ALL_Asset = api.get_all_open_time()
        tipo, pay = aberto(ALL_Asset, sinal, api=api)

        # tipo = 'digital'

        if tipo == None:
            print('Par fechado, passando para o próximo sinal.')
            continue
        print(tipo, pay)
        if horario.diferenca < 0:
            print('Sinal atrasado')
            continue
        else:
            while True:
                while horario.diferenca >= 2:
                    x = horario.atualiza()
                    # print('Faltam ', horario.diferenca)
                    pay = payout(api, sinal.par, tipo, sinal.expiracao)
                    # print('Payout: ', pay)
                    # system('cls')
                if pay < 80:
                    print('Payout insuficiente, aguardando próximo sinal.')
                    break
                elif horario.diferenca <= 2:
                    try:
                        check, id = compra(api, valor, sinal, tipo)
                    except TypeError as e:
                        print('ERRO NA COMPRA')
                        print('passando para o próximo sinal')
                        break
                    print('Validação')
                    print(check)
                    print(id)
                    sinal.id = id
                    if check:
                        print("Compra realizada")
                        print('ID do Sinal: ', sinal.id)
                        args = [api, valor, sinal, tipo]
                        # executor = ThreadPoolExecutor()
                        # executor.submit(lambda x: martingale(*x), args)
                        executor = Thread(target=martingale, args=args)
                        executor.setName(f'Gale {sinal.hora}')
                        executor.start()
                        # win = api.check_win_v3(id)
                        # print('Checando vitoria?')
                        # if win < 0:
                        #     print('Executando Gale')
                        #     check, id = compra(api, valor*2, sinal)
                        #     if check:
                        #         print('Gale executado com sucesso!')
                        #     else:
                        #         print('Não foi possível executar o Gale!')
                        # else:
                        #     print('Lucro: R$ ', win)
                        print('Passando para o próximo sinal')
                        break
                    else:
                        print("Não foi possível comprar")
                        break

    print('Fim da Lista')
