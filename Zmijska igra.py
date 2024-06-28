import sys
import os
import random
import math
import pygame

pygame.init()
pygame.display.set_caption("Zmijska Igra")
pygame.font.init()
random.seed()

# Globalne konstante
BRZINA = 0.36
VELICINA_ZMIJE = 9
VELICINA_JABUKE = VELICINA_ZMIJE  # Veličina zmije i jabuke će biti ista
RAZMAK = 10  # Razmak između dva piksela
VISINA_EKRANA = 600
SIRINA_EKRANA = 800
FPS = 25
TIPKA = {"GORE": 1, "DOLJE": 2, "LIJEVO": 3, "DESNO": 4}

# Inicijalizacija ekrana
ekran = pygame.display.set_mode((SIRINA_EKRANA, VISINA_EKRANA), pygame.HWSURFACE)
pygame.display.set_caption("Zmijska Igra")

# Resursi
font_bodovi = pygame.font.Font(None, 38)
font_broj_bodova = pygame.font.Font(None, 28)
font_kraj_igre = pygame.font.Font(None, 46)
font_igraj_ponovo = font_broj_bodova
poruka_bodovi = font_bodovi.render("Bodovi: ", 1, pygame.Color("green"))
velicina_poruke_bodovi = font_bodovi.size("Bodovi")
boja_pozadine = pygame.Color(0, 0, 0)  # Boja pozadine će biti crna
crna = pygame.Color(0, 0, 0)

# Sat u gornjem lijevom kutu
sat_igre = pygame.time.Clock()

def provjeriSudaranje(posA, velicinaA, posB, velicinaB):
    if (posA.x < posB.x + velicinaB and posA.x + velicinaA > posB.x and posA.y < posB.y + velicinaB and posA.y + velicinaA > posB.y):
        return True
    return False

def provjeriGranice(zmija):
    if (zmija.x > SIRINA_EKRANA):
        zmija.x = VELICINA_ZMIJE
    if (zmija.x < 0):
        zmija.x = SIRINA_EKRANA - VELICINA_ZMIJE
    if (zmija.y > VISINA_EKRANA):
        zmija.y = VELICINA_ZMIJE
    if (zmija.y < 0):
        zmija.y = VISINA_EKRANA - VELICINA_ZMIJE

class Jabuka:
    def __init__(self, x, y, stanje):
        self.x = x
        self.y = y
        self.stanje = stanje
        self.boja = pygame.color.Color("orange")  # Boja jabuke

    def nacrtaj(self, ekran):
        pygame.draw.rect(ekran, self.boja, (self.x, self.y, VELICINA_JABUKE, VELICINA_JABUKE), 0)

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.smjer = TIPKA["GORE"]
        self.boja = "bijela"

class Zmija:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.smjer = TIPKA["GORE"]
        self.segmenti = []  # Početni segmenti zmije
        self.segmenti.append(self)
        crnaKutija = Segment(self.x, self.y + RAZMAK)
        crnaKutija.smjer = TIPKA["GORE"]
        crnaKutija.boja = "NULL"
        self.segmenti.append(crnaKutija)

    def pomakni(self):
        zadnji_element = len(self.segmenti) - 1
        while (zadnji_element != 0):
            self.segmenti[zadnji_element].smjer = self.segmenti[zadnji_element - 1].smjer
            self.segmenti[zadnji_element].x = self.segmenti[zadnji_element - 1].x
            self.segmenti[zadnji_element].y = self.segmenti[zadnji_element - 1].y
            zadnji_element -= 1
        if (len(self.segmenti) < 2):
            zadnji_segment = self
        else:
            zadnji_segment = self.segmenti.pop(zadnji_element)
        zadnji_segment.smjer = self.segmenti[0].smjer
        if (self.segmenti[0].smjer == TIPKA["GORE"]):
            zadnji_segment.y = self.segmenti[0].y - (BRZINA * FPS)
        elif (self.segmenti[0].smjer == TIPKA["DOLJE"]):
            zadnji_segment.y = self.segmenti[0].y + (BRZINA * FPS)
        elif (self.segmenti[0].smjer == TIPKA["LIJEVO"]):
            zadnji_segment.x = self.segmenti[0].x - (BRZINA * FPS)
        elif (self.segmenti[0].smjer == TIPKA["DESNO"]):
            zadnji_segment.x = self.segmenti[0].x + (BRZINA * FPS)
        self.segmenti.insert(0, zadnji_segment)

    def uzmiGlavu(self):
        return (self.segmenti[0])

    def raste(self):
        zadnji_element = len(self.segmenti) - 1
        self.segmenti[zadnji_element].smjer = self.segmenti[zadnji_element].smjer
        if (self.segmenti[zadnji_element].smjer == TIPKA["GORE"]):
            novi_segment = Segment(self.segmenti[zadnji_element].x, self.segmenti[zadnji_element].y - VELICINA_ZMIJE)
            crnaKutija = Segment(novi_segment.x, novi_segment.y - RAZMAK)
        elif (self.segmenti[zadnji_element].smjer == TIPKA["DOLJE"]):
            novi_segment = Segment(self.segmenti[zadnji_element].x, self.segmenti[zadnji_element].y + VELICINA_ZMIJE)
            crnaKutija = Segment(novi_segment.x, novi_segment.y + RAZMAK)
        elif (self.segmenti[zadnji_element].smjer == TIPKA["LIJEVO"]):
            novi_segment = Segment(self.segmenti[zadnji_element].x - VELICINA_ZMIJE, self.segmenti[zadnji_element].y)
            crnaKutija = Segment(novi_segment.x - RAZMAK, novi_segment.y)
        elif (self.segmenti[zadnji_element].smjer == TIPKA["DESNO"]):
            novi_segment = Segment(self.segmenti[zadnji_element].x + VELICINA_ZMIJE, self.segmenti[zadnji_element].y)
            crnaKutija = Segment(novi_segment.x + RAZMAK, novi_segment.y)
        crnaKutija.boja = "NULL"
        self.segmenti.append(novi_segment)
        self.segmenti.append(crnaKutija)

    def postaviSmjer(self, smjer):
        if (self.smjer == TIPKA["DESNO"] and smjer == TIPKA["LIJEVO"] or self.smjer == TIPKA["LIJEVO"] and smjer == TIPKA["DESNO"]):
            pass
        elif (self.smjer == TIPKA["GORE"] and smjer == TIPKA["DOLJE"] or self.smjer == TIPKA["GORE"] and smjer == TIPKA["DOLJE"]):
            pass
        else:
            self.smjer = smjer

    def uzmiPravokutnik(self):
        pravokutnik = (self.x, self.y)
        return pravokutnik

    def uzmiX(self):
        return self.x

    def uzmiY(self):
        return self.y

    def postaviX(self, x):
        self.x = x

    def postaviY(self, y):
        self.y = y

    def provjeriSudaranje(self):
        brojac = 1
        while (brojac < len(self.segmenti) - 1):
            if (provjeriSudaranje(self.segmenti[0], VELICINA_ZMIJE, self.segmenti[brojac], VELICINA_ZMIJE) and self.segmenti[brojac].boja != "NULL"):
                return True
            brojac += 1
        return False

    def nacrtaj(self, ekran):
        pygame.draw.rect(ekran, pygame.color.Color("yellow"), (self.segmenti[0].x, self.segmenti[0].y, VELICINA_ZMIJE, VELICINA_ZMIJE), 0)
        brojac = 1
        while (brojac < len(self.segmenti)):
            if (self.segmenti[brojac].boja == "NULL"):
                brojac += 1
                continue
            pygame.draw.rect(ekran, pygame.color.Color("red"), (self.segmenti[brojac].x, self.segmenti[brojac].y, VELICINA_ZMIJE, VELICINA_ZMIJE), 0)
            brojac += 1

def uzmiTipku():
    for dogadaj in pygame.event.get():
        if dogadaj.type == pygame.KEYDOWN:
            if dogadaj.key == pygame.K_UP:
                return TIPKA["GORE"]
            elif dogadaj.key == pygame.K_DOWN:
                return TIPKA["DOLJE"]
            elif dogadaj.key == pygame.K_LEFT:
                return TIPKA["LIJEVO"]
            elif dogadaj.key == pygame.K_RIGHT:
                return TIPKA["DESNO"]
            elif dogadaj.key == pygame.K_ESCAPE:
                return "izlaz"
            elif dogadaj.key == pygame.K_y:
                return "da"
            elif dogadaj.key == pygame.K_n:
                return "ne"
        if dogadaj.type == pygame.QUIT:
            sys.exit(0)

def zavrsiIgru():
    poruka = font_kraj_igre.render("Kraj Igre", 1, pygame.Color("white"))
    poruka_igraj_ponovo = font_igraj_ponovo.render("Igraj ponovo? (Y/N)", 1, pygame.Color("green"))
    ekran.blit(poruka, (320, 240))
    ekran.blit(poruka_igraj_ponovo, (332, 280))

    pygame.display.flip()
    pygame.display.update()

    tipka = uzmiTipku()
    while (tipka != "izlaz"):
        if (tipka == "da"):
            main()
        elif (tipka == "ne"):
            break
        tipka = uzmiTipku()
        sat_igre.tick(FPS)
    sys.exit(0)

def nacrtajBodove(bodovi):
    broj_bodova = font_broj_bodova.render(str(bodovi), 1, pygame.Color("red"))
    ekran.blit(poruka_bodovi, (SIRINA_EKRANA - velicina_poruke_bodovi[0] - 60, 10))
    ekran.blit(broj_bodova, (SIRINA_EKRANA - 45, 14))

def nacrtajVrijemeIgre(vrijemeIgre):
    vrijeme_igre = font_bodovi.render("Vrijeme:", 1, pygame.Color("white"))
    broj_vrijeme_igre = font_broj_bodova.render(str(vrijemeIgre / 1000), 1, pygame.Color("white"))
    ekran.blit(vrijeme_igre, (30, 10))
    ekran.blit(broj_vrijeme_igre, (150, 14))  # Povećan razmak između teksta i broja sekundi

def ponovoPokreniJabuku(jabuke, indeks, sx, sy):
    radius = math.sqrt((SIRINA_EKRANA / 2 * SIRINA_EKRANA / 2 + VISINA_EKRANA / 2 * VISINA_EKRANA / 2)) / 2
    kut = 999
    while (kut > radius):
        kut = random.uniform(0, 800) * math.pi * 2
        x = SIRINA_EKRANA / 2 + radius * math.cos(kut)
        y = VISINA_EKRANA / 2 + radius * math.sin(kut)
        if (x == sx and y == sy):
            continue
    novaJabuka = Jabuka(x, y, 1)
    jabuke[indeks] = novaJabuka

def ponovoPokreniJabuke(jabuke, kolicina, sx, sy):
    brojac = 0
    del jabuke[:]
    radius = math.sqrt((SIRINA_EKRANA / 2 * SIRINA_EKRANA / 2 + VISINA_EKRANA / 2 * VISINA_EKRANA / 2)) / 2
    kut = 999
    while (brojac < kolicina):
        while (kut > radius):
            kut = random.uniform(0, 800) * math.pi * 2
            x = SIRINA_EKRANA / 2 + radius * math.cos(kut)
            y = VISINA_EKRANA / 2 + radius * math.sin(kut)
            if ((x - VELICINA_JABUKE == sx or x + VELICINA_JABUKE == sx) and (y - VELICINA_JABUKE == sy or y + VELICINA_JABUKE == sy)
                    or radius - kut <= 10):
                continue
        jabuke.append(Jabuka(x, y, 1))
        kut = 999
        brojac += 1

def main():
    bodovi = 0

    # Inicijalizacija zmije
    mojaZmija = Zmija(SIRINA_EKRANA / 2, VISINA_EKRANA / 2)
    mojaZmija.postaviSmjer(TIPKA["GORE"])
    mojaZmija.pomakni()
    pocetni_segmenti = 3  # Početno će zmija imati 3 segmenta
    while (pocetni_segmenti > 0):
        mojaZmija.raste()
        mojaZmija.pomakni()
        pocetni_segmenti -= 1

    # Hrana
    max_jabuke = 1  # Početna količina jabuka
    pojedena_jabuka = False  # Jabuka nestaje kada ju zmija pojede
    jabuke = [Jabuka(random.randint(60, SIRINA_EKRANA), random.randint(60, VISINA_EKRANA), 1)]
    ponovoPokreniJabuke(jabuke, max_jabuke, mojaZmija.x, mojaZmija.y)

    pocetnoVrijeme = pygame.time.get_ticks()
    krajIgre = 0

    while (krajIgre != 1):
        sat_igre.tick(FPS)

        # Unos
        pritisakTipke = uzmiTipku()
        if pritisakTipke == "izlaz":
            krajIgre = 1

        # Provjera sudara
        provjeriGranice(mojaZmija)
        if (mojaZmija.provjeriSudaranje() == True):
            zavrsiIgru()

        for mojaJabuka in jabuke:
            if (mojaJabuka.stanje == 1):
                if (provjeriSudaranje(mojaZmija.uzmiGlavu(), VELICINA_ZMIJE, mojaJabuka, VELICINA_JABUKE) == True):
                    mojaZmija.raste()
                    mojaJabuka.stanje = 0
                    bodovi += 10
                    pojedena_jabuka = True

        # Ažuriranje pozicije
        if (pritisakTipke):
            mojaZmija.postaviSmjer(pritisakTipke)
        mojaZmija.pomakni()

        # Ponovno postavljanje jabuke
        if (pojedena_jabuka == True):
            pojedena_jabuka = False
            ponovoPokreniJabuku(jabuke, 0, mojaZmija.uzmiGlavu().x, mojaZmija.uzmiGlavu().y)

        # Crtanje
        ekran.fill(boja_pozadine)
        for mojaJabuka in jabuke:
            if (mojaJabuka.stanje == 1):
                mojaJabuka.nacrtaj(ekran)

        mojaZmija.nacrtaj(ekran)
        nacrtajBodove(bodovi)
        vrijemeIgre = pygame.time.get_ticks() - pocetnoVrijeme
        nacrtajVrijemeIgre(vrijemeIgre)

        pygame.display.flip()
        pygame.display.update()

main()
