import time
from tkinter import Tk, Label, Button

class Horloge:
    def __init__(self, heure_tuple):
        # Initialisation de l'attribut d'instance 'heure' avec le tuple donné
        self.heure = heure_tuple

    def afficher_heure(self):
        # Extraction des heures, minutes et secondes du tuple 'self.heure'
        h, m, s = self.heure
        # Affichage de l'heure sous la forme "hh:mm:ss" en utilisant une f-string
        print(f"{h:02d}:{m:02d}:{s:02d}")

    def regler_heure(self, heure_tuple):
        # Mise à jour de l'attribut d'instance 'heure' avec le tuple donné
        self.heure = heure_tuple
        # Affichage de l'heure mise à jour
        self.afficher_heure()

    def regler_alarme(self, alarme_tuple):
        while True:
            # Récupération de l'heure actuelle à partir du module 'time'
            h, m, s = time.localtime()[3:6]
            # Mise à jour de l'attribut d'instance 'heure' avec l'heure actuelle
            self.heure = (h, m, s)
            # Vérification si l'heure actuelle correspond à l'heure de l'alarme
            if self.heure == alarme_tuple:
                # Affichage d'un message lorsque l'alarme se déclenche
                print("L'alarme se déclenche !")
                break
            # Affichage de l'heure actuelle
            self.afficher_heure()
            # Pause d'une seconde avant de répéter la boucle
            time.sleep(1)

def heure_locale_tuple():
    # Récupération de l'heure locale en utilisant 'time.localtime()'
    h, m, s = time.localtime()[3:6]
    # Retourne l'heure locale sous la forme d'un tuple
    return (h, m, s)

if __name__ == "__main__":
    # Récupération du tuple de l'heure locale
    heure_locale = heure_locale_tuple()

    # Création d'une instance de la classe 'Horloge' avec l'heure locale
    horloge = Horloge(heure_locale)
    horloge.regler_alarme(horloge)