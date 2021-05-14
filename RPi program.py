#-------------------------------------------------------------------------------------#
####### BIBLIOTEKER #######
import requests                # Lib should be included in latest python versions else do: python -m pip install requests   
import json                    # Lib should be included in latest python versions else do: python -m pip install json 
from time import time          # Skal det ligge en tidsfunksjon for å fjerne gjester?
import datetime                # Bibliotek med sanntidsklokke
from firebase import firebase  # Firebase bibliotek for python
from yr.libyr import Yr        # API for å importere fra yr

#-------------------------------------------------------------------------------------#
####### FUNKSJONER #######
def les_cot(data):
    payload = data
    response=requests.get('https://circusofthings.com/ReadValue',params=payload)
    datahandling=json.loads(response.content)  
    return datahandling["Value"]

def lag_cot_dict(key, value, token):
    """ Lager CoT-variabel (key, verdi, token) """
    data ={'Key':'0','Value':0,'Token':'0'}
    data['Key']= key
    data['Value']=value
    data['Token']=token
    return data

def motatt_signal(send_key, svar_key, id_key, token):
    """Om send signal og svar signal er 1, gi ID"""
    datasett_send = lag_cot_dict(send_key, 0, token)
    datasett_svar = lag_cot_dict(svar_key, 0, token)
    datasett_id = lag_cot_dict(id_key, 0, token)
    var1 = les_cot(datasett_send)
    var2 = les_cot(datasett_svar)
    var3 = les_cot(datasett_id)
    if((int(var1) == 1) and (int(var2) == 1)):
        return var3
    else:
        return True
    
def send_cot(key, value, token):
    """ Lager CoT-variabel (key, verdi, token) """
    data ={'Key':'0','Value':0,'Token':'0'}
    data['Key']= key
    data['Value']=value
    data['Token']=token
    response=requests.put('https://circusofthings.com/WriteValue',
				data=json.dumps(data),headers={'Content-Type':'application/json'})
    if(response.status_code==200):
        print("Suksessfull sending til CoT")
        return data
    
def f(qty, item, size, time): #Definerer hva funksjonen skal inneholde
    forbruk= (qty*size*time) #Hvordan bergne forbruket pr vare 
    return forbruk 

#-------------------------------------------------------------------------------------#
####### WEB SERVER #######
firebase = firebase.FirebaseApplication('https://prosjekt-vaar-2021-default-rtdb.firebaseio.com', None) ##finner databasen
resultat = firebase.get('/Gjester', None)           ##all data ligger under Gjester


resultat_liste = list(resultat)
gjester_liste = []
gjester_liste_old = []

for i in resultat_liste:                            ## Lager liste over alle gjestene registrert på Firebase
    var = list(resultat[i])
    for gjest in var:
        gjester_liste_old.append(gjest)
        gjester_liste.append(gjest)

                                                    ## Variabler for gjesteregistrering logikk. 
                                                    ##  Variablene er like, med forskjellige navn for beboerne
timer_gjester_Nina1, timer_gjester_Tor1, timer_gjester_Maja1, timer_gjester_Hanne1, timer_gjester_Hanna1 = True, True, True, True, True
antall_gjester_Nina, antall_gjester_Tor, antall_gjester_Maja, antall_gjester_Hanne, antall_gjester_Hanna = 0, 0, 0, 0, 0
antall_gjester_Nina_old, antall_gjester_Tor_old, antall_gjester_Maja_old, antall_gjester_Hanne_old, antall_gjester_Hanna_old = 0, 0, 0, 0, 0
timer_gjester_Nina, timer_gjester_Tor, timer_gjester_Maja, timer_gjester_Hanne, timer_gjester_Hanna = 0, 0, 0, 0, 0
timer_gjester_Nina2_aktiv, timer_gjester_Tor2_aktiv, timer_gjester_Maja2_aktiv, timer_gjester_Hanne2_aktiv, timer_gjester_Hanna2_aktiv = False, False, False, False, False
timer_gjester_Nina1_aktiv, timer_gjester_Tor1_aktiv, timer_gjester_Maja1_aktiv, timer_gjester_Hanne1_aktiv, timer_gjester_Hanna1_aktiv = False, False, False, False, False

booking_lengde = 0
sum_registrerte = 0
sum_registrerte_old = 1

#-------------------------------------------------------------------------------------#
####### VARIABLER #######
## Variabler for CoT
token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0OTk0In0.U2OYCiZTQR1tyb9o-E-mssfC1Xtu0wuTXUwgSpmsri0"
send_key = "14157"
send_til_rom_key = "28932"
svar_key = "412"
id_key = "27790"
endre_gjester_id_key = "23286"
endre_gjester_send_key = "30901"
booking_id_key = "2894"
booking_lengde_key = "10068"
booking_send_key = "2095"
temp_key = "2311"
skydekke_key = "24800"
stromforbruk_key = "19652"
rom_key_liste = ["9270", "29056", "10157", "21483", "13942", "29211", "11379"]
booking_key_liste = ["27684", "14119", "12849"]
# Lager datasett til CoT
datasett_send = lag_cot_dict(send_key, 0, token)
datasett_svar = lag_cot_dict(svar_key, 0, token)
datasett_send_rom = lag_cot_dict(send_til_rom_key, 0, token)
datasett_gjester_id =lag_cot_dict(endre_gjester_id_key, 0, token)
datasett_gjester_send = lag_cot_dict(endre_gjester_send_key, 0, token)
datasett_booking_id = lag_cot_dict(booking_id_key, 0, token)
datasett_booking_lengde = lag_cot_dict(booking_lengde_key, 0, token)
datasett_booking_send = lag_cot_dict(booking_send_key, 0, token)
send_cot(send_til_rom_key, 0, token)                # Nulstiller sendesignal til rom

## Variabler for booking
antall_bad = 0
antall_bad_old = 0
bad_booking = 0
first_syklus_bad = True

antall_kjokken = 0
antall_kjokken_old = 0
kjokken_booking = 0
timer_kjokken = 0
timer_kjokken1 = True
timer_kjokken2_aktiv = False
timer_kjokken1_aktiv = False

antall_stue = 0
antall_stue_old = 0
stue_booking = 0
timer_stue = 0
timer_stue1_aktiv = False
timer_stue2_aktiv = False
timer_stue3_aktiv = False

booking_send_old = False
sum_reserverte_gammel = 1

## Variabler for gjesteliste
gjesteliste = [0, 0, 0, 0, 0, 0, 0] 
gammelt_motatt = False
motatt_rom = True
sum_gjesteliste_gammel = 1
gammelt_legge_til = False
gammelt_fjerne = False

#-------------------------------------------------------------------------------------#
    ####### PROGRAM-LOOP #######

while(True):
    ####### GJESTER #######
    send_ringeklokke = les_cot(datasett_send)       ## Send signal fra ringeklokke
    motatt_rom = motatt_signal(send_til_rom_key, svar_key, id_key, token) 
    ### Legge til gjester manuelt
    gjester_id = (les_cot(datasett_gjester_id)-1)
    gjester_send = les_cot(datasett_gjester_send)
    if(gjester_send == 1):                          ## Signal om å legge til gjest manuelt
            if((gjesteliste[gjester_id]<2) and not gammelt_legge_til and (sum(gjesteliste)<5)): ## Betingelse på antall gjester tillat
                gjesteliste[gjester_id] = gjesteliste[gjester_id] + 1 
                gammelt_legge_til = True
            else:
                gammelt_legge_til = False
    ## Fjerne gjester
    if(sum(gjesteliste)>0):                         ## Betingelse på at det må være gjester som er registrert
        if(gjester_send == 2):                      ## Signal om å fjerne gjest manuelt
            if((gjesteliste[gjester_id]>0) and not gammelt_legge_til):
                gjesteliste[gjester_id] = gjesteliste[gjester_id] - 1  ## Fjern en gjest registrert på beboeren valgt
                gammelt_fjerne = True
        else:
            gammelt_fjerne = False
    if(sum(gjesteliste) < 5):                       ## Betingelse på at det ikke kan legges til fler en 5 gjester totalt
        if(send_ringeklokke == 1):                  ## Betingelse på at det sendes ringesignal fra ringeklokken
            if((gjesteliste[motatt_rom - 1] < 2)):  ## Betingelse på at det ikke kan legges til fler en 2 gjester totalt per beboer
                send_cot(send_til_rom_key, 1, token)## Mulighet til å sende ringesignal videre til konsollet - Sender singnal
            else:
                send_cot(send_til_rom_key, 0, token)## Mulighet til å sende ringesignal videre til konsollet - Sender ikke signal
                send_cot(svar_key, 2, token)        ## Sender svar til ringeklokke om at gjest får ikke komme inn
        else:
            send_cot(send_til_rom_key, 0, token)
    else:
        send_cot(send_til_rom_key, 0, token)
        send_cot(svar_key, 2, token)                ## Sender svar til ringeklokke om at gjest får ikke komme inn
    ## Legge til gjester automatikk
    if (motatt_rom is not True):                    ## Betingelse på at det skal legges til en ny gjest
        if(gammelt_motatt is False):
            gjesteliste[motatt_rom - 1] = gjesteliste[motatt_rom - 1] + 1 ## Legger til gjest
            gammelt_motatt = True
    else:
        gammelt_motatt = False
    ## Sende gjesteliste til CoT
    if (sum(gjesteliste)!=(sum_gjesteliste_gammel)):
        for i in range(5):
            verdi = gjesteliste[i]
            send_cot(rom_key_liste[i], verdi, token)
            sum_gjesteliste_gammel = sum(gjesteliste)

    ####### REGISTRERING AV GJESTER #######
    time_now = time()
    resultat = firebase.get('/Gjester', None)
    for i in resultat_liste:                        ## Liste over navn på gjester registrert på Firebase
        var = list(resultat[i])
        for gjest in var:
            if gjest not in gjester_liste:
                gjester_liste.append(gjest)
    if(sum_registrerte<5):                          ## Betingelse på at det ikke kan legges til fler en 5 gjester totalt   
        if(len(gjester_liste_old) != len(gjester_liste)):
            now = datetime.datetime.now()
            tid_now_min = int(now.strftime("%M"))   ## Sanntid 24H, minutter
            tid_now_hr = int(now.strftime("%H"))    ## Sanntid 24H, timer
            tid_now_i_minutter = tid_now_hr * 60 + tid_now_min ## Sanntid i minutter
            print("Ny reg")
            for i in gjester_liste:                 ## Løkke som går gjennom navn på gjester i gjestelisten
                if i not in gjester_liste_old:      ## Filtrerer ut de gjestene som allerede har blitt registrert
                    for navn in resultat_liste:     ## Løkke som kjører gjennom navnene på beboere
                        if i in resultat[navn]:     ## Løkke som henter ut data som er lagret på nye gjester i Firebase
                            booking_til = resultat[navn][i]["dro_kl"]
                            drar_hr = int(booking_til[0:2])     ## Når gjesten skulle forlate kollektivet 24H, timer
                            drar_min = int(booking_til[3:5])    ## Når gjesten skulle forlate kollektivet 24H, minutter
                            min_skal_vare = (drar_hr*60+drar_min) - (tid_now_i_minutter)
                            if(navn == "Nina"):
                                if(antall_gjester_Nina<2):      ## Betingelse på mindre enn 2 gjester som er registrert til "Nina"
                                    antall_gjester_Nina = antall_gjester_Nina+1
                                    booking_lengde = min_skal_vare
                            if(navn == "Tor"):
                                if(antall_gjester_Tor<2):       ## Betingelse på mindre enn 2 gjester som er registrert til "Tor"
                                    antall_gjester_Tor = antall_gjester_Tor+1
                                    booking_lengde = min_skal_vare
                            if(navn == "Maja"):
                                if(antall_gjester_Maja<2):      ## Betingelse på mindre enn 2 gjester som er registrert til "Maja"
                                    antall_gjester_Maja = antall_gjester_Maja+1
                                    booking_lengde = min_skal_vare
                            if(navn == "Hanne"):
                                if(antall_gjester_Hanne<2):     ## Betingelse på mindre enn 2 gjester som er registrert til "Hanne"
                                    antall_gjester_Hanne = antall_gjester_Hanne+1
                                    booking_lengde = min_skal_vare
                            if(navn == "Hanna"):
                                if(antall_gjester_Hanna<2):     ## Betingelse på mindre enn 2 gjester som er registrert til "Hanna"
                                    antall_gjester_Hanna = antall_gjester_Hanna+1
                                    booking_lengde = min_skal_vare
                            print("Loop")
                            gjester_liste_old = gjester_liste.copy()
    ## Fjerne registreringer etter tid
    ##Nina
    if(antall_gjester_Nina != antall_gjester_Nina_old):
        if(timer_gjester_Nina == 0):                ## Timer 1
            start_time_gjester_Nina1 = time()
            timer_gjester_Nina1_aktiv = True
            hvor_lenge_gjester_Nina1 = booking_lengde
            antall_gjester_Nina_old = antall_gjester_Nina
            timer_Nina = 1                          ## Bruk timer 2 neste
        elif(timer_gjester_Nina == 1):              ## Timer 2
            start_time_gjester_Nina2 = time()
            timer_gjester_Nina2_aktiv = True
            hvor_lenge_gjester_Nina2 = booking_lengde
            antall_gjester_Nina_old = antall_gjester_Nina
    else:
        if(timer_gjester_Nina1_aktiv):              ## Timer 1 er aktiv
            time_surpassed_gjester_Nina1 = time_now - start_time_gjester_Nina1
            if((time_surpassed_gjester_Nina1/60) > hvor_lenge_gjester_Nina1):   ## tid gått > booking tid satt
                antall_gjester_Nina = antall_gjester_Nina-1
                antall_gjester_Nina = antall_gjester_Nina
                timer_gjester_Nina = 0              ## Bruk timer 1 neste
                timer_gjester_Nina1_aktiv = False
        if(timer_gjester_Nina2_aktiv):              ## Timer 2 er aktiv
            time_surpassed_gjester_Nina2 = time_now - start_time_gjester_Nina2
            if((time_surpassed_gjester_Nina2/60) > hvor_lenge_gjester_Nina2):   ## tid gått > booking tid satt
                antall_gjester_Nina = antall_gjester_Nina-1
                antall_gjester_Nina_old = antall_gjester_Nina
                timer_gjester_Nina = 1              ## Bruk timer 2 neste
                timer_gjester_Nina1 = False
    ##Tor
    if(antall_gjester_Tor != antall_gjester_Tor_old):
        if(timer_gjester_Tor == 0):                 ## Timer 1
            start_time_gjester_Tor1 = time()
            timer_gjester_Tor1_aktiv = True
            hvor_lenge_gjester_Tor1 = booking_lengde
            antall_gjester_Tor_old = antall_gjester_Tor
            timer_Tor = 1                           ## Bruk timer 2 neste
        elif(timer_gjester_Tor == 1):               ## Timer 2
            start_time_gjester_Tor2 = time()
            timer_gjester_Tor2_aktiv = True
            hvor_lenge_gjester_Tor2 = booking_lengde
            antall_gjester_Tor_old = antall_gjester_Tor
    else:
        if(timer_gjester_Tor1_aktiv):               ## Timer 1 er aktiv
            time_surpassed_gjester_Tor1 = time_now - start_time_gjester_Tor1
            if((time_surpassed_gjester_Tor1/60) > hvor_lenge_gjester_Tor1):     ## tid gått > booking tid satt
                antall_gjester_Tor = antall_gjester_Tor-1
                antall_gjester_Tor = antall_gjester_Tor
                timer_gjester_Tor = 0               ## Bruk timer 1 neste
                timer_gjester_Tor1_aktiv = False
        if(timer_gjester_Tor2_aktiv):               ## Timer 2 er aktiv
            time_surpassed_gjester_Tor2 = time_now - start_time_gjester_Tor2
            if((time_surpassed_gjester_Tor2/60) > hvor_lenge_gjester_Tor2):     ## tid gått > booking tid satt
                antall_gjester_Tor = antall_gjester_Tor-1
                antall_gjester_Tor_old = antall_gjester_Tor
                timer_gjester_Tor = 1               ## Bruk timer 2 neste
                timer_gjester_Tor1 = False  
    ##Maja
    if(antall_gjester_Maja != antall_gjester_Maja_old):
        if(timer_gjester_Maja == 0):                ## Timer 1
            start_time_gjester_Maja1 = time()
            timer_gjester_Maja1_aktiv = True
            hvor_lenge_gjester_Maja1 = booking_lengde
            antall_gjester_Maja_old = antall_gjester_Maja
            timer_Maja = 1                          ## Bruk timer 2 neste
        elif(timer_gjester_Maja == 1):              ## Timer 2
            start_time_gjester_Maja2 = time()
            timer_gjester_Maja2_aktiv = True
            hvor_lenge_gjester_Maja2 = booking_lengde
            antall_gjester_Maja_old = antall_gjester_Maja
    else:
        if(timer_gjester_Maja1_aktiv):              ## Timer 1 er aktiv
            time_surpassed_gjester_Maja1 = time_now - start_time_gjester_Maja1
            if((time_surpassed_gjester_Maja1/60) > hvor_lenge_gjester_Maja1):   ## tid gått > booking tid satt
                antall_gjester_Maja = antall_gjester_Maja-1
                antall_gjester_Maja = antall_gjester_Maja
                timer_gjester_Maja = 0              ## Bruk timer 1 neste
                timer_gjester_Maja1_aktiv = False
        if(timer_gjester_Maja2_aktiv):              ## Timer 2 er aktiv
            time_surpassed_gjester_Maja2 = time_now - start_time_gjester_Maja2
            if((time_surpassed_gjester_Maja2/60) > hvor_lenge_gjester_Maja2):   ## tid gått > booking tid satt
                antall_gjester_Maja = antall_gjester_Maja-1
                antall_gjester_Maja_old = antall_gjester_Maja
                timer_gjester_Maja = 1              ## Bruk timer 2 neste
                timer_gjester_Maja1 = False
    ##Hanne
    if(antall_gjester_Hanne != antall_gjester_Hanne_old):
        if(timer_gjester_Hanne == 0):               ## Timer 1
            start_time_gjester_Hanne1 = time()
            timer_gjester_Hanne1_aktiv = True
            hvor_lenge_gjester_Hanne1 = booking_lengde
            antall_gjester_Hanne_old = antall_gjester_Hanne
            timer_Hanne = 1                         ## Bruk timer 2 neste
        elif(timer_gjester_Hanne == 1):             ## Timer 2
            start_time_gjester_Hanne2 = time()
            timer_gjester_Hanne2_aktiv = True
            hvor_lenge_gjester_Hanne2 = booking_lengde
            antall_gjester_Hanne_old = antall_gjester_Hanne
    else:
        if(timer_gjester_Hanne1_aktiv):             ## Timer 1 er aktiv
            time_surpassed_gjester_Hanne1 = time_now - start_time_gjester_Hanne1
            if((time_surpassed_gjester_Hanne1/60) > hvor_lenge_gjester_Hanne1):     ## tid gått > booking tid satt
                antall_gjester_Hanne = antall_gjester_Hanne-1
                antall_gjester_Hanne = antall_gjester_Hanne
                timer_gjester_Hanne = 0             ## Bruk timer 1 neste
                timer_gjester_Hanne1_aktiv = False
        if(timer_gjester_Hanne2_aktiv):             ## Timer 2 er aktiv
            time_surpassed_gjester_Hanne2 = time_now - start_time_gjester_Hanne2
            if((time_surpassed_gjester_Hanne2/60) > hvor_lenge_gjester_Hanne2):     ## tid gått > booking tid satt
                antall_gjester_Hanne = antall_gjester_Hanne-1
                antall_gjester_Hanne_old = antall_gjester_Hanne
                timer_gjester_Hanne = 1             ## Bruk timer 2 neste
                timer_gjester_Hanne1 = False
    ##Hanna
    if(antall_gjester_Hanna != antall_gjester_Hanna_old):
        if(timer_gjester_Hanna == 0):               ## Timer 1
            start_time_gjester_Hanna1 = time()
            timer_gjester_Hanna1_aktiv = True
            hvor_lenge_gjester_Hanna1 = booking_lengde
            antall_gjester_Hanna_old = antall_gjester_Hanna
            timer_Hanna = 1                         ## Bruk timer 2 neste
        elif(timer_gjester_Hanna == 1):             ## Timer 2
            start_time_gjester_Hanna2 = time()
            timer_gjester_Hanna2_aktiv = True
            hvor_lenge_gjester_Hanna2 = booking_lengde
            antall_gjester_Hanna_old = antall_gjester_Hanna
    else:
        if(timer_gjester_Hanna1_aktiv):             ## Timer 1 er aktiv
            time_surpassed_gjester_Hanna1 = time_now - start_time_gjester_Hanna1
            if((time_surpassed_gjester_Hanna1/60) > hvor_lenge_gjester_Hanna1):     ## tid gått > booking tid satt
                antall_gjester_Hanna = antall_gjester_Hanna-1
                antall_gjester_Hanna = antall_gjester_Hanna
                timer_gjester_Hanna = 0             ## Bruk timer 1 neste
                timer_gjester_Hanna1_aktiv = False
        if(timer_gjester_Hanna2_aktiv):             ## Timer 2 er aktiv
            time_surpassed_gjester_Hanna2 = time_now - start_time_gjester_Hanna2
            if((time_surpassed_gjester_Hanna2/60) > hvor_lenge_gjester_Hanna2):     ## tid gått > booking tid satt
                antall_gjester_Hanna = antall_gjester_Hanna-1
                antall_gjester_Hanna_old = antall_gjester_Hanna
                timer_gjester_Hanna = 1             ## Bruk timer 2 neste
                timer_gjester_Hanna1 = False
    sum_registrerte = (antall_gjester_Hanna+antall_gjester_Hanne+antall_gjester_Maja+antall_gjester_Nina+antall_gjester_Tor)
    if(sum_registrerte != sum_registrerte_old):     ## Sender oppdaterte verdier på registreringer til CoT
        send_cot("371", antall_gjester_Nina, token)
        send_cot("28285", antall_gjester_Tor, token)
        send_cot("1816", antall_gjester_Maja, token)
        send_cot("6614", antall_gjester_Hanne, token)
        send_cot("16785", antall_gjester_Hanna, token)
        sum_registrerte_old = sum_registrerte
    ####### BOOKING AV FELLESAREALE #######
    booking_id = les_cot(datasett_booking_id)
    booking_lengde = les_cot(datasett_booking_lengde)
    booking_send = les_cot(datasett_booking_send)
    reserverte_liste = [antall_stue,antall_kjokken,antall_bad]
    ## Ny booking
    if((antall_stue <3) and (booking_id == 2)):     ## Om det er færre en 3 bookinger og booking stue er valgt
        if(booking_send == 1): 
            if(not booking_send_old):
                antall_stue = antall_stue+1
                booking_send_old = True
        else:
            booking_send_old = False
    if((antall_bad<1) and (booking_id == 0)):       ## Om det er færre en 1 bookinger og booking stue er valgt
        if(booking_send == 1):
            antall_bad = antall_bad+1
    if((antall_kjokken <2) and (booking_id == 1)):  ## Om det er færre en 2 bookinger og booking stue er valgt
        if(booking_send == 1):
            if(not booking_send_old):
                antall_kjokken = antall_kjokken+1
                booking_send_old = True
        else:
            booking_send_old = False
    ##Fjerne booking (tidsavhengig)
    if(antall_bad != antall_bad_old):               ## Om det har kommet en ny booking på bad
        if(first_syklus_bad):
            start_time_bad = time()
            hvor_lenge_bad = booking_lengde
            first_syklus_bad = False
        else:
            time_surpassed_bad = time_now - start_time_bad
            if((time_surpassed_bad/60) > hvor_lenge_bad):               ## tid gått > booking tid satt
                antall_bad = antall_bad-1
                antall_bad_old = 0
    if(antall_kjokken > 0):                         ## Om det er noen aktive bookinger på kjøkkenet
        if(antall_kjokken != antall_kjokken_old):
            if(timer_kjokken == 0):                 ## Timer 1
                start_time_kjokken1 = time()
                timer_kjokken1_aktiv = True
                hvor_lenge_kjokken1 = booking_lengde
                antall_kjokken_old = antall_kjokken
                timer_kjokken = 1                   ## Bruk timer 2 neste
            elif(timer_kjokken == 1):               ## Timer 2
                start_time_kjokken2 = time()
                timer_kjokken2_aktiv = True
                hvor_lenge_kjokken2 = booking_lengde
                antall_kjokken_old = antall_kjokken
        else:
            if(timer_kjokken1_aktiv):
                time_surpassed_kjokken1 = time_now - start_time_kjokken1
                if((time_surpassed_kjokken1/60) > hvor_lenge_kjokken1): ## tid gått > booking tid satt
                    antall_kjokken = antall_kjokken-1
                    antall_kjokken_old = antall_kjokken
                    timer_kjokken = 0               ## Bruk timer 1 neste
                    timer_kjokken1_aktiv = False
            if(timer_kjokken2_aktiv):
                time_surpassed_kjokken2 = time_now - start_time_kjokken2
                if((time_surpassed_kjokken2/60) > hvor_lenge_kjokken2): ## tid gått > booking tid satt
                    antall_kjokken = antall_kjokken-1
                    antall_kjokken_old = antall_kjokken
                    timer_kjokken = 1               ## Bruk timer 2 neste
                    timer_kjokken1 = False
    if(antall_stue > 0):
        if(antall_stue != antall_stue_old):
            if(timer_stue == 0):                    ## Timer 1
                start_time_stue1 = time()
                timer_stue1_aktiv = True
                hvor_lenge_stue1 = booking_lengde
                antall_stue_old = antall_stue
                if(timer_stue2_aktiv):              ## Om timer 2 er aktiv
                    timer_stue = 2                  ## Bruk timer 3 neste
                else:
                    timer_stue = 1                  ## Bruk timer 2 neste
            elif(timer_stue == 1):                  ## Timer 2
                start_time_stue2 = time()
                timer_stue2_aktiv = True
                hvor_lenge_stue2 = booking_lengde
                antall_stue_old = antall_stue
                if(timer_stue1_aktiv):              ## Om timer 1 er aktiv
                    timer_stue = 2                  ## Bruk timer 3 neste
                else:
                    timer_stue = 0                  ## Bruk timer 1 neste
            elif(timer_stue == 2):                  ## Timer 3
                start_time_stue3 = time()
                timer_stue3_aktiv = True
                hvor_lenge_stue3 = booking_lengde
                antall_stue_old = antall_stue
                if(timer_stue1_aktiv):              ## Om timer 1 er aktiv
                    timer_stue = 1                  ## Bruk timer 2 neste
                else:
                    timer_stue = 0                  ## Bruk timer 3 neste
        else:
            if(timer_stue1_aktiv):
                time_surpassed_stue1 = time_now - start_time_stue1
                if((time_surpassed_stue1/60) > hvor_lenge_stue1):   ## tid gått > booking tid satt
                    antall_stue = antall_stue-1
                    antall_stue_old = antall_stue
                    timer_stue = 0
                    timer_stue1_aktiv = False
            if(timer_stue2_aktiv):
                time_surpassed_stue2 = time_now - start_time_stue2
                if((time_surpassed_stue2/60) > hvor_lenge_stue2):   ## tid gått > booking tid satt
                    antall_stue = antall_stue-1
                    antall_stue_old = antall_stue
                    timer_stue = 1
                    timer_stue2_aktiv = False
            if(timer_stue3_aktiv):
                time_surpassed_stue3 = time_now - start_time_stue3
                if((time_surpassed_stue3/60) > hvor_lenge_stue3): ## tid gått > booking tid satt
                    antall_stue = antall_stue-1
                    antall_stue_old = antall_stue
                    timer_stue = 2
                    timer_stue3_aktiv = False    
    ## Oppdater CoT med verdier på booking
    if (sum(reserverte_liste)!=sum_reserverte_gammel):
        for i in range(3):
            verdi = reserverte_liste[i]
            send_cot(booking_key_liste[i], verdi, token)
            sum_reserverte_gammel = sum(reserverte_liste)
    # Live oppdatering av vær
    weather = Yr(location_name='Norge/Trøndelag/Trondheim/Trondheim')   # lokasjon
    now = weather.now(as_json=True)                 ## Print og vis været "nå"
    now = json.loads(now) 
    temp = now["temperature"]["@value"]             ## Velger de verdiene jeg skal ha
    skydekke = now["symbol"]["@name"]
    for x in skydekke:
        if skydekke == "Partly cloudy":
            print("50")
        elif skydekke == "Fair":
            print("30")
        elif skydekke == "Clear sky":
            print("0") 
        elif skydekke == "Fog":
            print("40")
        elif skydekke == "Cloudy":
            print("80")
        else:
            print("100")
    # Send til CoT
    send_cot(temp_key, temp, token)
    send_cot(skydekke_key, temp, token)
    ## Estimering av strømforbruk
    a = [f(6, "lamper", 10, 7),                     ## Kaller "a" for å kunne finne sum
 
    f(1, "TV", 150, 4),
 
    f(1, "Vaskemaskin", 2200, 4),
 
    f(1, "Komfyr", 1200, 3),
 
    f(1, "Kaffetrakter", 1000, 1),
 
    f(6, "Panelovner", 1000, 7),
 
    f(1, "Varmtvannsbereder", 2500, 10),
 
    f(1, "Varmepumpe", 700, 10),
 
    f(1, "Annet", 100, 4)]
    usage= sum(a)*(0.001)                           ## Gjør om verdien fra Wh til kWh
    Usage_year = (usage*350)
    # Send til CoT
    send_cot(stromforbruk_key, Usage_year, token)