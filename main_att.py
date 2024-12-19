import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage
import tkinter as tk
from tkinter import filedialog
from os import path

with open(".env") as file:
    lines = file.readlines()
    SENDER_EMAIL = lines[0].split("=")[1].strip()
    SENDER_PASSWORD = lines[1].split("=")[1].strip()

print(f"Sender's Email: {SENDER_EMAIL}")

listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def get_info() -> str:
    with sr.Microphone() as source:
        print("listening...")
        voice = listener.listen(source, timeout=8)
        print("processing...")
        try:
            info: str = listener.recognize_google(voice)
            print("You said:", info)
        except sr.UnknownValueError:
            print("Could not understand audio.")
            info = ""
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )
            info = ""
    return info.lower()

def send_email(receiver, subject, message, attachments=None):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    email = EmailMessage()
    email["From"] = SENDER_EMAIL
    email["To"] = receiver
    email["subject"] = subject
    email.set_content(message)

    if attachments:
        for file in attachments:
            with open(file, "rb") as f:
                file_data = f.read()
                file_name = path.basename(f.name)
            email.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    server.send_message(email)
    server.quit()

email_list = {
    # Change this to actual name and email address
    # You can have multiple names and emails here.
    "name" : "email_address.com"
}

def get_email_info():
    talk("Who's the email for?")
    name: str = get_info()

    receiver: str = email_list.get(name)
    if not receiver:
        talk("I couldn't find the email address for that name.")
        return

    talk("What is the subject of your email?")
    subject: str = get_info()

    talk("What is the body of your email?")
    message: str = get_info()

    talk("Do you want to add any attachments?")
    add_attachments = get_info()

    attachments = []
    if "narnia" in add_attachments:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_paths = filedialog.askopenfilenames()
        attachments = list(file_paths)

    talk("Sending...")
    send_email(receiver, subject, message, attachments)

    talk("Your email is sent.")

    talk("Do you wish to send another email?")
    send_more = get_info()
    if "narnia" in send_more:
        get_email_info()
    elif "no" in send_more:
        talk("Okay, Bye.")
    else:
        talk("Please confirm either by saying 'narnia' or 'no'")

get_email_info()
