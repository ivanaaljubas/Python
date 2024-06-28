import random

kocka1=0
kocka2=0

igra_aktivna=True

def provjeriKrajIgre():
    global igra_aktivna
    while True:
        odgovor=input('Želiš li igrati ponovno (d/n)?')
        if odgovor.lower() == 'd':
            igra_aktivna=True
            break
        elif odgovor.lower()=='n':
            igra_aktivna=False
            break
        else:
            print('Unesite odgovarajući znak: d ili n')
def provjeriPobjedu():
    if kocka1 > kocka2:
        print(f'Prvi igrac je dobio {kocka1}, a drugi je dobio {kocka2}.')
        print('Pobijedio je igrac 1.\n')

    elif kocka2 > kocka1:
        print(f'Prvi igrac je dobio {kocka1}, a drugi je dobio {kocka2}.')
        print('Pobijedio je igrac 2.\n')
    else:
        print(f'Prvi igrac je dobio {kocka1}, a drugi je dobio {kocka2}.')
        print('Neriješeno!\n')


def provjeriRezultatIgre():
    pass

def igrajBacanjeKocke():
    global kocka1, kocka2
    while igra_aktivna:
        kocka1=random.randint(1, 6)
        kocka2=random.randint(1,6)
       
        provjeriPobjedu()
        provjeriKrajIgre()

igrajBacanjeKocke()
    
