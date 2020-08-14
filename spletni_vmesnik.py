import bottle
import os
from model import Igra

MAPA = os.path.dirname(os.path.relpath(__file__))
ZACETNA_STRAN = os.path.join(MAPA, 'views/zacetna_stran.html')
DODAJ_IGRALCE = os.path.join(MAPA, 'views/dodaj_igralce.html')
USPESNO_DODANA_IGRALCA = os.path.join(MAPA, 'views/uspesno_dodana_igralca.html')
DESKA = os.path.join(MAPA, 'views/deska.html')
DESKA_IGRAJ_BESEDO = os.path.join(MAPA, 'views/deska_igraj_besedo.html')
NAPAKA = os.path.join(MAPA, 'views/napaka.html')
KONEC = os.path.join(MAPA, 'views/konec.html')

stevilo_igralcev = 0
igra = Igra()

def naredi_tabelo_deske(igra):
    seznam_deske = igra.deska.deska 
    tabela = [[0 for k in range(15)] for l in range(15)]

    for polje in seznam_deske:
        (vr, st) = polje
        crka = seznam_deske[polje][0]
        vrednost = seznam_deske[polje][1]
        tabela[vr][st] = (crka, vrednost, polje)
        if crka == '':
            tabela[vr][st] = ('_+_', vrednost, polje)
        else:
            tabela[vr][st] = ('_' + crka + '_', vrednost, polje)  
    
    sredinska_crka = tabela[7][7][0]
    tabela[7][7] = (sredinska_crka, 'sredina', (7, 7))

    return tabela



@bottle.get('/')
def zacetna_stran():
    return bottle.template(ZACETNA_STRAN)

@bottle.get("/dodaj_igralce/")
def dodaj_igralce():
    return bottle.template(DODAJ_IGRALCE)

@bottle.get('/uspesno_dodana_igralca/')
def dodana_igralca():
    prvi_igralec = bottle.request.query.getunicode('ime_prvega')
    drugi_igralec = bottle.request.query.getunicode('ime_drugega')
    igralca = [prvi_igralec, drugi_igralec]
    igra.dodaj_igralce(igralca)
    return bottle.template(USPESNO_DODANA_IGRALCA, igrata=igralca)

@bottle.get('/deska/')
def deska():
    igralca = igra.igralci
    igrajoci = igra.igralci[igra.na_potezi]
    ne_igrajoci = igra.igralci[(igra.na_potezi + 1) % 2]

    tabela_deske = naredi_tabelo_deske(igra)
    na_potezi = igrajoci.ime
    ni_na_potezi = ne_igrajoci.ime
    stojalo_igralca = igrajoci.stojalo.stojalo
    tocke_igra = igrajoci.tocke
    tocke_ne_igra = ne_igrajoci.tocke
    return bottle.template(DESKA, nasa_deska=tabela_deske, na_potezi=na_potezi, stojalo=stojalo_igralca, tocke_igra=tocke_igra, ni_na_potezi=ni_na_potezi, tocke_ne_igra=tocke_ne_igra)

@bottle.post('/deska_zamenjaj_crko/')
def zamenjaj_crko():
    crka_za_zamenjat = bottle.request.forms.getunicode('zamenjana_crka')
    igra.zamenjaj(igra.igralci[igra.na_potezi], crka_za_zamenjat)

    if igra.konec_igre():
        bottle.redirect('/konec/')
    else:
        bottle.redirect('/deska/')

@bottle.get('/deska_igraj_besedo/')
def katero_besedo_bos_igral():
    igralca = igra.igralci
    igrajoci = igra.igralci[igra.na_potezi]
    ne_igrajoci = igra.igralci[(igra.na_potezi + 1) % 2]

    tabela_deske = naredi_tabelo_deske(igra)
    na_potezi = igrajoci.ime
    ni_na_potezi = ne_igrajoci.ime
    stojalo_igralca = igrajoci.stojalo.stojalo
    tocke_igra = igrajoci.tocke
    tocke_ne_igra = ne_igrajoci.tocke
    return bottle.template(DESKA_IGRAJ_BESEDO, nasa_deska=tabela_deske, na_potezi=na_potezi, stojalo=stojalo_igralca, tocke_igra=tocke_igra, ni_na_potezi=ni_na_potezi, tocke_ne_igra=tocke_ne_igra)

@bottle.post('/postavi_besedo/')
def igraj_besedo():
    besedilo = bottle.request.forms.getunicode('besedilo')
    smer = bottle.request.forms.getunicode('smer_besede')
    zacetek_niz = bottle.request.forms.getunicode('polje')
    zacetek_tuple = (int(zacetek_niz.replace(' ', '')[1]), int(zacetek_niz.replace(' ', '')[3]))
    igralec = igra.igralci[igra.na_potezi]
    
    try:
        igra.igraj_besedo(besedilo, igralec, zacetek_tuple, smer)
        bottle.redirect('/deska/')
    except ValueError:
        return bottle.template(NAPAKA, napaka='Neveljavna beseda!')

@bottle.get('/konec/')
def konec_igre():
    (zmagovalci, rezultat) = igra.kdo_je_zmagovalec()
    return bottle.template(KONEC, zmagovalci=zmagovalci, rezultat=rezultat)



bottle.run(debug=True, reloader=True)