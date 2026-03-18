from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import json

class MiguIA_App(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título épico de MiguIA
        self.layout.add_widget(Label(text="[b]MiguIA - UNFV Edition[/b]", 
                                    markup=True, size_hint_y=0.1, font_size='20sp'))

        # Área de chat
        self.scroll = ScrollView(size_hint_y=0.7)
        self.chat_history = Label(text="MiguIA: ¡Hola Miguel! Estoy listo para tus consultas universitarias.\n", 
                                 valign='top', halign='left', text_size=(400, None))
        self.scroll.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll)

        # Entrada de texto
        self.input = TextInput(hint_text="Escribe a MiguIA...", size_hint_y=0.1, multiline=False)
        self.layout.add_widget(self.input)

        # Botón enviar
        btn = Button(text="Enviar", size_hint_y=0.1, background_color=(0, 0.7, 0.3, 1))
        btn.bind(on_press=self.enviar_mensaje)
        self.layout.add_widget(btn)

        return self.layout

    def enviar_mensaje(self, instance):
        pregunta = self.input.text
        if pregunta:
            self.chat_history.text += f"Miguel: {pregunta}\n"
            self.input.text = ""
            
            # --- AQUÍ ESTÁ TU DIRECCIÓN DE NGROK ---
            url_ngrok = "https://nonciliated-overprolifically-reva.ngrok-free.dev/api/generate"
            
            data = {"model": "llama3", "prompt": pregunta, "stream": False}
            
            try:
                res = requests.post(url_ngrok, json=data, timeout=10)
                respuesta = res.json()['response']
                self.chat_history.text += f"MiguIA: {respuesta}\n\n"
            except Exception as e:
                self.chat_history.text += f"Error: ¿Ngrok está abierto? {e}\n"

if __name__ == '__main__':
    MiguIA_App().run()
