from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import json

class MiguIA(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        self.layout.add_widget(Label(text="MiguIA - UNFV Edition", size_hint_y=None, height=50, bold=True))

        # Configuración de URL (Para no compilar cada vez)
        self.url_input = TextInput(
            text="https://nonciliated-overprolifically-reva.ngrok-free.dev", 
            hint_text="Pega aquí tu nueva URL de Ngrok",
            size_hint_y=None, height=50, multiline=False
        )
        self.layout.add_widget(self.url_input)

        # Historial de chat
        self.scroll = ScrollView()
        self.chat_history = Label(text="MiguIA: ¡Conexión lista! Escribe algo abajo.\n", 
                                 size_hint_y=None, halign='left', valign='top')
        self.chat_history.bind(size=self.chat_history.setter('text_size'))
        self.scroll.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll)

        # Entrada de mensaje
        self.input = TextInput(hint_text="Pregúntale algo a la IA...", size_hint_y=None, height=100)
        self.layout.add_widget(self.input)

        # Botón enviar
        self.btn = Button(text="Enviar", size_hint_y=None, height=60, background_color=(0, 0.4, 0, 1))
        self.btn.bind(on_press=self.send_message)
        self.layout.add_widget(self.btn)

        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        ngrok_url = self.url_input.text.strip()
        
        if user_text:
            self.chat_history.text += f"\nMiguel: {user_text}\n"
            self.input.text = ""
            
            try:
                # LLAMADA CON SALTO DE ADVERTENCIA DE NGROK
                response = requests.post(
                    f"{ngrok_url}/api/generate",
                    json={"model": "llama3", "prompt": user_text, "stream": False},
                    headers={"ngrok-skip-browser-warning": "true"}, # <--- EL TRUCO MÁGICO
                    timeout=30
                )
                
                if response.status_code == 200:
                    answer = response.json().get('response', 'Sin respuesta')
                    self.chat_history.text += f"MiguIA: {answer}\n"
                else:
                    self.chat_history.text += f"Error del servidor: {response.status_code}\n"
            except Exception as e:
                self.chat_history.text += f"MiguIA: Revisa si tu Nitro V15 tiene el Ngrok abierto.\n"
