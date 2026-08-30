import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform

# ==========================================
# 1. ADMOB CONFIGURATION (APNI REAL IDs REPLACE KAREIN)
# ==========================================
# Android Logo wali ID (~ symbol)
ADMOB_APP_ID = "ca-app-pub-7837258792747147~6152837151" 

# Interstitial Logo wali ID (/ symbol)
ADMOB_INTERSTITIAL_ID = "ca-app-pub-7837258792747147/3899525554" 


# ==========================================
# 2. ADMANAGER CLASS (FOR ANDROID ADS)
# ==========================================
class AdManager:
    def __init__(self, app_id, interstitial_id):
        self.app_id = app_id
        self.interstitial_id = interstitial_id
        self.kw = None
        
        if platform == 'android':
            try:
                from kivmob import KivMob
                self.kw = KivMob(self.app_id)
                self.kw.new_interstitial(self.interstitial_id)
                self.kw.request_interstitial()
                print("AdMob successfully initialized!")
            except Exception as e:
                print(f"AdMob Init Exception: {e}")

    def show_interstitial_ad(self):
        if platform == 'android' and self.kw:
            try:
                if self.kw.is_interstitial_loaded():
                    self.kw.show_interstitial()
                    # Agli ad ke liye pre-request
                    self.kw.request_interstitial()
                else:
                    self.kw.request_interstitial()
            except Exception as e:
                print(f"Error showing ad: {e}")


# ==========================================
# 3. MAIN QUIZ APP LOGIC
# ==========================================
class QuizNovaApp(App):
    def build(self):
        self.title = "QuizNova"
        
        # AdManager instance
        self.ad_manager = AdManager(ADMOB_APP_ID, ADMOB_INTERSTITIAL_ID)
        
        # Quiz state variables
        self.current_level = 1
        self.total_levels = 21
        self.current_question_idx = 0
        self.questions_answered = 0
        self.timer_seconds = 5
        self.timer_event = None
        
        # Mock questions generation (21 levels x 500 questions context)
        self.questions = self.load_sample_questions()

        # UI Layout Setup
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header Info (Level & Timer)
        self.info_label = Label(
            text=f"Level: {self.current_level}/{self.total_levels} | Timer: 5s",
            font_size='20sp',
            size_hint_y=0.1,
            color=(1, 0.8, 0, 1)
        )
        self.layout.add_widget(self.info_label)

        # Question Text Label
        self.question_label = Label(
            text="",
            font_size='22sp',
            size_hint_y=0.3,
            halign='center',
            valign='middle'
        )
        self.question_label.bind(size=self.question_label.setter('text_size'))
        self.layout.add_widget(self.question_label)

        # Option Buttons (4 Options)
        self.option_buttons = []
        for i in range(4):
            btn = Button(
                text="",
                font_size='18sp',
                size_hint_y=0.12,
                background_normal='',
                background_color=(0.2, 0.4, 0.8, 1)
            )
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            self.layout.add_widget(btn)

        # Display first question
        self.display_question()
        return self.layout

    def load_sample_questions(self):
        # Sample quiz structure
        return [
            {
                "question": "What is the capital of France?",
                "options": ["Berlin", "Madrid", "Paris", "Rome"],
                "answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "answer": "Mars"
            },
            {
                "question": "What is 5 + 7?",
                "options": ["10", "11", "12", "13"],
                "answer": "12"
            },
            {
                "question": "Which element has chemical symbol 'O'?",
                "options": ["Gold", "Oxygen", "Osmium", "Silver"],
                "answer": "Oxygen"
            }
        ]

    def display_question(self):
        # Reset colors and timer
        self.reset_button_colors()
        self.timer_seconds = 5
        self.update_header()

        q_data = self.questions[self.current_question_idx]
        self.question_label.text = q_data["question"]
        
        for i, option in enumerate(q_data["options"]):
            self.option_buttons[i].text = option
            self.option_buttons[i].disabled = False

        # Start 5 second timer
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer_seconds -= 1
        self.update_header()
        
        if self.timer_seconds <= 0:
            self.timer_event.cancel()
            self.highlight_correct_answer()
            Clock.schedule_once(self.next_question, 1.5)

    def update_header(self):
        self.info_label.text = f"Level: {self.current_level} | Time Left: {self.timer_seconds}s"

    def check_answer(self, instance):
        if self.timer_event:
            self.timer_event.cancel()

        for btn in self.option_buttons:
            btn.disabled = True

        q_data = self.questions[self.current_question_idx]
        correct_ans = q_data["answer"]

        if instance.text == correct_ans:
            instance.background_color = (0, 1, 0, 1)  # Green for Correct
        else:
            instance.background_color = (1, 0, 0, 1)  # Red for Wrong
            self.highlight_correct_answer()

        Clock.schedule_once(self.next_question, 1.5)

    def highlight_correct_answer(self):
        q_data = self.questions[self.current_question_idx]
        for btn in self.option_buttons:
            if btn.text == q_data["answer"]:
                btn.background_color = (0, 1, 0, 1)

    def reset_button_colors(self):
        for btn in self.option_buttons:
            btn.background_color = (0.2, 0.4, 0.8, 1)

    def next_question(self, dt):
        self.current_question_idx = (self.current_question_idx + 1) % len(self.questions)
        self.questions_answered += 1

        # EVERY 3 QUESTIONS: TRIGGER ADMOB INTERSTITIAL AD
        if self.questions_answered % 3 == 0:
            self.ad_manager.show_interstitial_ad()

        self.display_question()


if __name__ == '__main__':
    QuizNovaApp().run()