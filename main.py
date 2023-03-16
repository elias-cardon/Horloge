import time
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox

class Horloge:
    def __init__(self, heure_tuple):
        self.heure = heure_tuple

    def afficher_heure(self):
        h, m, s = self.heure
        return f"{h:02d}:{m:02d}:{s:02d}"

    def regler_heure(self, heure_tuple):
        self.heure = heure_tuple

    def regler_alarme(self, alarme_tuple):
        while True:
            h, m, s = time.localtime()[3:6]
            self.heure = (h, m, s)
            if self.heure == alarme_tuple:
                return "L'alarme se déclenche !"
            time.sleep(1)

def heure_locale_tuple():
    h, m, s = time.localtime()[3:6]
    return (h, m, s)

class Application(Tk):
    def __init__(self):
        super().__init__()

        self.title("Horloge et alarme")
        self.geometry("300x200")

        self.heure_label = Label(self, text="")
        self.heure_label.pack(pady=10)

        self.alarme_label = Label(self, text="Régler l'alarme (hh:mm):")
        self.alarme_label.pack()

        self.alarme_entry = Entry(self)
        self.alarme_entry.pack()

        self.alarme_button = Button(self, text="Régler l'alarme", command=self.set_alarm)
        self.alarme_button.pack(pady=10)

        self.status_label = Label(self, text="")
        self.status_label.pack()

        self.update_clock()

    def update_clock(self):
        heure_locale = heure_locale_tuple()
        horloge = Horloge(heure_locale)
        heure_text = horloge.afficher_heure()
        self.heure_label.config(text=heure_text)
        self.after(1000, self.update_clock)

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

        # Utilisez la méthode after pour appeler la fonction check_alarm
        # sans bloquer l'interface principale
        self.after(1000, self.check_alarm, horloge, alarme_tuple)

    def check_alarm(self, horloge, alarme_tuple):
        result = horloge.regler_alarme(alarme_tuple)
        if result:
            messagebox.showinfo("Alarme", result)
        else:
            self.after(1000, self.check_alarm, horloge, alarme_tuple)

if __name__ == "__main__":
    app = Application()
    app.mainloop()