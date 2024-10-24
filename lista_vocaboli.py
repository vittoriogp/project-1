from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from custom_widgets import BoxLayout
from custom_widgets import VGP_Button
from kivy.metrics import dp
from kivy.uix.label import Label
from styles import Styles
from custom_widgets import VGP_CliccableBoxLayout
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from custom_widgets import VGP_TextInput
from Firebase_Database_Management import Database
from firebase_admin import db
from custom_widgets import Test_AnchorLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle

"""
> L'interfaccia e la classe devono avere lo stesso nome. Ecco perché l'interfaccia "Lista_Vocaboli" e la classe "Lista_Vocaboli" hanno lo stesso nome.
"""

# Implementazione dell'interfaccia "Lista_Vocaboli"
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
            
<Lista_Vocaboli>: 
    # Nome dello screen
    name: "screen_lista_vocaboli"
    
    # Contenitore di tutti gli elementi
    BoxLayout: 
        alpha: 0.2
        hex_code: "#e33434"
        # Orientation
        orientation: "vertical"
        
        # Header
        BoxLayout: 
            # Colroe e trasparenza
            alpha: 0.2
            hex_code: "#7ae334"
            # Dimensione
            size_hint_y: root.ALTEZZA_HEADER
        
        # Body
        BoxLayout: 
            # Colroe e trasparenza
            alpha: 0.2
            hex_code: "#e3b134"
            # Dimensione
            size_hint_y: root.ALTEZZA_BODY
                    
            # Scrollview con i vocaboli
            ScrollView: 
                # Direzione dello scrolling
                do_scroll_y: True
                # Grid Layout contennete i vari vocaboli
                GridLayout: 
                    # ID
                    id: grid_layout
                    # Colore e trasparenza
                    alpha: 0.2
                    hex_code: "#e3da34"
                    # Spacing
                    spacing: dp(root.SPAZIO_TRA_VOCABOLI)
                    # Dimensione del Grid Layout
                    size_hint_y: None
                    height: self.minimum_height
                    # Padding
                    padding: [dp(root.PADDING_ORIZZONTALE), dp(root.PADDING_VERTICALE), dp(root.PADDING_ORIZZONTALE), dp(root.PADDING_VERTICALE)]
                    # Numero di righe e colonne
                    cols: 1            
        # Footer
        BoxLayout: 
            # Colroe e trasparenza
            alpha: 1
            hex_code: root.PRIMARY_COLOR
            # Dimensione
            size_hint_y: root.ALTEZZA_FOOTER
                    
            # Home
            Test_AnchorLayout: 
                # Colore e trasparenza
                alpha: 1
                hex_code: root.PRIMARY_COLOR
                # Ancoraggio 
                anchor_x: "center"
                anchor_y: "center"
                # Padding destro
                padding: [0, 0, dp(5), 0]
                # Button - Home
                Button: 
                    # Inserimento di un rettangolo contenente l'immagine
                    canvas: 
                        Rectangle: 
                            pos: self.pos
                            size: self.size
                            source: root.ICONA_HOME
                    # Dimensione
                    size_hint: None, None
                    size: min(self.parent.height, self.parent.height)*root.RIDUZIONE_IMMAGINE, min(self.parent.height, self.parent.height)*root.RIDUZIONE_IMMAGINE
                    # Callback - Ritorno alla home
                    on_press: root.switch_to_home()
                    # Inserimento dell'immagine (con bugfix)
                    background_normal: ''
                    background_color: 0, 0, 0, 0
        
""")

# Implementazione dell'interfaccia "Lista_Vocaboli"
class Lista_Vocaboli(Screen): 
    # DIMENSIONI
    ALTEZZA_HEADER = 0.01 # % rispetto all'altezza della pagina
    ALTEZZA_FOOTER = 0.1 # % rispetto all'altezza della pagina
    ALTEZZA_BODY = 1 - ALTEZZA_HEADER - ALTEZZA_FOOTER # % rispetto all'altezza della pagina

    ALTEZZA_VOCABOLO = 100 # Convertito in dp

    SPAZIO_TRA_VOCABOLI = 10 # Spaziatura tra le caselle corrispondenti ai vari vocaboli
    
    PADDING_ORIZZONTALE = 15 # Convertito in dp
    PADDING_VERTICALE = 15 # Convertito in dp
    PADDING_VOCABOLO = 10 # Convertito in dp

    TRASPARENZA_VOCABOLO = 0.2

    DIMENSIONE_FONT = 16

    # Fattore di riduzione della dimensione dell'immagine
    RIDUZIONE_IMMAGINE = 0.75

    # CONFIGURAZIONE POP-UP
    POPUP_ALTEZZA = 0.75 # % rispetto all'altezza della pagina
    POPUP_LARGHEZZA = 0.75 # % rispetto all'altezza della pagina
    POPUP_SEPARATORE_SPESSORE = 0 # convertito in dp

    # COLORI
    PRIMARY_COLOR = Styles.primary_color_hex

    # Icone
    ICONA_HOME = Styles.ICONA_HOME

    def on_enter(self):
        if Database.lista_vocaboli_aggiornata == 1: 
            if Database.lista_vocaboli_aggiornata is not None: 
                # Pulizia di tutti i widgets una volta chiuso il pop-up
                self.ids.grid_layout.clear_widgets()
            # Rappresentazione del database
            self.rappresenta_database_ita(self)
            # Aggiornamento lista vocaboli
            Database.lista_vocaboli_aggiornata = 0
    
    def rappresenta_database_ita(self, obj): 
        # Scarica il database completo
        database_completo_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/")
        database_completo = database_completo_ref.get()

        # Scarica gli indici
        indici_completo_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli_priorities/")
        indici_completo = indici_completo_ref.get()

        if Database.almeno_un_vocabolo == 1: 
            # Eliminazione dell'elemento "None"
            database_completo = [item for item in database_completo if item is not None]
            indici_completo = [item for item in indici_completo if item is not None]
            # Aggiunta degli ID
            for i, vocabolo in enumerate(database_completo): 
                id_item = indici_completo[i]
                vocabolo["id"] = id_item["id"]
            # Riordino della lista in ordine alfabetico
            database_completo = sorted(database_completo, key=lambda x: x.get("ita", ""))
            for vocabolo in database_completo: 
                if vocabolo.get("cancellato") is None: 
                    self.aggiungi_vocabolo_a_lista(vocabolo["id"], vocabolo["eng"], vocabolo["ita"], vocabolo["uso"], vocabolo["esempio"])

        

    def aggiungi_vocabolo_a_lista(self, vocabolo_id, eng, ita, uso, esempio): 
        # Creazione del layout contenitore corrispondente ad un singolo vocabolo
        layout_complessivo = VGP_CliccableBoxLayout(
            alpha = self.TRASPARENZA_VOCABOLO, 
            # hex_code = "#7ae334",
            hex_code = Styles.primary_color_hex,
            orientation = "vertical",
            size_hint_y = None, 
            height = dp(self.ALTEZZA_VOCABOLO),
            padding = [dp(self.PADDING_VOCABOLO), dp(self.PADDING_VOCABOLO), dp(self.PADDING_VOCABOLO), dp(self.PADDING_VOCABOLO)],
            on_press=lambda instance, id=vocabolo_id: self.show_item(id, eng, ita, uso, esempio)
        )

        # Label contenente la parola in italiano
        ita_label = Label(
            text = ita, 
            color = (0, 0, 0, 1), 
            font_size = f"{self.DIMENSIONE_FONT}sp", 
            font_name = Styles.ROBOTO_LIGHT_PATH,
            halign = "left", 
            valign = "middle",
        )
        ita_label.bind(size=lambda label, size: label.setter('text_size')(label, (label.width, None))) # ha l'effetto di collegare il cambiamento della dimensione del widget ita_label alla proprietà text_size della stessa label, in modo che text_size venga automaticamente aggiornato quando la larghezza di ita_label cambia.

        # Label contenente la parola in inglese
        eng_label = Label(
            text = eng, 
            color = (0, 0, 0, 1), 
            font_size = f"{self.DIMENSIONE_FONT}sp", 
            halign = "left", 
            valign = "middle",
            font_name = Styles.ROBOTO_LIGHT_PATH,
        )
        eng_label.bind(size=lambda label, size: label.setter('text_size')(label, (label.width, None))) # ha l'effetto di collegare il cambiamento della dimensione del widget ita_label alla proprietà text_size della stessa label, in modo che text_size venga automaticamente aggiornato quando la larghezza di ita_label cambia.

        # Label contenente l'uso
        uso_label = Label(
            text = uso, 
            color = (0, 0, 0, 1), 
            font_size = f"{self.DIMENSIONE_FONT}sp", 
            halign = "left", 
            valign = "middle",
            font_name = Styles.ROBOTO_LIGHT_PATH,
        )
        uso_label.bind(size=lambda label, size: label.setter('text_size')(label, (label.width, None))) # ha l'effetto di collegare il cambiamento della dimensione del widget ita_label alla proprietà text_size della stessa label, in modo che text_size venga automaticamente aggiornato quando la larghezza di ita_label cambia.

        # Label contenente l'esempio
        esempio_label = Label(
            text = esempio, 
            color = (0, 0, 0, 1), 
            font_size = f"{self.DIMENSIONE_FONT}sp", 
            halign = "left", 
            valign = "middle",
            font_name = Styles.ROBOTO_LIGHT_PATH,
        )
        esempio_label.bind(size=lambda label, size: label.setter('text_size')(label, (label.width, None))) # ha l'effetto di collegare il cambiamento della dimensione del widget ita_label alla proprietà text_size della stessa label, in modo che text_size venga automaticamente aggiornato quando la larghezza di ita_label cambia.
        
        # Aggiunta dei widget
        layout_complessivo.add_widget(ita_label)
        layout_complessivo.add_widget(eng_label)
        layout_complessivo.add_widget(uso_label)
        layout_complessivo.add_widget(esempio_label)

        # Aggiunta
        self.ids.grid_layout.add_widget(layout_complessivo)
    
    def show_item(self, id, eng, ita, uso, esempio): 
        # Creazione di un nuovo pop-up
        popup = VGP_Popup(id, eng, ita, uso, esempio)
        # Chiusura del pop-up
        popup.bind(on_dismiss=self.riaggiorna_lista)
        # Show popup
        popup.open()
    
    def riaggiorna_lista(self, instance): 
        # Pulizia di tutti i widgets una volta chiuso il pop-up
        self.ids.grid_layout.clear_widgets()
        # Richiamo della funzione aggiornata
        self.rappresenta_database_ita(self)

    def switch_to_home(self): 
        # Transizione verso sinistra
        self.parent.transition.direction = "left"
        # Passaggio allo screen "Add_word"
        self.manager.current = "screen_home" # self.manager ritorna lo ScreenManager dello Screen, in questo caso "Interfaccia_ScreenManager"


    



class VGP_Popup(ModalView):
    # Colore e trasparenza
    ALPHA = 1

    # Dimensioni
    POPUP_LARGHEZZA = 0.75
    POPUP_ALTEZZA = 0.6

    PADDING = 20
    SPAZIO_TRA_ELEMENTI = 10
    ALTEZZA_INPUT = 50

    SPAZIO_TRA_BUTTONS = 10

    def __init__(self, input_id, input_ita, input_eng, input_uso, input_esempio, **kwargs):
        super(VGP_Popup, self).__init__(**kwargs)
        # Sfondo
        self.background = ""
        self.background_color = (1, 1, 1, 1)
        # Dimensioni
        self.size_hint_x = self.POPUP_LARGHEZZA
        self.size_hint_y = self.POPUP_ALTEZZA

        # Layout principale
        layout_principale = BoxLayout(
            alpha = 0.2, 
            hex_code = "#e3b134",
            size_hint = (1, 1),
            orientation = "vertical", 
            padding = [dp(self.PADDING), dp(self.PADDING), dp(self.PADDING), dp(self.PADDING)],
            spacing = dp(self.SPAZIO_TRA_ELEMENTI),
        )

        # Vocabolo in inglese
        eng_label = VGP_TextInput(
            text = input_eng,
            hint_text_color = (0, 0, 0, 1),
        )
        layout_principale.add_widget(eng_label)
        
        # Vocabolo in italiano
        ita_label = VGP_TextInput(
            text = input_ita,
            hint_text_color = (0, 0, 0, 1),
        )
        layout_principale.add_widget(ita_label)
        
        # Vocabolo uso
        uso_label = VGP_TextInput(
            text = input_uso,
            hint_text_color = (0, 0, 0, 1),
        )
        layout_principale.add_widget(uso_label)
        
        # Vocabolo uso
        esempio_label = VGP_TextInput(
            text = input_esempio,
            hint_text_color = (0, 0, 0, 1),
        )
        layout_principale.add_widget(esempio_label)

        # Aggiunta dei due buttons (Modifica e cancella)
        layout_buttons = BoxLayout(
            # Orientamento
            orientation = "horizontal",
            # Spaziatura 
            spacing = self.SPAZIO_TRA_BUTTONS,
            # Colore 
            alpha = 0.2, 
            hex_code = "#e33434",
        )
        layout_principale.add_widget(layout_buttons)

        # Aggiunta del tasto di modifica
        pulsante_modifica = VGP_Button(
            text = "Modifica", 
            on_release=lambda instance: self.modifica_vocabolo(input_id, eng_label.text, ita_label.text, uso_label.text, esempio_label.text)
        )
        layout_buttons.add_widget(pulsante_modifica)

        # Aggiunta del tasto di modifica
        pulsante_cancella = VGP_Button(
            text = "Cancella", 
            on_release=lambda instance: self.cancella_vocabolo(input_id)
        )
        layout_buttons.add_widget(pulsante_cancella)

        # Aggiunta del contenitore al popup
        self.add_widget(layout_principale)

    def cancella_vocabolo(self, input_id): 
        # Cancellazione del vocabolo
        Database.cancella_vocabolo(input_id)
        # Chiusura del pop-up e richiamo della relativa callback function
        self.dismiss()

    def modifica_vocabolo(self, input_id, eng, ita, uso, esempio): 
        # Modifica del database
        Database.aggiorna_vocabolo(input_id, eng, ita, uso, esempio)
        # Chiusura del pop-up e richiamo della relativa callback function
        self.dismiss()

