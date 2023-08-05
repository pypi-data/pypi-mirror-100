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


class Virus():
    """
    This is the class Virus. Pretty basic stuff.
    """
    def open_website(self, duration:float):
        t = 0
        duration = duration*60
        while t <= duration:
            webbrowser.open(random.choice(sites))
            time.sleep(1)
            t += 1
