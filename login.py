# Importazione delle classi di Kivy
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from styles import Styles

# Importazione del database manager
# from SQL_database_management import Database
from Firebase_Database_Management import Database
from database_utenti_locale import DatabaseUtentiLocale

"""
> L'interfaccia e la classe devono avere lo stesso nome. Ecco perché l'interfaccia "Login" e la classe "Login" hanno lo stesso nome.
"""

# Implementazione dell'interfaccia "Login"
Builder.load_string("""

# CLASSI COSTRUITE PER IL TESTING
# Alcuni colori utilizzabili: rosso (#e33434), arancione (#e3b134), giallo (#e3da34), verde (#7ae334), blu (#3440e3), viola (#e334c9)
#: import BgBoxLayout custom_widgets
#: import BgAnchorLayout custom_widgets
#: import BgFloatLayout custom_widgets
#: import BgStackLayout custom_widgets
#: import BgGridLayout custom_widgets
                    
# CLASSI CUSTOMIZZATE
#: import VGP_Button custom_widgets
#: import VGP_TextInput custom_widgets
#: import VGP_SignupText custom_widgets
                    
<Login>: 
    # Nome dello screen
    name: "screen_login"
    # BoxLayout - Contenitore di tutti gli elementi
    BoxLayout: 
        # Orientamento
        orientation: "vertical"
        # Padding
        padding: self.width*0.05
        # Logo
        BoxLayout: 
            # Dimensioni
            size_hint: 1, 0.3                    
            # Image - Logo
            Image: 
                # Sorgente immagine 
                source: root.LOGO
                # Dimensione
                size_hint: 0.8, 0.8
                # Posizione
                pos_hint: {"center_x": 0.5, "center_y": 0.3}
        # "Login to your account" + username + password + login
        AnchorLayout: 
            # Dimensioni
            size_hint: 1, 0.4
            # Ancoraggio
            anchor_y: "center"
            # BoxLayout ancorato
            BoxLayout: 
                # Orientamento
                orientation: "vertical"
                # Dimensioni stabilite dai widget contenuti all'interno del BoxLayout
                size_hint_y: None
                height: self.minimum_height
                # padding
                padding: [dp(30), 0, dp(30), 0]
                # Spacing
                spacing: dp(10)
                # Label: "Login to your account"
                Label: 
                    # Testo
                    text: "Esegui l'accesso"
                    # Colore testo
                    color: 0, 0, 0, 1 
                    # Font size
                    font_size: "16sp"  
                    # Dimensione del testo
                    text_size: self.size
                    # Allineamento orizzontale del testo
                    halign: "left"   
                    # Font name
                    font_name: root.font_path 
                    # Dimensioni
                    size_hint_y: None
                    size: self.texture_size
                # TextInput - username
                VGP_TextInput: 
                    # ID
                    id: email
                    # Dimensioni
                    size_hint_y: None
                    height: dp(50)
                    # Multiline
                    multiline: False
                    # Hint text
                    hint_text: "Email"
                # TextInput - password
                VGP_TextInput: 
                    # ID
                    id: password
                    # Dimensioni
                    size_hint_y: None
                    height: dp(50)
                    # Multiline
                    multiline: False
                    # Hint text
                    hint_text: "Password"
                    # Oscuramento della password 
                    password: True
                # Button - Login
                VGP_Button: 
                    # Testo
                    text: "Accedi"
                    # Dimensioni
                    size_hint_y: None
                    height: dp(50)
                    # Login
                    on_press: root.login()
        # "Don't have an account? Signup"
        AnchorLayout: 
            # Dimensioni
            size_hint: 1, 0.3
            # Ancoraggio
            anchor_x: "center"
            anchor_y: "center"
            # BoxLayout contenente i widgets
            BoxLayout: 
                # Dimensioni
                size_hint_x: None
                width: self.minimum_width
                size_hint_y: None
                height: self.minimum_height
                # Spacing
                spacing: dp(4)
                # Label: "Don't have an account?"
                Label:
                    # Testo
                    text: "Non sei ancora iscritto?"
                    # Colore testo
                    color: 0, 0, 0, 1
                    # Dimensioni
                    size_hint_x: None
                    size: self.texture_size # Dimensione lungo x pari alla dimensione del testo
                # Label: "Signup"
                VGP_SignupText: 
                    # Testo
                    text: "Iscriviti"
                    # Dimensioni
                    size_hint_x: None
                    size_hint_y: None
                    size: self.texture_size # Dimensione lungo x pari alla dimensione del testo
                    # Evento - Apertura di Signup
                    on_press: root.switch_to_signup() # L'evento on_press è disponibile per questo elemento grazie al fatto che è stato aggiunta la superclasse "ButtonBehavior" nella definizione della classe "VGP_SignupText"
""")

# Implementazione dell'interfaccia "Login"
class Login(Screen):

    # Font
    font_path = Styles.ROBOTO_BLACK_PATH

    # LOGO
    LOGO = Styles.LOGO

    def switch_to_signup(self): 
        # Transizione verso sinistra
        self.parent.transition.direction = "left"
        # Passaggio allo screen "Signup"
        self.manager.current = "screen_signup" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"

    def login(self): 
        # Fetch dei dati inseriti dall'utente
        email = self.ids.email.text
        password = self.ids.password.text
        # Cancellazione del testo scritto dall'utente
        self.ids.email.text = ""
        self.ids.password.text = ""
        # Verifica se l'utente è valido (email e password corrispondono a quelli di un utente)
        if (Database.is_userValid(email, password)):
            # Transizione verso sinistra
            self.parent.transition.direction = "left"
            # Passaggio allo screen "Home"
            self.manager.current = "screen_home" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"
            # Salvataggio delle credenziali in locale
            DatabaseUtentiLocale.salva_email(email)
            DatabaseUtentiLocale.salva_password(password)
        else: 
            pass