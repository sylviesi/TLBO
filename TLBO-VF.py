import math
import random
import time

temps = time.process_time()

print("entrer la taille de la population")
popsize = int(input())
print("entrer le profil 1,2 ou 3")
profil=int(input())
print("entrer le nb d'itérations")
nb_ite=int(input())
A = 1000
Cp = 100
hr = 0.1
P = []
T = []
B = []
TP = []
wselect = []  # liste qui retiens les individus sélectionnés par la méthode de la roulette
listecross = [] # liste qui retiens les individus qui sont sélectionnés pour le croisement
best = 0
besti=0
'''On déclare et on initialise les variables globales qui vont servir dans le reste de l'algo'''

def calc_TP (p,t,b):
    global A,hr,Cp,profil
    phi = 30 * (1 - math.exp(-b / 1195))
    D = demande(profil,p)
    Q = t * D
    tp = ((p + phi) * D - (A * D / Q) - (Cp * D) - (hr * Cp * Q * 0.5) - b)
    return (tp)
'''C'est la fonction qui sert à calculer la valeur de la fitness fonction selon les variables d'entrée'''

def demande (profil,p):

    if profil==1:
        D = -0.003539 * (p ** 3) + 2.1215 * (p ** 2) - 413.3 * p + 26580
        return (D)
    elif profil==2:
        D = -0.002703 * (p ** 3) + 1.577 * (p ** 2) - 296.8 * p + 18413
        return (D)
    else:
        D = -0.0023 * (p ** 3) + 1.35 * (p ** 2) - 254.5 * p + 15500
        return (D)
'''Fonction qui sert à  calculer la demande selon le profil sélectionné pour l'utilisateur'''

def inititialisation ():
    global A, Cp, hr,total2,P,best,besti
    best=0
    besti=0
    TP[:]= []
    P[:]= []
    T[:] = []
    B[:] = []
    for i in range(popsize):
        tpm=-1
        while tpm < 0:
            pi = random.uniform(170, 270)
            ti = random.random()
            bi = random.uniform(0, 15000)
            tpm=calc_TP(pi,ti,bi)

        P.append(pi)
        T.append(ti)
        B.append(bi)
        TP.append(tpm)
'''Dans cette fontion d'initialisation, on génère une population de façon "aléatoire" en respectant les contraintes
   imposées dans l'article. On interdit également des valeurs nules pour la fitness fonction. '''


def teacher():
    global P,T,B,TP,popsize
    teacher1 =max(TP)
    i_teacher1=TP.index(teacher1)
    mean_P=sum(P)/popsize
    mean_T=sum(T)/popsize
    mean_B=sum(B)/popsize
    DM_P=random.random()*(P[i_teacher1]-mean_P)
    DM_T=random.random()*(T[i_teacher1]-mean_T)
    DM_B=random.random()*(B[i_teacher1]-mean_B)

    for i in range(popsize):
        pi=P[i] + DM_P
        if pi<170:
            pi=170
        elif pi>270:
            pi = 270

        ti = T[i] + DM_T
        if ti <= 0:
            ti = 2 ** (-53)
        elif ti > 1:
            ti = 1

        bi=B[i] + DM_B
        if bi <= 0:
            bi = 2 ** (-53)
        elif bi > 15000:
            bi = 15000
        '''On calcule les nouvealles valeurs de (P, T et B) et on varifie qu'elle restent bien dans les intervalles 
        imposées dans l'article'''

        tpm=calc_TP(pi,ti,bi)

        if tpm>TP[i]:
            TP[i]=tpm
            P[i] = pi
            T[i] = ti
            B[i] = bi

    return (max(TP))
'''Dans cette partie, on sélectionne le meilleur individu qui sera concidéré comme le proffeseur et il va apprendre 
aux autres individus pour qu'ils puissent progresser.'''

def learner():
    global P,T,B,TP, popsize,best,besti

    for i in range(popsize):
        tirage1 = random.randint(0, popsize-1)
        tirage2=tirage1
        while tirage2 != tirage1:
            tirage2 = random.randint(0, popsize-1)

        max(TP[tirage1], TP[tirage2])
        maxi = TP.index(max(TP[tirage1], TP[tirage2]))
        mini = TP.index(min(TP[tirage1], TP[tirage2]))

        pi = P[mini] + random.random() * (P[maxi] - P[mini])
        if pi < 170:
            pi = 170
        elif pi > 270:
            pi = 270

        ti = T[mini] + random.random() * (T[maxi] - T[mini])
        if ti <= 0:
            ti = 2 ** (-53)
        elif ti > 1:
            ti = 1

        bi = B[mini] + random.random() * (B[maxi] - B[mini])
        if bi <= 0:
            bi = 2 ** (-53)
        elif bi > 15000:
            bi = 15000

        tpm = calc_TP(pi,ti, bi)

        if tpm > TP[mini]:
            TP[mini] = tpm
            P[mini] = pi
            T[mini] = ti
            B[mini] = bi

    if max(TP)>best:
        best=max(TP)
        besti=index
    return
'''Dans cette partie, les individus vont être sélectionnés deux par deux de façon aléatoire et ils vont apprendre l'un 
de l'autre. Le moins bon individu de chaque pair va apprendre du meilleur de la pair et si la solution obtenue avec
l'apprentissage du moins bon est meilleur que celle originale alors la solution modifiée sera conservée.'''


result=[]
result2=[]
for x in range(nb_ite):
    test=inititialisation()
    global index
    for index in range(100):
        test2=teacher()
        test3=learner()
    result.append(best)
    result2.append(besti)
print("moyenne Tp",sum(result) / nb_ite)
print("besti=",sum(result2)/nb_ite)
print("tps de calc",time.process_time() - temps)


