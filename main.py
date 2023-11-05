from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
import pyttsx3

driver = webdriver.Chrome()
driver.maximize_window()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+10)
engine.setProperty('voice', voices[1].id)
recognizer=sr.Recognizer()
microphone=sr.Microphone()

def speak (query):
    engine.say(query)
    engine.runAndWait()

def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    respose=""
    speak("Identifying speech..")
    try:
        response=recognizer.recognize_google(audio)
    except:
        response ="Error"
    return response
time.sleep (1)
speak ("Hello User! I am now online..")
while True:
    speak("How can I help you?")
    voice= recognize_speech ().lower()
    print(voice)
    if 'open google' in voice:
        speak ('Opening google..')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://google.com')
    elif 'search google' in voice:
        while True:
            speak('What do you want to search on google...')
            query=recognize_speech()
            if query!='Error':
                break
        element = driver.find_element("name","q")
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    if 'open youtube' in voice:
        speak ('Opening youtube..')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://youtube.com')
    elif 'search youtube' in voice:
        while True:
            speak('What do you want to search on Youtube...')
            query=recognize_speech()
            speak(f'searching {query} on youtube')
            if query!='Error':
                break
        element = driver.find_element("name","search_query")
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'switch tab' in voice:
        num_tabs=len(driver.window_handles)
        cur_tab=0
        for i in range(num_tabs):
            if driver.window_handles[i]==driver.current_window_handle:
                if i !=num_tabs-1:
                    cur_tab=i+1
                    break
        driver.switch_to_window(driver.window_handles[cur_tab])
    elif 'close tab' in voice:
        speak('closing current Tab...')
        driver.close()
    elif 'go back' in voice:
        speak('Going Back')
        driver.back()
    elif 'go forward' in voice:
        speak('Going forward')
        driver.forward()
    elif 'exit' in voice:
        speak('exiting, Goodbye...')
        driver.quit()
        break
    else:
        speak('sorry thats not a valid command')
    time.sleep(1)

