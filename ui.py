import tkinter as tk
from tkinter import scrolledtext
import threading
import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent
from voice.text_to_speech import speak
from voice.speech_to_text import listen, calibrate_microphone

# ============================================================
# ZUNO UI
# ============================================================

class ZunoUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zuno — AI Personal Assistant")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.running = True
        self.voice_enabled = True
        self.creative_mode = False
        self.is_listening = False  # Tracks continuous listening state
        
        self.runner = InMemoryRunner(agent=root_agent)
        self.user_id = "ui_user"
        self.session = None

        self.setup_ui()
        threading.Thread(target=self.initialize_agent, daemon=True).start()

    def initialize_agent(self):
        try:
            calibrate_microphone()
            async def create_session():
                return await self.runner.session_service.create_session(
                    app_name=self.runner.app_name,
                    user_id=self.user_id,
                )
            self.session = asyncio.run(create_session())
            self.root.after(0, self.agent_ready)
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Could not initialize Zuno:\n\n{e}"))

    def agent_ready(self):
        self.status_label.config(text="ONLINE")
        self.status_dot.config(fg="#35d07f")
        self.bottom_status.config(text="● Zuno ready", fg="#35d07f")
        self.assistant_text.config(text="Ready to help.")
        self.add_activity("Zuno agent connected")

    def setup_ui(self):
        self.root.configure(bg="#0f1117")

        top = tk.Frame(self.root, bg="#151821", height=75)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="ZUNO", font=("Segoe UI", 25, "bold"), fg="#ffffff", bg="#151821").pack(side="left", padx=25)
        tk.Label(top, text="AI PERSONAL ASSISTANT", font=("Segoe UI", 9), fg="#8d93a6", bg="#151821").pack(side="left")

        self.status_label = tk.Label(top, text="STARTING", font=("Segoe UI", 10, "bold"), fg="#f5b942", bg="#151821")
        self.status_label.pack(side="right")
        self.status_dot = tk.Label(top, text="●", font=("Segoe UI", 15), fg="#f5b942", bg="#151821")
        self.status_dot.pack(side="right", padx=(0, 8))

        content = tk.Frame(self.root, bg="#0f1117")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        left = tk.Frame(content, bg="#151821", width=300)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        tk.Label(left, text="ASSISTANT", font=("Segoe UI", 9, "bold"), fg="#858b9e", bg="#151821").pack(anchor="w", padx=20, pady=(20, 8))
        self.assistant_text = tk.Label(left, text="Starting Zuno...", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#151821", wraplength=250, justify="left")
        self.assistant_text.pack(anchor="w", padx=20, pady=(0, 20))

        tk.Label(left, text="MODE", font=("Segoe UI", 9, "bold"), fg="#858b9e", bg="#151821").pack(anchor="w", padx=20, pady=(10, 8))
        self.mode_label = tk.Label(left, text="●  GENERAL MODE", font=("Segoe UI", 11, "bold"), fg="#7aa7ff", bg="#151821")
        self.mode_label.pack(anchor="w", padx=20)

        self.creative_button = tk.Button(left, text="✨  CREATIVE MODE", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#252a38", activebackground="#303747", activeforeground="#ffffff", relief="flat", bd=0, padx=15, pady=12, command=self.activate_creative)
        self.creative_button.pack(fill="x", padx=20, pady=(20, 10))

        self.voice_button = tk.Button(left, text="🔊  VOICE ON", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#252a38", activebackground="#303747", activeforeground="#ffffff", relief="flat", bd=0, padx=15, pady=12, command=self.toggle_voice)
        self.voice_button.pack(fill="x", padx=20)

        tk.Label(left, text="RECENT ACTIVITY", font=("Segoe UI", 9, "bold"), fg="#858b9e", bg="#151821").pack(anchor="w", padx=20, pady=(30, 10))
        self.activity = tk.Label(left, text="• Zuno started\n• Gemini connected\n• Agent initializing...", font=("Segoe UI", 9), fg="#b5bac8", bg="#151821", justify="left")
        self.activity.pack(anchor="w", padx=20)

        right = tk.Frame(content, bg="#0f1117")
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="COMMAND", font=("Segoe UI", 9, "bold"), fg="#858b9e", bg="#0f1117").pack(anchor="w")

        command_frame = tk.Frame(right, bg="#151821")
        command_frame.pack(fill="x", pady=(8, 15))

        self.command_entry = tk.Entry(command_frame, font=("Segoe UI", 12), fg="#ffffff", bg="#151821", insertbackground="#ffffff", relief="flat", bd=0)
        self.command_entry.pack(side="left", fill="x", expand=True, padx=15, pady=14)
        self.command_entry.bind("<Return>", lambda event: self.run_command())

        send_button = tk.Button(command_frame, text="RUN", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#4c6fff", activebackground="#5d7cff", relief="flat", bd=0, padx=20, pady=10, command=self.run_command)
        send_button.pack(side="right", padx=7)

        # CONTINUOUS LISTEN TOGGLE BUTTON
        self.mic_button = tk.Button(command_frame, text="🎤 START LISTENING", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#d93838", activebackground="#ff5252", relief="flat", bd=0, padx=20, pady=10, command=self.toggle_listening)
        self.mic_button.pack(side="right", padx=7)

        tk.Label(right, text="ZUNO OUTPUT", font=("Segoe UI", 9, "bold"), fg="#858b9e", bg="#0f1117").pack(anchor="w")

        self.output = scrolledtext.ScrolledText(right, font=("Segoe UI", 11), fg="#e8eaf0", bg="#151821", insertbackground="#ffffff", relief="flat", bd=0, wrap="word", padx=20, pady=20)
        self.output.pack(fill="both", expand=True, pady=(8, 15))
        self.output.insert("end", "Zuno is ready.\n\nClick '🎤 START LISTENING' for continuous hands-free mode.")
        self.output.config(state="disabled")

        bottom = tk.Frame(right, bg="#0f1117")
        bottom.pack(fill="x")

        self.bottom_status = tk.Label(bottom, text="● Starting...", font=("Segoe UI", 9), fg="#f5b942", bg="#0f1117")
        self.bottom_status.pack(side="left")

        self.speaking_status = tk.Label(bottom, text="", font=("Segoe UI", 9), fg="#7aa7ff", bg="#0f1117")
        self.speaking_status.pack(side="right")

    # ========================================================
    # CONTINUOUS VOICE LISTENING
    # ========================================================
    
    def toggle_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.mic_button.config(bg="#d93838", text="🎤 START LISTENING")
            self.bottom_status.config(text="● Voice paused", fg="#f5b942")
            self.assistant_text.config(text="Ready.")
        else:
            self.is_listening = True
            self.mic_button.config(bg="#a12c2c", text="🛑 STOP LISTENING")
            self._start_listening_cycle()

    def _start_listening_cycle(self):
        if not self.is_listening:
            return
        self.assistant_text.config(text="Listening...")
        self.bottom_status.config(text="● Waiting for voice...", fg="#f5b942")
        threading.Thread(target=self._voice_worker, daemon=True).start()

    def _voice_worker(self):
        command = listen()
        
        if not self.is_listening:
            return
            
        if command:
            self.root.after(0, lambda: self._apply_voice_command(command))
        else:
            # If nothing was heard, instantly loop and listen again
            self.root.after(0, self._start_listening_cycle)

    def _apply_voice_command(self, command):
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, command)
        self.run_command()

    # ========================================================
    # UI HELPERS & COMMAND PROCESSING
    # ========================================================

    def write_output(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.config(state="disabled")
        self.output.see("end")

    def add_activity(self, text):
        current = self.activity.cget("text")
        lines = current.split("\n")
        lines.append(f"• {text}")
        self.activity.config(text="\n".join(lines[-6:]))

    def activate_creative(self):
        self.creative_mode = not self.creative_mode
        if self.creative_mode:
            self.mode_label.config(text="●  CREATIVE MODE", fg="#c084fc")
            self.creative_button.config(bg="#6d3db5")
        else:
            self.mode_label.config(text="●  GENERAL MODE", fg="#7aa7ff")
            self.creative_button.config(bg="#252a38")
        self.command_entry.focus()

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        if self.voice_enabled:
            self.voice_button.config(text="🔊  VOICE ON")
        else:
            self.voice_button.config(text="🔇  VOICE OFF")

    def run_command(self):
        command = self.command_entry.get().strip()
        if not command or not self.session:
            return

        self.command_entry.delete(0, "end")
        self.assistant_text.config(text="Thinking...")
        self.bottom_status.config(text="● Zuno is thinking...", fg="#7aa7ff")
        
        threading.Thread(target=self.process_command, args=(command,), daemon=True).start()

    def process_command(self, command):
        try:
            response = asyncio.run(self.ask_zuno(command))
            if not response:
                response = "I completed the request."
            
            self.root.after(0, self.show_response, response)

            # Route to TTS, or restart listening immediately if voice is muted
            if self.voice_enabled:
                threading.Thread(target=self.speak_response, args=(response,), daemon=True).start()
            else:
                if self.is_listening:
                    self.root.after(500, self._start_listening_cycle)

        except Exception as e:
            self.root.after(0, self.show_error, f"{type(e).__name__}: {e}")
            if self.is_listening:
                self.root.after(1000, self._start_listening_cycle)

    async def ask_zuno(self, command):
        content = types.Content(role="user", parts=[types.Part(text=command)])
        response_text = ""
        async for event in self.runner.run_async(user_id=self.user_id, session_id=self.session.id, new_message=content):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
        return response_text.strip()

    def speak_response(self, response):
        try:
            self.root.after(0, lambda: self.speaking_status.config(text="🔊 Zuno speaking..."))
            
            # 1. Clean out markdown
            clean_text = response.replace("*", "").replace("#", "")
            
            # 2. STRIP EMOJIS AND SPECIAL CHARACTERS that crash Windows TTS
            # This keeps only normal letters, numbers, and basic punctuation
            clean_text = "".join(c for c in clean_text if ord(c) < 128)
            
            # 3. Split the story into sentences so the voice engine doesn't choke
            sentences = clean_text.replace("!", ".").replace("?", ".").split(".")
            
            # Read it sentence by sentence
            for sentence in sentences:
                if sentence.strip():
                    speak(sentence.strip())
                    
            self.root.after(0, lambda: self.speaking_status.config(text=""))
        except Exception as e:
            self.root.after(0, lambda: self.speaking_status.config(text=f"TTS error: {e}"))
        finally:
            if self.is_listening:
                self.root.after(500, self._start_listening_cycle)

    def show_response(self, response):
        self.write_output(response)
        self.assistant_text.config(text="Done.")
        self.bottom_status.config(text="● Ready", fg="#35d07f")

    def show_error(self, error):
        self.write_output("Zuno encountered an error.\n\n" + error)
        self.bottom_status.config(text="● Error", fg="#ff6b6b")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ZunoUI()
    app.run()