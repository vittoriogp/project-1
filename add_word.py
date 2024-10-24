from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from styles import Styles

# Importazione del database_management
# from SQL_database_management import Database
from Firebase_Database_Management import Database

"""
> L'interfaccia e la classe devono avere lo stesso nome. Ecco perché l'interfaccia "Home" e la classe "Home" hanno lo stesso nome.
"""

# Implementazione dell'interfaccia "ADD_WORD"
Builder.load_string("""

# CLASSI COSTRUITE PER IL TESTING
# Nell'utilizzare questi Layouts personalizzati, indicare sempre hex_code (colore di background in formato esadecimale) e alpha (numero compreso tra 0 e 1)
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
            
<ADD_WORD>: 
    # Nome dello screen
    name: "screen_add_word"
    
    # Contenitore complessivo
    BoxLayout: 
        # Orientamento
        orientation: "vertical"
        
        # Header
        BoxLayout: 
            # Colore e trasparenza
            hex_code: "#7ae334"
            alpha: 0.2
            # Dimensione verticale
            size_hint_y: root.ALTEZZA_HEADER
        
        # Corpo centrale
        AnchorLayout: 
            # Colore e trasparenza
            hex_code: "#3440e3"
            alpha: 0.2
            # Dimensione verticale
            size_hint_y: root.ALTEZZA_BODY
            # Ancoraggio
            anchor_y: "center"
            # Padding
            padding: [dp(root.PADDING_BODY), 0, dp(root.PADDING_BODY), 0]
            # Contenitore
            BoxLayout: 
                # Orientamento
                orientation: "vertical"
                # Spacing tra gli oggetti
                spacing: dp(root.SPACING_LABELS_AND_BUTTONS)
                # Dimensione (minima da accogliere i widget)
                size_hint_y: None
                height: self.minimum_height
                # Label - Aggiungi un vocabolo
                Label: 
                    # Testo
                    text: "Aggiungi un vocabolo"
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
                # Text input - Vocabolo in italiano
                VGP_TextInput: 
                    # ID
                    id: ita
                    # Dimensioni
                    size_hint_y: None
                    height: dp(root.ALTEZZA_TEXT_INPUT)
                    # Multiline: False
                    multiline: False
                    # Hint text
                    hint_text: "Italiano"
                # Text input - Vocabolo in inglese
                VGP_TextInput: 
                    # ID
                    id: eng
                    # Dimensioni
                    size_hint_y: None
                    height: dp(root.ALTEZZA_TEXT_INPUT)
                    # Multiline: False
                    multiline: False
                    # Hint text
                    hint_text: "Inglese"

                # Text input - Uso
                VGP_TextInput: 
                    # ID
                    id: uso
                    # Dimensioni
                    size_hint_y: None
                    height: dp(root.ALTEZZA_TEXT_INPUT)
                    # Multiline: False
                    multiline: False
                    # Hint text
                    hint_text: "Uso"

                # Text input - Uso
                VGP_TextInput: 
                    # ID
                    id: esempio
                    # Dimensioni
                    size_hint_y: None
                    height: dp(root.ALTEZZA_TEXT_INPUT)
                    # Multiline: False
                    multiline: False
                    # Hint text
                    hint_text: "Esempio"
                
                # Button - Aggiungi
                VGP_Button: 
                    # Testo
                    text: "Aggiungi"
                    # Dimensioni
                    size_hint_y: None
                    height: dp(root.ALTEZZA_TEXT_INPUT)
                    # Callback function
                    on_release: root.aggiungi_nuovo_utente()
                
                # Button - Annulla
                VGP_Button: 
                    # Testo
                    text: "Annulla"
                    # Dimensioni
                    size_hint_y: None
                    height: dp(root.ALTEZZA_TEXT_INPUT)
                    # Callback function
                    on_release: root.annulla()
        # Header
        BoxLayout: 
            # Colore e trasparenza
            hex_code: "#7ae334"
            alpha: 0.2
            # Dimensione verticale
            size_hint_y: root.ALTEZZA_FOOTER
                    
""")

# Implementazione dell'interfaccia "Signup"
class Add_word(Screen): 
    # Dimensioni
    PADDING_BODY = 51 # Padding laterale dei text labels presenti all'interno del body
    PADDING_RETURN_BUTTON = 15

    SPACING_LABELS_AND_BUTTONS = 10

    ALTEZZA_FOOTER = 0.1
    ALTEZZA_BODY = 1 - 2*ALTEZZA_FOOTER
    ALTEZZA_HEADER = ALTEZZA_FOOTER

    ALTEZZA_TEXT_INPUT = 50

    # FONT
    font_path = Styles.ROBOTO_BLACK_PATH

    # Callback function - Aggiungi
    def aggiungi_nuovo_utente(self): 
        # Fetch dei dati inseriti dall'utente
        ita = self.ids.ita.text 
        eng = self.ids.eng.text
        uso = self.ids.uso.text
        esempio = self.ids.esempio.text
        # Creazione di un nuovo utente
        if ita and eng: 
            Database.aggiungi_vocabolo(ita, eng, uso, esempio)
            # Transizione verso sinistra
            self.parent.transition.direction = "right"
            # Ritorna alla home
            self.manager.current = "screen_home" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"
            # Pulizia
            self.ids.ita.text = ""
            self.ids.eng.text = ""
            self.ids.uso.text = ""
            self.ids.esempio.text = ""

    
    # Callback function - Annulla
    def annulla(self): 
        # Transizione verso sinistra
        self.parent.transition.direction = "right"
        # Ritorno alla home
        self.manager.current = "screen_home" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"
        # Pulizia
        self.ids.ita.text = ""
        self.ids.eng.text = ""
        self.ids.uso.text = ""
        self.ids.esempio.text = ""
