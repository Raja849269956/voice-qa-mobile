from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import threading
import os
import requests
import json

try:
    from android.permissions import request_permissions, Permission
    ANDROID = True
except ImportError:
    ANDROID = False

class VoiceQAApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = ''
        self.client = None
        
    def build(self):
        if ANDROID:
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.title_label = Label(
            text='🎤 Voice Q&A Assistant',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        layout.add_widget(self.title_label)
        
        self.status_label = Label(
            text='Status: Ready',
            size_hint_y=0.08,
            font_size='16sp',
            color=(0.13, 0.59, 0.95, 1)
        )
        layout.add_widget(self.status_label)
        
        api_key_label = Label(
            text='API Key (get from console.anthropic.com):',
            size_hint_y=0.06,
            font_size='12sp'
        )
        layout.add_widget(api_key_label)
        
        self.api_key_input = TextInput(
            text='',
            hint_text='sk-ant-...',
            multiline=False,
            size_hint_y=0.08,
            font_size='12sp',
            password=True
        )
        self.api_key_input.bind(text=self.on_api_key_change)
        layout.add_widget(self.api_key_input)
        
        question_input_label = Label(
            text='Ask a Question:',
            size_hint_y=0.06,
            font_size='14sp',
            bold=True
        )
        layout.add_widget(question_input_label)
        
        self.question_input = TextInput(
            text='',
            hint_text='Type your question here...',
            multiline=True,
            size_hint_y=0.15,
            font_size='14sp'
        )
        layout.add_widget(self.question_input)
        
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=0.5, spacing=10)
        
        question_label = Label(
            text='Last Question:',
            size_hint_y=0.1,
            font_size='16sp',
            bold=True
        )
        scroll_layout.add_widget(question_label)
        
        self.question_text = Label(
            text='Waiting for question...',
            size_hint_y=0.4,
            font_size='14sp',
            color=(0, 0, 0, 1)
        )
        scroll_layout.add_widget(self.question_text)
        
        answer_label = Label(
            text='Answer:',
            size_hint_y=0.1,
            font_size='16sp',
            bold=True
        )
        scroll_layout.add_widget(answer_label)
        
        self.answer_text = Label(
            text='Answer will appear here...',
            size_hint_y=0.4,
            font_size='14sp',
            color=(0, 0, 0, 1)
        )
        scroll_layout.add_widget(self.answer_text)
        
        layout.add_widget(scroll_layout)
        
        self.ask_btn = Button(
            text='🤔 Get Answer',
            background_color=(0.3, 0.69, 0.31, 1),
            size_hint_y=0.12,
            font_size='18sp',
            bold=True
        )
        self.ask_btn.bind(on_press=self.ask_question)
        self.ask_btn.disabled = True
        layout.add_widget(self.ask_btn)
        
        return layout
    
    def on_api_key_change(self, instance, value):
        self.api_key = value.strip()
        if self.api_key.startswith('sk-ant-') and len(self.api_key) > 20:
            self.client = True
            self.status_label.text = 'Status: API Key Set ✓'
            self.status_label.color = (0.3, 0.69, 0.31, 1)
            self.ask_btn.disabled = False
        else:
            self.status_label.text = 'Status: Enter valid API key'
            self.status_label.color = (0.96, 0.26, 0.21, 1)
            self.ask_btn.disabled = True
    
    def ask_question(self, instance):
        question = self.question_input.text.strip()
        
        if not question:
            self.status_label.text = 'Status: Please enter a question'
            return
        
        if not self.client:
            self.status_label.text = 'Status: API Key Missing'
            return
        
        self.status_label.text = 'Status: Getting answer...'
        self.ask_btn.disabled = True
        
        def get_answer():
            try:
                response = requests.post(
                    'https://api.anthropic.com/v1/messages',
                    headers={
                        'x-api-key': self.api_key,
                        'anthropic-version': '2023-06-01',
                        'content-type': 'application/json'
                    },
                    json={
                        'model': 'claude-sonnet-4-20250514',
                        'max_tokens': 200,
                        'system': 'Answer in exactly 5-6 lines, be concise and direct.',
                        'messages': [{'role': 'user', 'content': question}]
                    },
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                answer = data['content'][0]['text'].strip()
                
                Clock.schedule_once(lambda dt: self.update_answer(question, answer))
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_error(str(e)))
        
        threading.Thread(target=get_answer, daemon=True).start()
    
    def update_answer(self, question, answer):
        self.question_text.text = question
        self.answer_text.text = answer
        self.status_label.text = 'Status: ✓ Complete'
        self.status_label.color = (0.3, 0.69, 0.31, 1)
        self.ask_btn.disabled = False
    
    def update_error(self, error):
        self.status_label.text = f'Status: Error - {error}'
        self.status_label.color = (0.96, 0.26, 0.21, 1)
        self.ask_btn.disabled = False

if __name__ == '__main__':
    VoiceQAApp().run()
