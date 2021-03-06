from vpython import *
#GlowScript 2.9 VPython
'''
Resurse

https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation
https://vpython.org/contents/doc.html
https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
https://www.reddit.com/r/explainlikeimfive/comments/4i1485/eli5_how_does_eulers_method_of_approximation_work/

'''
#PARAMETRII

UA = 149.6e6*1000                               #UA = unitate astronomica(149.6 milioane km) - in metri

masa_soare = 1.98892 * 10**30
raza_soare = 695.7*10**7                        #raza_soare = 695.7*10**5 am modificat cu 10**7 pentru ca nu se vede


distanta_soare_pamant = 1*UA                    #150.68 milioane km, in metri(aproximativ 1 UA)
raza_pamant = 6371*10**5                        #raza_pamant = 6371*10**3 am modificat cu 10**5 pentru ca nu se vede
masa_pamant = 5.9742 * 10**24                   #29.783 km/sec
viteza_pamant = 29.783 * 1000
impuls_pamant = masa_pamant * viteza_pamant     

distanta_soare_venus = 0.723*UA                 #107.9  milioane km, in metri
raza_venus = 6051.8*10**5                       #am schimbat din 10**3 in 10**5 ca sa se vada
masa_venus = 4.8685 * 10**24
viteza_venus = -35.02*1000
impuls_venus = masa_venus * viteza_venus

#cometa cu valori arbitrare
masa_oumuamua = 5*10**14                       #fun - 10**30 / normal - 10**14
viteza_oumuamua = 26.33 * 1000
impuls_oumuamua = masa_oumuamua * viteza_oumuamua

G = 6.67428e-11                                 #constanta gravitationala

dt = 5000                                       #dt = 0.0001, am pus asa mare deoarece am luat niste numere foarte mari
t = 0

def forta_gravitationala(corp1, corp2):
    '''
    calculeaza forta gravitationala exercitata de corpul 2 asupra corpului 1
    In: corp1, corp2 - obiecte
    Out: vectorul fortei exercitat de corpul 2 asuprea corpului 1

    Obs: se foloseste expresia vectoriala
    '''

    #vector distanta
    vector_distanta = corp1.pos - corp2.pos

    #lungimea vectorului distanta
    lungime_vector = mag(vector_distanta)

    #vectorul unitate al vectorului distanta
    vectorul_unitate = vector_distanta/lungime_vector

    #valoarea fortei
    valoarea_fortei = G * corp1.masa * corp2.masa/lungime_vector**2

    #vectorul fortei
    vectorul_fortei = - valoarea_fortei * vectorul_unitate
    
    return vectorul_fortei

soare = sphere(pos = vector(0,0,0), radius = raza_soare, color = color.white,
                masa = masa_soare, impuls = vector(0, 0, 0), make_trail = True)

pamant = sphere(pos = vector(-distanta_soare_pamant, 0, 0), radius = raza_pamant, color = color.blue,
                masa = masa_pamant, impuls = vector(0, -impuls_pamant, 0), make_trail = True)

venus = sphere(pos = vector(distanta_soare_venus, 0, 0), radius = raza_venus, color = color.red,
                masa = masa_venus, impuls = vector(0, -impuls_venus, 0), make_trail = True)

oumuamua = sphere(pos = vector(-2*UA, 1.5*UA, 0), radius = 5*10**8, color = color.green,
                  masa = masa_oumuamua, impuls = vector(impuls_oumuamua, -impuls_oumuamua, 0), make_trail = True)

axa_ox = gcurve(color = color.purple, label = 'x')
axa_oy = gcurve(color = color.orange, label = 'y')
axa_oz = gcurve(color = color.magenta, label = 'z')

def animatie(t, dt):
    '''
    distanta derivata = viteza
    viteza derivata = acceleratia etc.
    Cunoscand viteza in fiecare moment si directia vectorului viteza, calculez distanta parcursa
    folosind metoda Euler-Cromer de integrare.
    
    Observatie: Valorile sunt schimbate. Daca as pune un dt = 0.0001 as obtine o simulare realista,
                deci nu s-ar putea observa efectul in timp util. Nu pot modifica vitezele deoarece
                planetele ar iesi din orbita(escape velocity)
    '''
    
    while True:

        #de cate ori se executa pe secunda
        rate(1000)
    
        soare.forta = forta_gravitationala(soare, pamant) + forta_gravitationala(soare, venus)   + forta_gravitationala(soare, oumuamua)
        pamant.forta = forta_gravitationala(pamant, soare) + forta_gravitationala(pamant, venus) + forta_gravitationala(pamant, oumuamua) 
        venus.forta = forta_gravitationala(venus, soare) + forta_gravitationala(venus, pamant)   + forta_gravitationala(venus, oumuamua)
        oumuamua.forta = forta_gravitationala(oumuamua, soare) + forta_gravitationala(oumuamua, pamant) + forta_gravitationala(oumuamua, venus)

        #modific impulsul
        soare.impuls += soare.forta*dt
        pamant.impuls += pamant.forta*dt
        venus.impuls += venus.forta*dt
        oumuamua.impuls += oumuamua.forta*dt
        
        #modific pozitiile
        soare.pos += soare.impuls/soare.masa*dt
        pamant.pos += pamant.impuls/pamant.masa*dt
        venus.pos += venus.impuls/venus.masa*dt
        oumuamua.pos += oumuamua.impuls/oumuamua.masa*dt
    
        t += dt
        
        #Grafic oumuamua
        axa_ox.plot(pos=(t, oumuamua.pos.x))
        axa_oy.plot(pos=(t, oumuamua.pos.y))
        axa_oz.plot(pos=(t, oumuamua.pos.z))
        
animatie(t, dt)