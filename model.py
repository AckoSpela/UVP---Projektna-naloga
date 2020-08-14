import random
import os



MAPA = os.path.dirname(os.path.abspath(__file__))
POT_DO_DATOTEKE_Z_BESEDAMI = os.path.join(MAPA, 'besede.txt')

with open(POT_DO_DATOTEKE_Z_BESEDAMI, "r", encoding = "utf-8") as datoteka_z_besedami:
    bazen_besed = [vrstica.strip().upper() for vrstica in datoteka_z_besedami]



class Deska:
    def __init__(self):
        # self.deska = [[(i, j) for j in range(15)] for i in range(15)]

        self.sredina = (7, 7)

        #Posebna polja:
        self.trojni_pomen_besede = ((0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14))
        self.dvojni_pomen_besede = ((1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), (12, 12), (13, 13),(13, 1), (12, 2), (11, 3), (10, 4), (4, 10), (3, 11), (2, 12), (1, 13))
        self.trojni_pomen_crke = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
        self.dvojni_pomen_crke = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))

        self.deska = self.naredi_desko()


    def naredi_desko(self):
        deska = {}
        for i in range(15):
            vrstica_i = {(i, j) : ("", None) for j in range(15)}
            deska.update(vrstica_i)
        #dodajmo še posebna polja:
        for posebno in self.trojni_pomen_besede:
            deska[posebno] = ("", "TPB")
        for posebno in self.dvojni_pomen_besede:
            deska[posebno] = ("", "DPB")
        for posebno in self.trojni_pomen_crke:
            deska[posebno] = ("", "TPČ")
        for posebno in self.dvojni_pomen_crke:
            deska[posebno] = ("", "DPČ")
        return deska




#VREDNOSTI IN ŠTEVILA ČRK (vrednost, število)
vrednosti_in_st_crk = {
    "A" : (1, 10),
    "B" : (4, 2),
    "C" : (8, 1),
    "Č" : (5, 1),
    "D" : (2, 4),
    "E" : (1, 11),
    "F" : (10, 1),
    "G" : (4, 2),
    "H" : (5, 1),
    "I" : (1, 9),
    "J" : (1, 4),
    "K" : (3, 3),
    "L" : (1, 4),
    "M" : (3, 2),
    "N" : (1, 7),
    "O" : (1, 8),
    "P" : (3, 2),
    "R" : (1, 6),
    "S" : (1, 6),
    "Š" : (6, 1),
    "T" : (1, 4),
    "U" : (3, 2),
    "V" : (2, 4),
    "Z" : (4, 2),
    "Ž" : (10, 1)
}


class VrecaPloscic:

    def __init__(self, ploscice=[]):
        self.ploscice = ploscice
        self.napolni_vreco()

    def napolni_vreco(self):
        for crka in vrednosti_in_st_crk:
            #vrednost_crke = vrednosti_in_st_crk[crka][0]
            st_crk = vrednosti_in_st_crk[crka][1]
            for i in range(st_crk):
                #self.ploscice.append((crka, vrednost_crke))
                self.ploscice.append(crka)

    def vleci_crko(self):
        self.ploscice
        st_ploscic_v_vreci = len(self.ploscice)
        if st_ploscic_v_vreci <= 0:
            return None
        else:
           izbrana_ploscica = random.choice(self.ploscice)
           self.ploscice.remove(izbrana_ploscica)
           return izbrana_ploscica
    
    def vleci_iz_vrece(self, stevilo):
        if stevilo <= 0 :
            return []
        elif stevilo > len(self.ploscice):
            izvlecene_crke = self.ploscice
            self.ploscice = []
            return izvlecene_crke
        else:
            izvlecene_crke = []
            for i in range(stevilo):
                izvlecene_crke.append(self.vleci_crko())
            return izvlecene_crke
            

class Beseda:

    def __init__(self, beseda, zacetek, smer, igralec, deska):
        self.beseda = beseda.upper()
        self.deska = deska
        self.igralec = igralec
        self.zacetek = zacetek
        self.smer = smer.upper()
        # self.je_veljavna()
    
    def je_v_bazenu_besed(self):
        if self.beseda not in bazen_besed:
            raise ValueError(f"Beseda {self} ni v Franu!")
        else:
            return True
    
    def lahko_damo_na_desko(self):
        (z_vrstica, z_stolpec) = self.zacetek
        dolzina_besede = len(self.beseda)
        je_ok = False

        if (z_vrstica in range(15)) and (z_stolpec in range(15)):
            if self.smer == "DESNO":
                if (z_stolpec + dolzina_besede - 1) in range(15):
                    je_ok = True
            elif self.smer == "DOL":
                if (z_vrstica + dolzina_besede - 1) in range(15):
                    je_ok = True

        if je_ok == True:
            return True
        else:
            raise ValueError(f"Beseda {self} ne gre na desko!")
        
   

    def polozi_besedo(self):
        if (not self.je_v_bazenu_besed) or (not self.lahko_damo_na_desko):
            raise ValueError(f"Beseda {self} ni veljavna.")
        
        else:
            dolzina = len(self.beseda)
            posebna_polja = []
            (z_vr, z_st) = self.zacetek
            

            se_ni_na_deski = False
            se_stika_vsaj_v_eni = False

            if self.smer == "DESNO":
                for i in range(dolzina):
                    (crka, vrednost) = self.deska.deska[(z_vr, z_st + i)]

                    if (z_vr, z_st + i) == self.deska.sredina:
                        se_stika_vsaj_v_eni = True

                    if crka == '':
                        se_ni_na_deski = True
                        self.deska.deska[(z_vr, z_st + i)] = (self.beseda[i], vrednost)
                    elif crka == self.beseda[i]:
                        se_stika_vsaj_v_eni = True
                    else:
                        raise ValueError(f"Napačno postavljenja beseda f{self}.")
                    
                    if vrednost != None:
                        posebna_polja.append(((z_vr, z_st + i), vrednost, self.beseda[i]))
            
            if self.smer == "DOL":
                for i in range(dolzina):
                    (crka, vrednost) = self.deska.deska[(z_vr + i, z_st)]

                    if (z_vr + i, z_st) == self.deska.sredina:
                        se_stika_vsaj_v_eni = True

                    if crka == '':
                        se_ni_na_deski = True
                        self.deska.deska[(z_vr + i, z_st)] = (self.beseda[i], vrednost)
                    elif crka == self.beseda[i]:
                        se_stika_vsaj_v_eni = True
                    else:
                        raise ValueError(f"Napačno postavljenja beseda f{self}.")
                    
                    if vrednost != None:
                        posebna_polja.append(((z_vr + i, z_st), vrednost, self.beseda[i]))
            
            else:
                pass

        if se_stika_vsaj_v_eni and se_ni_na_deski:
            return posebna_polja
        else:
            raise ValueError(f"Napačno postavljenja beseda f{self}.")


    def izracunaj_vrednost_besede(self, posebna_polja):
        beseda = self.beseda
        vrednost = 0
        kratnost = 1

        #Izracunamo vrednost same besede
        for crka in beseda:
            vrednost += vrednosti_in_st_crk[crka][0]

        for posebna_vrednost in posebna_polja:
            posebna = posebna_vrednost[1]
            p_crka = posebna_vrednost[2]

            if posebna == 'TPB':
                kratnost *= 3
            if posebna == 'DPB':
                kratnost *= 2
            if posebna == 'TPČ':
                vrednost += (2 * vrednosti_in_st_crk[p_crka][0])
            if posebna == 'DPČ':
                vrednost += vrednosti_in_st_crk[p_crka][0]

        return vrednost * kratnost
                





class Stojalo:

    def __init__(self, vreca):
        self.vreca = vreca
        self.stojalo = []

        self.napolni_stojalo()

    def napolni_stojalo(self):
        koliko_jih_rabimo = 7 - len(self.stojalo)
        self.stojalo += self.vreca.vleci_iz_vrece(koliko_jih_rabimo)
    
    def vzemi_s_stojala(self, ploscica):
        if ploscica in self.stojalo:
            self.stojalo.remove(ploscica)
            return ploscica

    def zamenjaj_ploscico(self, ploscica):
        vrnjena = self.vzemi_s_stojala(ploscica)
        self.vreca.ploscice.append(vrnjena)
        self.napolni_stojalo()



class Igralec:

    def __init__(self, ime, vreca, po_vrsti):
        self.ime = ime
        self.vreca = vreca
        self.tocke = 0
        self.stojalo = Stojalo(vreca)
        self.po_vrsti = po_vrsti
    
    def dodaj_tocke(self, stevilo):
        self.tocke += stevilo


class Igra:
    
    def __init__(self):
        self.stevilo_igralcev = 2
        self.vreca = VrecaPloscic()
        self.deska = Deska()
        self.igralci = []
        self.stevilo_zaporedno_preskocenih = 0
        self.na_potezi = 0
        self.prva_beseda_ze_igrana = False

    def dodaj_igralca(self, igralec):
        self.igralci.append(igralec)

    def dodaj_igralce(self, zelijo_igrat):
        if self.stevilo_igralcev == len(zelijo_igrat):
            i = 0
            for ime in zelijo_igrat:
                igralec = Igralec(ime, self.vreca, i)
                self.dodaj_igralca(igralec)
                i += 1
        else:
            raise ValueError("Napačno število igralcev!")
        return self


    def igraj_besedo(self, besedilo, igralec, zacetek, smer):
        
        beseda = Beseda(besedilo.upper(), zacetek, smer.upper(), igralec, self.deska)
        indeks_crke = 0
        (z_vr, z_st) = beseda.zacetek 

        for crka in beseda.beseda:
            if beseda.smer == 'DESNO':
                if crka in beseda.igralec.stojalo.stojalo:
                    beseda.igralec.stojalo.stojalo.remove(crka)
                    indeks_crke += 1
                elif crka == self.deska.deska[(z_vr, z_st + indeks_crke)][0]:
                    indeks_crke +=1
                else:
                    raise ValueError(f"Igralec {beseda.igralec} stojalu nima črke {crka}.")

            if beseda.smer == 'DOL':
                if crka in beseda.igralec.stojalo.stojalo:
                    beseda.igralec.stojalo.stojalo.remove(crka)
                    indeks_crke += 1
                elif crka == self.deska.deska[(z_vr + indeks_crke, z_st)][0]:
                    indeks_crke +=1
                else:
                    raise ValueError(f"Igralec {beseda.igralec} stojalu nima črke {crka}.")
        
        posebne_vrednosti = beseda.polozi_besedo()
        vrednost = beseda.izracunaj_vrednost_besede(posebne_vrednosti)
        
        beseda.igralec.stojalo.napolni_stojalo()

        beseda.igralec.tocke += vrednost
        self.stevilo_zaporedno_preskocenih = 0
        self.na_potezi +=1
        self.na_potezi %= 2
        self.prva_beseda_ze_igrana = True

    def zamenjaj(self, igralec, crka):
        igralec.stojalo.zamenjaj_ploscico(crka)
        self.stevilo_zaporedno_preskocenih += 1
        self.na_potezi +=1
        self.na_potezi %= 2

    def konec_igre(self):
        stevilo_crk_v_vreci = len(self.vreca.ploscice)
        vreca_je_prazna = (stevilo_crk_v_vreci <= 0)
        return (self.stevilo_zaporedno_preskocenih >= 3) or vreca_je_prazna

    
    #Vprasamo, ce bo igral besedo al bo menjal črko.

    def kdo_je_zmagovalec(self):
        koncni_rezultat = []
        for igralec in self.igralci:
            koncni_rezultat.append((igralec.ime, igralec.tocke))
            koncni_rezultat.sort(key=lambda tup: tup[1], reverse=True)
        zmagovalci = []
        top_tocke = koncni_rezultat[0][1]
        for rezultat in koncni_rezultat:
            if rezultat[1] == top_tocke:
                zmagovalci.append(rezultat[0])
        return zmagovalci, koncni_rezultat


def nova_igra(seznam_igralcev):
    igra = Igra().dodaj_igralce(seznam_igralcev)
    return igra



[('Jana', 2), ('Špela', 5), ('Maša', 3), ('Miran', 1)]       
        

igra = nova_igra(['Špela', 'Tonček'])
Špela = igra.igralci[0]
Tonček = igra.igralci[1]

Špela.stojalo.stojalo = ['B', 'E', 'S', 'E', 'D', 'A', 'Ž']
Tonček.stojalo.stojalo = ['E', 'M', 'B', 'R', 'I', 'O', 'B']

igra.igraj_besedo("beseda", Špela, (7, 7), "desno")
igra.igraj_besedo("embrio", Tonček, (7, 8), "DOL")

Špela.stojalo.stojalo = ['B', 'E', 'S', 'E', 'D', 'A', 'Ž']
igra.igraj_besedo("bes", Špela, (5, 9),'dol')
igra.zamenjaj(Tonček, 'B')
igra.zamenjaj(Špela, 'E')
igra.zamenjaj(Špela, 'D')
print(igra.kdo_je_zmagovalec())
print(igra.igralci[igra.na_potezi].ime)
print(igra.igralci[(igra.na_potezi + 1) % 2].ime)



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


def samo_crke(tabela):
    for i in range(15):
        for j in range(15):
            elt = tabela[i][j]
            tabela[i][j] = elt[0]
    return tabela

print(naredi_tabelo_deske(igra)[7][7])

        
