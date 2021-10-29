#!/usr/bin/python3

# 2021/10/26 PSR
# BP
# Part 03 - # 2021/10/21 PSR
# Exercício 1 - Tempo e Temporizadores

from colorama import Fore, Back, Style
import time
import argparse
import readchar
from random import seed, randint

asciicharmin = 97
asciicharmax = 122
tempojogo = 0
numerocaract = 0
stop_key = ' '
pressed_keys = []  # empty list to start with
dicResult = {}
Input = namedtuple('Input', ['requested', 'received', 'duration'])
registo = []

def tic():
    return time.time()

def toc( inicio):
    return time.time() - inicio


def readAllUpToTime(inicio, tempojogo, stop):

    contatentativas = 0
    charcertos = 0

    print('Tempos' + str(inicio) + '  tempo jogo:' + str(tempojogo))
    # Ask for all the entries and put them in a list
    while ( (toc(inicio) ) < tempojogo):

        valueChar = randint(asciicharmin, asciicharmax)
        inicioInput = tic()
        print('Type -> '+ chr(valueChar)+'('+stop+' to stop)')
        pressed_key = readchar.readkey()
        fimInput = toc(inicioInput)

        registo.append(Input(chr(valueChar), pressed_key, fimInput - inicioInput))

        if pressed_key == stop:
            print('You typed ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL
                  + ' terminating.')
            break
        else:
            contatentativas = contatentativas + 1
            if pressed_key == chr(valueChar):
                charcertos = charcertos + 1
                #print('acertas-te ')
                # print('Thank you for typing ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL)
            pressed_keys.append(pressed_key)

    #print('Acertou : ' +str(charcertos))


    dicResult = {'accuracy': (charcertos / contatentativas), 'inputs': registo,
                 'number_of_hits': charcertos, 'number_of_types': contatentativas,
                 'test_duration': (tic() - inicio),
                 'test_end': time.ctime(tic()),
                 'test_start': time.ctime(inicio)}

    print(dicResult)

def readAllUpToCaract(inicio, numerocarac, stop):

    contacaracteres = 0
    contatentativas = 0
    charcertos = 0

    print('Tempos' + str(inicio) + '  tempo jogo:' + str(tempojogo))
    # Ask for all the entries and put them in a list
    while ( contacaracteres< numerocarac):

        valueChar = randint(asciicharmin, asciicharmax)
        print('Type -> ' + chr(valueChar) + '(' + stop + ' to stop)')
        pressed_key = readchar.readkey()

        if pressed_key == stop:
            print('You typed ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL
                  + ' terminating.')
            break
        else:
            contatentativas = contatentativas + 1
            if pressed_key == chr(valueChar):
                charcertos = charcertos + 1
            # print('Thank you for typing ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL)
            pressed_keys.append(pressed_key)

        contacaracteres = contacaracteres +1

    print('Acertou : ' +str(charcertos))


def main():

    # usage: main.py [-h] [-utm] [-mv MAX_VALUE]
    parser = argparse.ArgumentParser(description='Parametros do Trabalho Pratico N1', prog='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
 #   parser.add_argument('-h', '--help', help='Ajuda, ver opcoes do programa')
    parser.add_argument('-utm', '--use_time_mode', action='store_true',  help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv MAX_VALUE', '--max_value MAX_VALUE', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
  #  parser.print_help()
    args = vars(parser.parse_args())
    print(args)

    opfuncionamento = 2 # vai funcionar por numero de caracteres
    if args['use_time_mode']:
        print("O utilizador definiu tempo maximo :"+ str(args['use_time_mode']))
        opfuncionamento = 1

    if args['max_value MAX_VALUE']:
        if (opfuncionamento == 1):
            tempojogo = args['max_value MAX_VALUE']
        else:
            numerocaract = args['max_value MAX_VALUE']

    seed(1)
    inicio = tic()
    seconds = time.time()

    print("O utilizador escolheu a operação ::" + str(opfuncionamento) + '  com o valor max::' + str(args['max_value MAX_VALUE']))

    print( "Para iniciar carregue numa tecla pf")

    #Funciona durante o tempo que o utilizador indicou
    if (opfuncionamento == 1):
        # fazer enquanto estiver dentro do tempo definido
        # nao esquecer que quando o utilizador carrega no espaço, termina
        readAllUpToTime(inicio, tempojogo, stop_key)

    # Funciona pelo numero de carecteres que o utilizador indicou
    if (opfuncionamento == 2):
        # nao esquecer que quando o utilizador carrega no espaço, termina
        readAllUpToCaract(inicio, numerocaract, stop_key)

    print(pressed_keys)

    local_time = time.ctime(seconds)
    print("This is" + Fore.RED + "Ex1" + Style.RESET_ALL + " Local time:" + Fore.BLUE + Back.GREEN + local_time + Style.RESET_ALL)

    fim = toc(inicio);
    print('Ellapsed time: ', fim)

    # TODO : Check this
    print(" ++++++++++++ FIM ++++++++++++++ ")
    print(registo)

    print(dicResult)


if __name__ == '__main__':
    main()


