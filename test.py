import pyttsx3
import random

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.say('Is this going at the right speed for a Youtube video?')
engine.runAndWait()


