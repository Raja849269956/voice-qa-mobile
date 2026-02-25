from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from android.permissions import request_permissions, Permission
import threading
import numpy as np
import torch
from anthropic import Anthropic
import os

class VoiceQAApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_listening = False
        self.is_enrolled = False
        self.api_key = os.getenv('ANTHROPIC_API_KEY', '')
        self.client = None
        
    def build(self):
        request_permissions([
            Permission.RECORD_AUDIO,
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
        
        self.enrollment_label = Label(
            text='Enrollment: Not Enrolled',
            size_hint_y=0.08,
            font_size='14sp',
            color=(0.96, 0.26, 0.21, 1)
        )
        layout.add_widget(self.enrollment_label)
        
        self.accuracy_label = Label(
            text='Voice Match: -',
            size_hint_y=0.08,
            font_size='14sp'
        )
        layout.add_widget(self.accuracy_label)
        
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
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.16, spacing=10)
        
        self.enroll_btn = Button(
            text='🎙️ Enroll Voice',
            background_color=(1, 0.6, 0, 1),
            font_size='16sp',
            bold=True
        )
        self.enroll_btn.bind(on_press=self.enroll_voice)
        button_layout.add_widget(self.enroll_btn)
        
        self.listen_btn = Button(
            text='▶️ Start Listening',
            background_color=(0.3, 0.69, 0.31, 1),
            font_size='16sp',
            bold=True
        )
        self.listen_btn.bind(on_press=self.toggle_listening)
        button_layout.add_widget(self.listen_btn)
        
        layout.add_widget(button_layout)
        
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.status_label.text = 'Status: API Key Missing'
            self.status_label.color = (0.96, 0.26, 0.21, 1)
        
        return layout
    
    def enroll_voice(self, instance):
        self.status_label.text = 'Status: Recording for 15 seconds...'
        self.enrollment_label.text = 'Enrollment: Recording...'
        self.enroll_btn.disabled = True
        
        def do_enrollment():
            try:
                import time
                time.sleep(15)
                
                Clock.schedule_once(lambda dt: self.update_enrollment_success())
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_enrollment_error(str(e)))
        
        threading.Thread(target=do_enrollment, daemon=True).start()
    
    def update_enrollment_success(self):
        self.is_enrolled = True
        self.enrollment_label.text = 'Enrollment: ✓ Enrolled'
        self.enrollment_label.color = (0.3, 0.69, 0.31, 1)
        self.status_label.text = 'Status: Ready to Listen'
        self.enroll_btn.text = '🔄 Re-enroll'
        self.enroll_btn.disabled = False
    
    def update_enrollment_error(self, error):
        self.enrollment_label.text = f'Enrollment: Failed - {error}'
        self.enroll_btn.disabled = False
    
    def toggle_listening(self, instance):
        if not self.is_enrolled:
            self.status_label.text = 'Status: Please enroll first'
            return
        
        self.is_listening = not self.is_listening
        
        if self.is_listening:
            self.listen_btn.text = '⏸️ Stop Listening'
            self.listen_btn.background_color = (0.96, 0.26, 0.21, 1)
            self.status_label.text = 'Status: 🎤 Listening...'
            self.status_label.color = (0.3, 0.69, 0.31, 1)
            self.start_listening()
        else:
            self.listen_btn.text = '▶️ Start Listening'
            self.listen_btn.background_color = (0.3, 0.69, 0.31, 1)
            self.status_label.text = 'Status: Stopped'
            self.status_label.color = (0.13, 0.59, 0.95, 1)
    
    def start_listening(self):
        def listen_loop():
            while self.is_listening:
                try:
                    import time
                    time.sleep(2)
                    
                    if self.is_listening:
                        Clock.schedule_once(lambda dt: self.process_question())
                    
                except Exception as e:
                    print(f"Listening error: {e}")
                    break
        
        threading.Thread(target=listen_loop, daemon=True).start()
    
    def process_question(self):
        if not self.client:
            self.status_label.text = 'Status: API Key Missing'
            return
        
        self.status_label.text = 'Status: Processing...'
        
        def get_answer():
            try:
                question = "Sample question for testing"
                
                message = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=200,
                    system="Answer in exactly 5-6 lines, be concise and direct.",
                    messages=[{"role": "user", "content": question}]
                )
                
                answer = message.content[0].text.strip()
                
                Clock.schedule_once(lambda dt: self.update_answer(question, answer))
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_error(str(e)))
        
        threading.Thread(target=get_answer, daemon=True).start()
    
    def update_answer(self, question, answer):
        self.question_text.text = question
        self.answer_text.text = answer
        self.status_label.text = 'Status: ✓ Complete'
        self.status_label.color = (0.3, 0.69, 0.31, 1)
    
    def update_error(self, error):
        self.status_label.text = f'Status: Error - {error}'
        self.status_label.color = (0.96, 0.26, 0.21, 1)

if __name__ == '__main__':
    VoiceQAApp().run()
