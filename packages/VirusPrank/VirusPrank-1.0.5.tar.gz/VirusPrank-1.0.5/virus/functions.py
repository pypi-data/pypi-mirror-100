"""
Module that contains the main functions for opening the websites
"""
import webbrowser
import time
import random

sites = [
    'https://web.whatsapp.com',
    'https://primevideo.com',
    'https://amazon.com','https://discord.com',
    'https://instagram.com','https://github.com',
    'https://google.com',
    'https://youtube.com',
    'https://facebook.com',
    'https://netflix.com',
    'https://gmail.com',
    'https://docs.google.com'
]


class Virus:
    def open_website(self, duration):
        t = 0
        while t <= duration:
            webbrowser.open(random.choice(sites))
            time.sleep(1)
            t += 1

    def start(self, duration = 10): #Default site type is 'sfw' and duration is 10 minutes
        open_website(duration*60)
