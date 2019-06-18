import speech_recognition as sr
from google_speech import Speech
import time
import sys
import os
from time import sleep
import pyttsx3
#from response import *
from fuzzywuzzy import fuzz
import datetime

opts = {
    "alias": ('джесси', 'джесс'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'которыЙ час'),
        "you": ('имя', 'как тебя зовут'),
    }
}

#Functions
def speak(what):
    speak_engine = pyttsx3.init()
    print( what )
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print('[log] Распознано: ' + voice)

        if(voice.startswith(opts["alias"])):
            #Say to Jassy
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            #Response command and execute it
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print('[log] Голос не распознан!')
    except sr.RequestError:
        print('[log] Неизвестная ошибка, проверьте интернет соединение')

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC

def execute_cmd(cmd):
    if(cmd == 'ctime'):
        #Say what time is now
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ':' + str(now.minute))
    elif(cmd == 'you'):
        speak('Меня зовут Джесси')

    else:
        speak('Команда не распознана повторите')



def program():
    #Start
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    with m as source:
        r.adjust_for_ambient_noise(source)

    speak_engine = pyttsx3.init()

    voices = speak_engine.getProperty('voices')
    speak_engine.setProperty('voice', voices[0].id)

    speak('Добрый день, хозяин')
    speak('Джесси слушает')
    stop_listening = r.listen_in_background(m, callback)
    while True:
        time.sleep(0.1) #infinity loop

if __name__ == '__main__':
    while True:
        program()