# Importe les bibliothèques nécessaires
import time
from tkinter import Tk, Label, Button, Entry, messagebox, font

# Classe Horloge pour gérer l'affichage et la vérification de l'heure et de l'alarme
class Horloge:
    # Initialise l'objet Horloge avec une heure donnée sous forme de tuple
    def __init__(self, heure_tuple):
        self.heure = heure_tuple

    # Renvoie l'heure sous forme de chaîne formatée hh:mm:ss
    def afficher_heure(self):
        h, m, s = self.heure
        return f"{h:02d}:{m:02d}:{s:02d}"

    # Met à jour l'heure de l'objet Horloge
    def regler_heure(self, heure_tuple):
        self.heure = heure_tuple

    # Vérifie si l'alarme doit se déclencher en comparant l'heure actuelle avec l'alarme définie
    def check_alarme(self, alarme_tuple):
        h, m, s = time.localtime()[3:6]
        self.heure = (h, m, s)
        if self.heure == alarme_tuple:
            return "L'alarme se déclenche !"
        else:
            return None

    def afficher_heure_12h(self):
        h, m, s = self.heure
        am_pm = "AM" if h < 12 else "PM"
        h = h % 12 if h % 12 != 0 else 12
        return f"{h:02d}:{m:02d}:{s:02d} {am_pm}"

# Fonction pour obtenir l'heure locale sous forme de tuple
def heure_locale_tuple():
    h, m, s = time.localtime()[3:6]
    return (h, m, s)

# Classe Application pour construire l'interface graphique et gérer l'interaction utilisateur
class Application(Tk):
    # Initialise l'objet Application, crée les éléments de l'interface graphique et positionne la fenêtre au centre de l'écran
    def __init__(self):
        super().__init__()
        self.paused = False
        self.mode_12h = True  # True pour le mode 12 heures, False pour le mode 24 heures

        # Met à jour l'affichage de la fenêtre pour s'assurer que tous les éléments sont créés et ont la bonne taille
        self.update()

        # Centre la fenêtre sur l'écran
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = (width - self.winfo_reqwidth()) // 2
        y = (height - self.winfo_reqheight()) // 2
        self.geometry(f"+{x}+{y}")

        self.title("Horloge et alarme")

        # Définit une police plus grande et indigo pour les labels et boutons
        big_font = font.Font(size=14)
        indigo_color = "#4B0082"

        self.heure_label = Label(self, text="", font=big_font, fg=indigo_color)
        self.heure_label.pack(pady=10)

        self.alarme_label = Label(self, text="Régler l'alarme (hh:mm) :", font=big_font, fg=indigo_color)
        self.alarme_label.pack()

        self.alarme_entry = Entry(self)
        self.alarme_entry.pack()

        self.alarme_button = Button(self, text="Régler l'alarme", command=self.set_alarm, font=big_font,
                                    fg=indigo_color)
        self.alarme_button.pack(pady=10)

        self.status_label = Label(self, text="", font=big_font, fg=indigo_color)
        self.status_label.pack()

        self.pause_button = Button(self, text="Pause", command=self.pause_clock, font=big_font, fg=indigo_color)
        self.pause_button.pack(pady=10)

        self.mode_button = Button(self, text="Changer de mode", command=self.toggle_time_mode, font=big_font,
                                  fg=indigo_color)
        self.mode_button.pack(pady=10)

        self.heure_label.pack(pady=10, padx=20)  # Ajoute l'option padx

        self.alarme_label.pack(padx=20)  # Ajoute l'option padx

        self.alarme_entry.pack(padx=20)  # Ajoute l'option padx

        self.alarme_button.pack(pady=10, padx=20)  # Ajoute l'option padx

        self.status_label.pack(padx=20)  # Ajoute l'option padx

        self.pause_button.pack(pady=10, padx=20)  # Ajoute l'option padx

        self.mode_button.pack(pady=10, padx=20)  # Ajoute l'option padx

        self.update_clock()

    def pause_clock(self):
        self.paused = not self.paused

    def toggle_time_mode(self):
        self.mode_12h = not self.mode_12h

    # Met à jour l'affichage de l'heure chaque seconde
    def update_clock(self):
        if not self.paused:
            heure_locale = heure_locale_tuple()
            horloge = Horloge(heure_locale)

            if self.mode_12h:
                heure_text = horloge.afficher_heure_12h()
            else:
                heure_text = horloge.afficher_heure()

            self.heure_label.config(text=heure_text)
        self.after(1000, self.update_clock)

    # Récupère l'heure de l'alarme entrée par l'utilisateur et planifie la vérification de l'alarme
    def set_alarm(self):
        alarme_text = self.alarme_entry.get()
        try:
            h, m = map(int, alarme_text.split(':'))
            if not (0 <= h < 24) or not (0 <= m < 60):
                raise ValueError("Heure ou minute invalide.")
        except ValueError as e:
            messagebox.showerror("Erreur", f"Entrée d'alarme invalide : {e}")
            return

        alarme_tuple = (h, m, 0)
        heure_locale = heure_locale_tuple()
        horloge = Horloge(heure_locale)
        self.after(1000, self.check_alarm, horloge, alarme_tuple)

    # Vérifie si l'alarme doit se déclencher et affiche une boîte de message si nécessaire, sinon répète la vérification toutes les secondes
    def check_alarm(self, horloge, alarme_tuple):
        result = horloge.check_alarme(alarme_tuple)
        if result:
            messagebox.showinfo("Alarme", result)
        else:
            self.after(1000, self.check_alarm, horloge, alarme_tuple)

# Code principal : crée une instance de l'objet Application et démarre la boucle principale de l'application
if __name__ == "__main__":
    app = Application()
    app.mainloop()