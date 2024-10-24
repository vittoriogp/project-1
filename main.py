# Python version: 3.10.X
# pip install kivy==2.1.0

# Importazione delle classi di Kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from styles import Styles

# Importazione delle classi/interfacce implementate all'interno di altri files
from login import Login
from signup import Signup
from home import Home
from add_word import Add_word
from lista_vocaboli import Lista_Vocaboli

# Importazione del database_management
# from SQL_database_management import Database
from Firebase_Database_Management import Database
from database_utenti_locale import DatabaseUtentiLocale

"""
> L'interfaccia principale e la classe devono avere lo stesso nome. Ecco perché l'interfaccia "Interfaccia_ScreenManager" e la classe "Interfaccia_ScreenManager" hanno lo stesso nome.
"""

# Implementazione dell'interfaccia "Login"
Builder.load_string("""
<Interfaccia_ScreenManager>: 
    # Implementazione di un rettangolo bianco come sfondo dell'applicazione.
    canvas.before: 
        Color: 
            rgba: 1, 1, 1, 1
        Rectangle: 
            # La posizione del rettangolo è pari a quella del layout padre
            pos: self.pos
            # Le dimensioni del rettangolo sono pari alle dimensioni del layout padre
            size: self.size
""")

# Dimensione della finestra corrispondente all'applicazione (Da cancellare per la produzione)
Window.size = (Styles.FINESTRA_LARGHEZZA, Styles.FINESTRA_ALTEZZA)

# Implementazione dello screen manager principale
class Interfaccia_ScreenManager(ScreenManager): 
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)

        # # # Cancellazione di tutto il database (DA INSERIRE A MANO)
        # Database.delete_all_users()
        
        # Aggiunta dell'interfaccia "Login" implementata all'interno del file "login.py"
        email, password = DatabaseUtentiLocale.get_credentials()
        if (email is None) or (password is None) or (Database.is_userValid(email, password) == False):
            login = Login()
            self.add_widget(login)

            # Aggiunta dell'interfaccia "Signup" implementata all'interno del file "signup.py"
            signup = Signup()
            self.add_widget(signup)
            
        # Aggiunta dell'interfaccia "Home" implementata all'interno del file "home.py"
        home = Home() 
        self.add_widget(home)

        # Aggiunta dell'interfaccia "Add_word" implementata all'interno del file "add_word.py"
        add_word = Add_word()
        self.add_widget(add_word)
        
        # Aggiunta dell'interfaccia "Lista_Vocaboli" implementata all'interno del file "lista_vocaboli.py"
        lista_vocaboli = Lista_Vocaboli()
        self.add_widget(lista_vocaboli)

# Implementazione dell'applicazione principale
class Applicazione(App): 
    def build(self):
        self.title = "Flip and Learn"
        return Interfaccia_ScreenManager()

# Lancio dell'applicazione principale
Applicazione().run()