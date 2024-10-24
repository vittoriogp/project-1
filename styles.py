from kivy.utils import rgba
import os

class Styles: 
    # Colore primario dell'applicazione
    primary_color_hex = "#044789"
    primary_color = rgba(primary_color_hex) # rgba("#7F32CB") # Viola
    # Colore secondario dell'applicazione
    secondary_color_hex = "#090909"
    secondary_color = rgba(secondary_color_hex) # Nero
    # Colore terziario dell'applicazione
    tertiary_color_hex = "#E8E6E6"
    tertiary_color = rgba(tertiary_color_hex)
    
    # Colore dei pulsanti
    button_backgroundColor = primary_color
    # Colore del background dei text input
    text_input_background_color = tertiary_color

    # Path dei fonts
    
    ROBOTO_BLACK_PATH = os.path.abspath(os.path.dirname(__file__)) + "/fonts/Roboto_Black.ttf"
    ROBOTO_LIGHT_PATH = os.path.abspath(os.path.dirname(__file__)) + "/fonts/Roboto_Light.ttf"

    # Dimensione totale della finestra
    FINESTRA_LARGHEZZA = 500
    FINESTRA_ALTEZZA = 700

    # Icone
    ICONA_LISTA_VOCABOLI = os.path.abspath(os.path.dirname(__file__)) + "/Icone/rectangle-list.png"
    ICONA_ITALIANO = os.path.abspath(os.path.dirname(__file__)) + "/Icone/Italia.png"
    ICONA_INGLESE = os.path.abspath(os.path.dirname(__file__)) + "/Icone/Inghilterra.png"
    ICONA_AGGIUNGI_VOCABOLO = os.path.abspath(os.path.dirname(__file__)) + "/Icone/multiple.png"
    ICONA_VOCABOLO_CONOSCIUTO = os.path.abspath(os.path.dirname(__file__)) + "/Icone/check.png"
    ICONA_VOCABOLO_SCONOSCIUTO = os.path.abspath(os.path.dirname(__file__)) + "/Icone/cross-circle.png"
    ICONA_MOSTRA = os.path.abspath(os.path.dirname(__file__)) + "/Icone/view_4362272.png"
    ICONA_NASCONDI = os.path.abspath(os.path.dirname(__file__)) + "/Icone/hide_9684799.png"
    ICONA_ASCOLTA = os.path.abspath(os.path.dirname(__file__)) + "/Icone/listen_4906.png"
    ICONA_HOME = os.path.abspath(os.path.dirname(__file__)) + "/Icone/home.png"
    LOGO = os.path.abspath(os.path.dirname(__file__)) + "/Immagini/Logo5.png"
