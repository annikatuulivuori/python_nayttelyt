#!/usr/bin/env python

# TODO: näyttelyn lisääminen hakeminen tietokannasta
# TODO: tuomarin lisääminen tietokantaan ja hakeminen tietokannasta
# TODO: lisaa_tulos ja lisaa_titteli -funktioille id-haku omaan aliohjelmaan (?)

import sys
import psycopg2

conn = psycopg2.connect(host="88.115.137.130",dbname="tjta3501", user="kissat",password="kissa123")

def loyda_kissa(kissa):
    # TODO: kissan tietojen tulostus sarakkeiden nimien kanssa
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM kissa WHERE rek_nimi = %s;"
        cur.execute(sql, (kissa,))
        kissan_tiedot = cur.fetchall()
        cur.close()
        
        if kissan_tiedot == None:
            print()
            print("Ei löytynyt kissaa")
            return None
            
        valinta = input("Tulostetaanko tiedot? (k=kyllä, e=ei) ")
        
        if valinta == "k":
            print(kissan_tiedot)
        else:
            return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def loyda_kissa_id(kissa):
    try:
        cur = conn.cursor()
        sql = "SELECT id FROM kissa WHERE rek_nimi = %s;"
        cur.execute(sql, (kissa,))
        kissa_id = cur.fetchone()[0]
        cur.close()
        
        if kissa_id == None:
            print ("Virhe: kissa_id")
        else:
            return kissa_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def nayta_tulokset(kissa_id):
    try:
        cur = conn.cursor()
        sql = "SELECT tulos FROM tulos2 JOIN kissa ON tulos2.kissa_id = kissa.id WHERE kissa_id = %s ORDER BY tulos2.id DESC LIMIT 5;"
        cur.execute(sql, (kissa_id,))
        tulokset = cur.fetchall()
        cur.close()
        
        if tulokset == None:
            print()
            print("Ei löytynyt tuloksia")
            return None
        else:
            print()
            print('Uusimmat näyttelytulokset: ')
            for x in tulokset:
                print(x)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    main()
        
def nayta_tittelit(kissa_id):
    try:
        cur = conn.cursor()
        sql = "SELECT luokka FROM titteli JOIN kissa ON titteli.kissa_id = kissa.id WHERE kissa.id = %s ORDER BY titteli.id DESC LIMIT 6;"
        cur.execute(sql, (kissa_id,))
        loydetyt = cur.fetchall()
        cur.close()
        
        if loydetyt == None:
            print()
            print("Ei löytynyt titteleitä")
            return None
        else:
            print()
            print('Kissan tittelit: ')
            for x in loydetyt:
                print(x)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    main()
        
def lisaa_tulos(kissa_id):
    # TODO: tulokseen relaatio tauluihin nayttely ja tuomari (ei toimi tällä versiolla)
    
    try:
        cur = conn.cursor()
        count_sql = "SELECT COUNT(*) FROM tulos2;"
        cur.execute(count_sql)
        tulos_id = cur.fetchone()[0]
        tulos_id += 1
        
        tulos = input("Syötä kissan näyttelytulos > ")
        sql = "INSERT INTO tulos2 VALUES (%s, %s, %s);"
        cur.execute(sql, (tulos_id, kissa_id, tulos,))
        conn.commit()
        cur.close()
        
        print('Lisättiin näyttelytulos: ', tulos)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    main()

def lisaa_titteli(kissa_id):    
    luokka = input("Syötä kissan uusi luokka > ")
    pvm = input("Syötä uuden tittelin päivämäärä (DD.MM.YYYY) > ")
    v_pvm = input("Syötä tittelin vahvituksen päivämäärä (DD.MM.YYYY) > ")
    
    try:
        cur = conn.cursor()
        count_sql = "SELECT COUNT(*) FROM titteli2;"
        cur.execute(count_sql)
        titteli_id = cur.fetchone()[0]
        titteli_id += 1
        sql = "INSERT INTO titteli2 VALUES (%s, %s, %s, %s, %s);"
        cur.execute(sql, (titteli_id, kissa_id, luokka, pvm, v_pvm,))
        conn.commit()
        cur.close()
        
        print('Lisättiin titteli: ', luokka)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    main()   
        
def lopeta():
    print("Hei hei! :)")
    if conn is not None: conn.close()
    sys.exit()

def main():
    print("===================")
    print("1) Näytä tulokset")
    print("2) Näytä titteli")
    print("3) Lisää tulos")
    print("4) Lisää titteli")
    print("5) Lopeta")
    print()
    
    valinta = int(input("Mitä haluat tehdä? > "))
    if valinta == 1:
        nayta_tulokset(kissa_id)
    elif valinta == 2:
        nayta_tittelit(kissa_id)
    elif valinta == 3:
        lisaa_tulos(kissa_id)
    elif valinta == 4:
        lisaa_titteli(kissa_id)
    elif valinta == 5:
        lopeta()
    else:
        print("Virheellinen valinta")
        
kissa = input("Syötä kissan nimi > ")
kissa_id = int(loyda_kissa_id(kissa))
kissa = loyda_kissa(kissa)

main()