import whisper
import pyaudio
import numpy as np
import torch
import time
import smtplib
import pygame
import tempfile
import wave
import os

# 🔊 Audio & Alert Settings
SIREN_PATH = os.path.abspath("../my-app/assets/siren.mp3")   # Ensure siren.mp3 is in the same directory
EMAIL_ADDRESS = "rahulrengan4098@gmail.com"
EMAIL_PASSWORD = "wghdcoatxbrpqqem"

# Emergency contacts (for SMS alerts via email)
emergency_contacts = [
    "5104748042@vtext.com",  # Verizon Example
    "1234567890@txt.att.net"  # AT&T Example
]

# 🎤 Whisper Model Load
model = whisper.load_model("base")  # Corrected reference

# 🎙️ Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper works best at 16kHz
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 3  # Length of each snippet

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Initialize Pygame for Audio
pygame.mixer.init()

print("Listening for 'Help'...")

def send_sms_via_email(message):
    """Send an SMS alert via email."""
    try:
        print(f"Attempting to send SMS: {message}")  # Debug: Print message before sending
        message = message.encode("ascii", "ignore").decode()  # Remove non-ASCII characters

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            print("Connecting to SMTP server...")  # Debug: Check connection start
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("Logged into email server")  # Debug: Ensure login success

            for contact in emergency_contacts:
                print(f"📨 Sending SMS to {contact}")  # Debug: Show recipient
                server.sendmail(EMAIL_ADDRESS, contact, message)

        print("Emergency SMS sent successfully!")
    except Exception as e:
        print(f"⚠️ Failed to send SMS: {e}")  # Debug: Show the exact error


def play_siren():
    try:
        print("🔊 Playing siren!")
        sound = pygame.mixer.Sound(SIREN_PATH)
        sound.play()
    except Exception as e:
        print(f"Error playing siren: {e}")

# 🏃‍♂️ Real-Time Whisper Audio Detection
def detect_help():
    while True:
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        # Convert audio and transcribe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            with wave.open(temp_wav.name, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))

            print("🎙️ Processing audio...")
            result = model.transcribe(temp_wav.name)

        text = result["text"].strip().lower()
        print(f"Recognized: {text}")

        yield text 

        text = result["text"].strip().lower()
        print(f"Recognized: {text}")

        if "help" in text:
            print("HELP I AM IN DANGER")
            send_sms_via_email("HELP! Emergency detected!") 
            play_siren()
            time.sleep(5)

try:
    detect_help()
except KeyboardInterrupt:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
