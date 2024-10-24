from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from styles import Styles
from kivy.graphics import Rectangle
from kivy.app import App
import platform
import pyttsx3
import sys


# Importazione del database_management
# from SQL_database_management import Database
from Firebase_Database_Management import Database

"""
> L'interfaccia e la classe devono avere lo stesso nome. Ecco perché l'interfaccia "Home" e la classe "Home" hanno lo stesso nome.
"""

# Implementazione dell'interfaccia "Login"
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
            
<Home>: 
                                      
    # Nome dello screen
    name: "screen_home"
    
    # BoxLayout contenente tutti gli elementi
    BoxLayout: 
        # Colore e trasparenza
        alpha: 0.2
        hex_code: "#e33434"
        # Orientamtno
        orientation: "vertical"
        
        # Header (barra superiore)
        BoxLayout: 
            # Colore e trasparenza
            alpha: 0.2
            hex_code: "#e3b134"
            
            # Dimensione verticale
            size_hint_y: root.HEADER_ALTEZZA

            #  Button: Lista vocaboli
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio al centro
                anchor_x: "center"
                anchor_y: "center"
                # Button
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_LISTA_VOCABOLI
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE, min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE
                    # Callback - Ritorno a lista vocaboli
                    on_press: root.switch_to_lista_vocaboli()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0
            
            # Bandiera italiana - Switcha alla lingua italiana
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio 
                anchor_x: "right"
                anchor_y: "center"
                # Padding destro
                padding: [0, 0, dp(5), 0]
                # Button - Ritorno a Login
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_ITALIANO
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE, min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE
                    # Callback - Ritorno a Login
                    on_press: root.switch_to_italian()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0
            
            # Bandiera dell'inghilterra - Switcha alla lingua inglese
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio
                anchor_x: "left"
                anchor_y: "center"
                # Padding sinistro
                padding: [dp(5), 0, 0, 0]
                # Button
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_INGLESE
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE, min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE
                    # Callback - Ritorno a Login
                    on_press: root.switch_to_english()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0
            # Aggiungi un nuovo vocabolo
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio
                anchor_x: "center"
                anchor_y: "center"
                # Button
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_AGGIUNGI_VOCABOLO
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE, min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE
                    # Callback - Switch a add_word
                    on_press: root.switch_to_add_word()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0

        # Body - Card 
        # AnchorLayout per ancorare al centro
        AnchorLayout: 
            # Colore e trasparenza
            alpha: 0.7
            hex_code: "#7ae334"
            
            # Dimensione verticale
            size_hint_y: root.BODY_ALTEZZA
            
            # Ancoraggio al centro
            anchor_y: "center"
            anchor_x: "center"
            
            # Padding
            padding: [dp(root.PADDING_BODY_SCRITTE), dp(root.PADDING_BODY_SCRITTE), dp(root.PADDING_BODY_SCRITTE), dp(root.PADDING_BODY_SCRITTE)]
            
            # Rettangolo contenente la card
            canvas: 
                Color: 
                    rgba: 1, 1, 1, 1  # Colore del rettangolo
                RoundedRectangle:
                    pos: self.center_x - (self.width - dp(root.PADDING_BODY_CONTORNOCARD)) / 2, self.center_y - (self.height - dp(root.PADDING_BODY_CONTORNOCARD)) / 2  # Posizione del rettangolo
                    size: self.width - dp(root.PADDING_BODY_CONTORNOCARD), self.height - dp(root.PADDING_BODY_CONTORNOCARD) # Dimensioni del rettangolo
                    radius: [root.CARD_RAGGIO, root.CARD_RAGGIO, root.CARD_RAGGIO, root.CARD_RAGGIO]  # Raggio per gli angoli smussati
                Color: 
                    rgba: root.PRIMARY_COLOR
                Line:
                    width: root.CARD_CONTORNO_SPESSORE  # Spessore del contorno
                    rounded_rectangle: (self.center_x - (self.width - dp(root.PADDING_BODY_CONTORNOCARD)) / 2, self.center_y - (self.height - dp(root.PADDING_BODY_CONTORNOCARD)) / 2, self.width - dp(root.PADDING_BODY_CONTORNOCARD), self.height - dp(root.PADDING_BODY_CONTORNOCARD), root.CARD_RAGGIO, root.CARD_RAGGIO, root.CARD_RAGGIO, root.CARD_RAGGIO)  # Dimensioni e raggio degli angoli smussati
            
            # BoxLayout contenente i vari elementi della card
            BoxLayout: 
                # Colore e trasparenza
                alpha: 0.2
                hex_code: "#e3da34"
                # Orientamento verticale
                orientation: "vertical"
                # Spaziatura tra i vari elementi
                spacing: dp(10)
                # Label - Parola da tradurre 
                Label: 
                    id: testo_da_tradurre_id
                    # Rettangolo per la parola da tradurre
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1  # Colore del bordo
                        Line:
                            points: [self.x, self.y, self.right, self.y, self.right, self.top, self.x, self.top, self.x, self.y]  # Crea un rettangolo attorno al Label
                            width: root.CARD_CONTORNO_SPESSORE  # Spessore del bordo
                        Color:
                            rgba: root.PRIMARY_COLOR
                        Rectangle: 
                            pos: self.center_x - self.width/2, self.center_y - self.height/2
                            size: self.width, self.height
                    # Testo da tradurre
                    # text: "Placeholder".upper()
                    # Dimensione del testo
                    text_size: self.width, None
                    # Allineamento
                    halign: "center"
                    valign: "middle"
                    # Colore
                    color: 1, 1, 1, 1
                    # Dimensione del font
                    font_size: "16sp"  
                    # Font
                    font_name: root.font_path  

                # Traduzione
                Label: 
                    # Id
                    id: testo_tradotto_id
                    # Traduzione
                    # text: "Look after".upper()
                    # Dimensione del testo
                    text_size: self.width, None
                    # Allineamento
                    halign: "center"
                    valign: "middle"
                    # Colore del font
                    color: 0, 0, 0, 1
                    # Dimensione del font
                    font_size: "16sp"  
                    # Nome del font
                    font_name: root.font_path
            
                # Utilizzo
                Label: 
                    # ID
                    id: utilizzo_id
                    # Testo
                    # text: "To look after <someone>"
                    # Dimensione del testo
                    text_size: self.width, None
                    # Allineamento
                    halign: "center"
                    valign: "middle"
                    # Colore del font
                    color: 0, 0, 0, 1
                    # Dimensione del font
                    font_size: "16sp"  
                    # Nome del font
                    font_name: root.font_path
                
                # Esempio di utilizzo
                Label:
                    # ID
                    id: esempio_id
                    # Testo
                    # text: "I have to look after Lupin even if it is not my dog"
                    # Dimensione del testo
                    text_size: self.width, None
                    # Allineamento
                    halign: "center"
                    valign: "middle"
                    # Colore
                    color: 0, 0, 0, 1
                    # Dimensione del font
                    font_size: "16sp"
                    # Nome del font
                    font_name: root.font_path
                    
        # Footer (barra in basso)
        BoxLayout: 
            # Colore e trasparenza
            alpha: 0.1
            hex_code: "#3440e3"
            # Dimensione verticale
            size_hint_y: root.FOOTER_ALTEZZA
            # Orientamento
            orientation: "horizontal"
            # Rettangolo contenente la barra
            canvas.before: 
                Color: 
                    rgba: root.PRIMARY_COLOR
                Rectangle:
                    pos: self.center_x -self.width/2, self.center_y - self.height/2 
                    size: self.width, self.height
            # Button - Conosco la parola
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio
                anchor_x: "center"
                anchor_y: "center"
                # Button
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_VOCABOLO_CONOSCIUTO
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*0.75, min(self.parent.height, self.parent.height)*0.75
                    # Callback - Nel caso in cui la parola sia conosciuta
                    on_press: root.is_known()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0

            # Button - Mostra o nascondi
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio
                anchor_x: "center"
                anchor_y: "center"
                # Button
                Button: 
                    # ID
                    id: button_mostra_nascondi_id
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_MOSTRA
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*0.75, min(self.parent.height, self.parent.height)*0.75
                    # Callback - Nel caso in cui la parola sia conosciuta
                    on_press: root.mostra_o_nascondi()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0

            # Button - Ascolta
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio
                anchor_x: "center"
                anchor_y: "center"
                # Button
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_ASCOLTA
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*0.75, min(self.parent.height, self.parent.height)*0.75
                    # Callback - Nel caso in cui la parola sia conosciuta
                    on_press: root.ascolta()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0
                    
            # Button - Non conosco la parola
            AnchorLayout: 
                # Colore e trasparenza
                alpha: 0.5
                hex_code: "#e3b134"
                # Ancoraggio
                anchor_x: "center"
                anchor_y: "center"
                # Button 
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_VOCABOLO_SCONOSCIUTO
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE, min(self.parent.height, self.parent.height)*root.ICONE_CHECK_DIMENSIONE
                    # Callback - Ritorno a Login
                    on_press: root.is_unknown()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0
        
""")

# Implementazione dell'interfaccia "Signup"
class Home(Screen): 
    # Dimensioni geometriche
    HEADER_ALTEZZA = 0.1 # % rispetto all'altezza della pagina
    BODY_ALTEZZA = 0.8 # % rispetto all'altezza della pagina
    FOOTER_ALTEZZA = 0.1 # % rispetto all'altezza della pagina
    
    PADDING_BODY_SCRITTE = 80 # Padding tra il box Body e i box contenenti le scritte
    PADDING_BODY_CONTORNOCARD = 120 # Padding tra il box Body e il contorno della card 

    CARD_RAGGIO = 20
    CARD_CONTORNO_SPESSORE = 1.5

    ICONE_CHECK_DIMENSIONE = 0.75

    # Colori
    PRIMARY_COLOR = (Styles.primary_color[0], Styles.primary_color[1], Styles.primary_color[2], 1)

    # Flag
    primo_avvio = 1

    # Font
    font_path = Styles.ROBOTO_BLACK_PATH

    # Icone
    ICONA_LISTA_VOCABOLI = Styles.ICONA_LISTA_VOCABOLI
    ICONA_ITALIANO = Styles.ICONA_ITALIANO
    ICONA_INGLESE = Styles.ICONA_INGLESE
    ICONA_AGGIUNGI_VOCABOLO = Styles.ICONA_AGGIUNGI_VOCABOLO
    ICONA_VOCABOLO_CONOSCIUTO = Styles.ICONA_VOCABOLO_CONOSCIUTO
    ICONA_VOCABOLO_SCONOSCIUTO = Styles.ICONA_VOCABOLO_SCONOSCIUTO
    ICONA_MOSTRA = Styles.ICONA_MOSTRA
    ICONA_NASCONDI = Styles.ICONA_NASCONDI
    ICONA_ASCOLTA = Styles.ICONA_ASCOLTA

    # Callback function eseguita all'apertura dello screen
    def on_enter(self):
        # Cambio del vocabolo mostrato all'interno dell'applicazione
        Database.cambia_vocabolo()
        # Qui puoi chiamare la funzione che desideri eseguire all'apertura dello screen
        self.mostra_vocabolo_senza_dettagli()
        # Aggiornamento della visualizzazione
        self.is_view = 0
        self.switch_to_iconaMostra()

    
    def mostra_vocabolo_senza_dettagli(self): 
        # Verifica che ci sia un vocabolo da mostrare
        if Database.vocabolo_da_mostrare is not None: 
            # Rappresentazione del testo da tradurre
            if Database.logged_lingua_da_tradurre == "ita": 
                self.ids.testo_da_tradurre_id.text = Database.vocabolo_da_mostrare["ita"].upper()
            if Database.logged_lingua_da_tradurre == "eng": 
                self.ids.testo_da_tradurre_id.text = Database.vocabolo_da_mostrare["eng"].upper()
            # Rappresentazione del testo tradotto
            self.ids.testo_tradotto_id.text = ""
            # Rappresentazione dell'utilizzo
            self.ids.utilizzo_id.text = ""
            # Rappresentazione dell'esempio
            self.ids.esempio_id.text = ""
            # Mostra dello stato di visualizzazione
            self.is_view = 0
            # Cambia l'icona 
            self.switch_to_iconaMostra()
        else: 
            self.ids.testo_da_tradurre_id.text = ""
            self.ids.testo_tradotto_id.text = ""
            self.ids.utilizzo_id.text = ""
            self.ids.esempio_id.text = ""

    # Funzione per switchare la lingua da tradurre in inglese
    def switch_to_english(self): 
        if Database.logged_lingua_da_tradurre != "eng": 
            # Modifica la lingua nel database
            Database.switch_to_english()
            # Aggiornamento della rapprsentazione del vocabolo
            if self.is_view == 0: 
                self.mostra_vocabolo_senza_dettagli()
            else: 
                self.mostra_vocabolo_senza_dettagli()
                self.mostra_dettagli_parola()

    # Funzione per switchare la lingua da tradurre in italiano
    def switch_to_italian(self): 
        if Database.logged_lingua_da_tradurre != "ita": 
            # Modifica la lingua nel database
            Database.switch_to_italian()
            # Aggiornamento della rapprsentazione del vocabolo
            if self.is_view == 0: 
                self.mostra_vocabolo_senza_dettagli()
            else: 
                self.mostra_vocabolo_senza_dettagli()
                self.mostra_dettagli_parola()
    
    # Mostra dettagli della parola
    def mostra_dettagli_parola(self):
        # Verifica che sia stato definito un vocabolo
        if Database.vocabolo_da_mostrare is not None:  
            # Mostra testo tradotto
            if Database.logged_lingua_da_tradurre == "ita": 
                self.ids.testo_tradotto_id.text = Database.vocabolo_da_mostrare["eng"].upper()
            if Database.logged_lingua_da_tradurre == "eng": 
                self.ids.testo_tradotto_id.text = Database.vocabolo_da_mostrare["ita"].upper()
            # Rappresentazione dell'utilizzo
            self.ids.utilizzo_id.text = Database.vocabolo_da_mostrare["uso"]
            # Rappresentazione dell'esempio
            self.ids.esempio_id.text = Database.vocabolo_da_mostrare["esempio"]
            # Modifica dello stato 
            self.is_view = 1

    def mostra_o_nascondi(self): 
        if Database.vocabolo_da_mostrare is not None: 
            if self.is_view == 0: 
                self.mostra_dettagli_parola()
                self.switch_to_iconaNascondi()
            else: 
                self.mostra_vocabolo_senza_dettagli()
                self.switch_to_iconaMostra()

    def switch_to_add_word(self): 
        # Transizione verso sinistra
        self.parent.transition.direction = "left"
        # Passaggio allo screen "Add_word"
        self.manager.current = "screen_add_word" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"
    
    def switch_to_lista_vocaboli(self): 
        # Transizione verso destra
        self.parent.transition.direction = "right"
        self.manager.current = "screen_lista_vocaboli" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"

    def is_unknown(self): 
        # Aggiornamento del database con la priorità
        Database.aumenta_priority()
        # Cambio del vocabolo mostrato all'interno dell'applicazione
        Database.cambia_vocabolo()
        # Qui puoi chiamare la funzione che desideri eseguire all'apertura dello screen
        self.mostra_vocabolo_senza_dettagli()
    
    def is_known(self): 
        # Aggiornamento del database con la priorità
        Database.diminuisci_priority()
        # Cambio del vocabolo mostrato all'interno dell'applicazione
        Database.cambia_vocabolo()
        # Qui puoi chiamare la funzione che desideri eseguire all'apertura dello screen
        self.mostra_vocabolo_senza_dettagli()

    # Mostra l'icona "Mostra"
    def switch_to_iconaMostra(self): 
        if self.primo_avvio == 0: 
            self.ids.button_mostra_nascondi_id.canvas.clear()
            with self.ids.button_mostra_nascondi_id.canvas:
                Rectangle(
                    pos=self.ids.button_mostra_nascondi_id.pos, 
                    size=self.ids.button_mostra_nascondi_id.size, 
                    source=self.ICONA_MOSTRA
                )
        
    # Mostra l'icona "Nascondi"
    def switch_to_iconaNascondi(self): 
        self.primo_avvio = 0
        self.ids.button_mostra_nascondi_id.canvas.clear()
        with self.ids.button_mostra_nascondi_id.canvas:
            Rectangle(pos=self.ids.button_mostra_nascondi_id.pos, size=self.ids.button_mostra_nascondi_id.size, source=self.ICONA_NASCONDI)

    def ascolta(self): 
        if Database.vocabolo_da_mostrare is not None: 
            # Identificazione del testo da leggere
            testo_da_leggere = Database.vocabolo_da_mostrare["eng"]

            # PIATTAFORMA ANDROID
            if sys.platform == 'android': 
                pass


            # PIATTAFORMA WINDOWS O MAC
            if platform.system() == 'Windows' or platform.system() == 'Darwin': 
                # Inizializzazione
                engine = pyttsx3.init()
                # Impostazione della velocità della voce
                engine.setProperty('rate', 150)  # Imposta la velocità della voce (opzionale)
                # Impostazione del volume
                engine.setProperty('volume', 1)  # Imposta il volume (da 0.0 a 1.0)
                # Leggi il testo
                engine.say(testo_da_leggere)
                engine.runAndWait()  # Aspetta che il testo venga letto

            # Piattaforma iOS
            if sys.platform == 'ios': 
                pass
        else:       
            pass