# Importazione delle classi di Kivy
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from styles import Styles

# Importazione
# from SQL_database_management import Database
from Firebase_Database_Management import Database

"""
> L'interfaccia e la classe devono avere lo stesso nome. Ecco perché l'interfaccia "Signup" e la classe "Signup" hanno lo stesso nome.
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
                    
<Signup>: 
    # Nome dello screen
    name: "screen_signup"

    # Contenitore complessivo
    BoxLayout:  
        # Orientamento
        orientation: "vertical"
        
        # Header
        BoxLayout: 
            # Dimensione
            size_hint_y: 0.1
        
        # Corpo centrale
        AnchorLayout: 
            # Dimensione verticale
            size_hint_y: 0.8
            # Ancoraggio
            anchor_y: "center"
            # Padding
            padding: [dp(51), 0, dp(51), 0]
            # Widget disposti verticalmente    
            BoxLayout: 
                # Orientamento
                orientation: "vertical" 
                # Spacing tra i widget
                spacing: dp(10)
                # Dimensione (minima da accogliere i widget)
                size_hint_y: None
                height: self.minimum_height
                # Label - Create your account
                Label: 
                    # Testo
                    text: "Crea il tuo account"
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
                # Text input - Email
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
                # Text input - Password
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
                    # Oscura la password
                    password: True
                # Text input - Confirm password
                VGP_TextInput: 
                    # ID
                    id: confirm_password
                    # Dimensioni
                    size_hint_y: None
                    height: dp(50)
                    # Multiline
                    multiline: False
                    # Hint text
                    hint_text: "Conferma password"
                    # Oscura la password
                    password: True
                # Button - Signup
                VGP_Button: 
                    # Testo
                    text: "Iscriviti"
                    # Dimensioni
                    size_hint_y: None
                    height: dp(50)
                    on_press: root.create_new_user()

                # Button - Annulla
                VGP_Button: 
                    # Testo
                    text: "Annulla"
                    # Dimensioni
                    size_hint_y: None
                    height: dp(50)
                    on_press: root.switch_to_login()
                     
        # Footer senza immagine
        BoxLayout: 
            # Dimensione verticale
            size_hint_y: 0.1 
                    
""")

# Implementazione dell'interfaccia "Signup"
class Signup(Screen): 

    # Font path 
    font_path = Styles.ROBOTO_BLACK_PATH
    
    def create_new_user(self):
        # Fetch dei dati inseriti dall'utente
        email = self.ids.email.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text
        # Cancellazione del testo scritto dall'utente
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.confirm_password.text = ""
        # Controllo che l'utente abbia inserito una email, una password e un confirm password
        if (email and password and confirm_password): 
            # Controllo che password e confirm_password siano uguali
            if(password == confirm_password): 
                # Controllo che l'email non sia già stata utilizzata
                if (Database.is_emailValid(email) == True): 
                    # Creazione di un nuovo utente
                    Database.create_new_user(email, password)
                    # Ritorno allo Screen "Login"
                    self.manager.current = "screen_login" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"
                else: 
                    pass
            else: 
                pass
    def switch_to_login(self): 
        # Transizione verso sinistra
        self.parent.transition.direction = "right"
        # Ritorno allo screen "Login"
        self.manager.current = "screen_login" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"
