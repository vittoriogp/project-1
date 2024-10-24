from kivy.lang import Builder
from styles import Styles
from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.properties import BoundedNumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
import os

# Classi per il test della struttura
class Test_BoxLayout(BoxLayout):
    alpha=BoundedNumericProperty(0, min=0, max=1)
    hex_code=StringProperty("#FFFFFF")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_background)
        Clock.schedule_interval(self.update,1/30)
    def hex_to_rgb(self,hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal/255)
        return rgb
    def update(self, *args):
        self.rect.pos=self.pos
        self.rect.size=self.size
    def create_background(self, *args):
        self.hex_code=str(self.hex_code).split("#")[-1]
        r,g,b=self.hex_to_rgb(self.hex_code)
        with self.canvas.before:
            Color(r,g,b,self.alpha)
            self.rect=Rectangle(pos=self.pos, size=self.size)

class Test_AnchorLayout(AnchorLayout):
    alpha=BoundedNumericProperty(0, min=0, max=1)
    hex_code=StringProperty("#FFFFFF")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_background)
        Clock.schedule_interval(self.update,1/30)
    def hex_to_rgb(self,hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal/255)
        return rgb
    def update(self, *args):
        self.rect.pos=self.pos
        self.rect.size=self.size
    def create_background(self, *args):
        self.hex_code=str(self.hex_code).split("#")[-1]
        r,g,b=self.hex_to_rgb(self.hex_code)
        with self.canvas.before:
            Color(r,g,b,self.alpha)
            self.rect=Rectangle(pos=self.pos, size=self.size)

class Test_FloatLayout(FloatLayout):
    alpha=BoundedNumericProperty(0, min=0, max=1)
    hex_code=StringProperty("#FFFFFF")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_background)
        Clock.schedule_interval(self.update,1/30)
    def hex_to_rgb(self,hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal/255)
        return rgb
    def update(self, *args):
        self.rect.pos=self.pos
        self.rect.size=self.size
    def create_background(self, *args):
        self.hex_code=str(self.hex_code).split("#")[-1]
        r,g,b=self.hex_to_rgb(self.hex_code)
        with self.canvas.before:
            Color(r,g,b,self.alpha)
            self.rect=Rectangle(pos=self.pos, size=self.size)

class Test_StackLayout(StackLayout):
    alpha=BoundedNumericProperty(0, min=0, max=1)
    hex_code=StringProperty("#FFFFFF")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_background)
        Clock.schedule_interval(self.update,1/30)
    def hex_to_rgb(self,hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal/255)
        return rgb
    def update(self, *args):
        self.rect.pos=self.pos
        self.rect.size=self.size
    def create_background(self, *args):
        self.hex_code=str(self.hex_code).split("#")[-1]
        r,g,b=self.hex_to_rgb(self.hex_code)
        with self.canvas.before:
            Color(r,g,b,self.alpha)
            self.rect=Rectangle(pos=self.pos, size=self.size)

class Test_GridLayout(GridLayout):
    alpha=BoundedNumericProperty(0, min=0, max=1)
    hex_code=StringProperty("#FFFFFF")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_background)
        Clock.schedule_interval(self.update,1/30)
    def hex_to_rgb(self,hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal/255)
        return rgb
    def update(self, *args):
        self.rect.pos=self.pos
        self.rect.size=self.size
    def create_background(self, *args):
        self.hex_code=str(self.hex_code).split("#")[-1]
        r,g,b=self.hex_to_rgb(self.hex_code)
        with self.canvas.before:
            Color(r,g,b,self.alpha)
            self.rect=Rectangle(pos=self.pos, size=self.size)


# Button personalizzato
Builder.load_string("""
<VGP_Button>:  
    # Colore del background del pulsante
    background_color: self.bg_color
    background_normal: ""
    # Callback functions quando viene premuto/rilasciato il pulsante
    on_press: root.button_pressed()
    on_release: root.button_released()
                    
""")

class VGP_Button(Button):
    # Colore di background del pulsante
    bg_color = Styles.button_backgroundColor

    # Funzione richiamata quando viene premuto il pulsante
    def button_pressed(self): 
        # Cambio colore del tasto (viene cambiata solamente l'opacità del tasto)
        self.background_color = (self.bg_color[0], self.bg_color[1], self.bg_color[2], 0.8) 

    # Funzione richiamata quando viene rilasciato il pulsante
    def button_released(self): 
        # Cambio del colore del tasto (riportato al colore originario)
        self.background_color = self.bg_color

# Text input personalizzato
Builder.load_string("""
<VGP_TextInput>:
    # Colore del background del text input
    background_color: self.bg_color
    background_normal: "" 
    # Definizione del font
    font_name: root.font_path # Scaricato da https://www.fontsquirrel.com/fonts/list/popular
    # Dimensione del font
    font_size: "16sp"
    # Padding per centrare l'hint test all'interno del text input
    padding: [(self.height - self.font_size)/2, (self.height - self.font_size)/2, (self.height - self.font_size)/2, 0]
""")

class VGP_TextInput(TextInput): 
    # Colore di background del text input
    bg_color = Styles.text_input_background_color
    # Font
    font_path = Styles.ROBOTO_LIGHT_PATH


# Testo utilizzato all'interno dello Screen "Login" per il testo "Signup"
Builder.load_string("""
<VGP_SignupText>:
    # Colore del testo
    color: self.bg_color
""")

class VGP_SignupText(ButtonBehavior, Label):
    # Colore di background del pulsante
    bg_color = Styles.primary_color

# BoxLayout cliccabile
Builder.load_string("""
<VGP_CliccableBoxLayout>:
    
""")

class VGP_CliccableBoxLayout(ButtonBehavior, Test_BoxLayout):
    pass