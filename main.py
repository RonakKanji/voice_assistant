import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes

CONTACTS = {
    
}
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def take_command(source):
    print('Listening...')
    voice = listener.listen(source)
    print('Listened')
    command = listener.recognize_google(voice).lower()
    print(command)
    return command


def greeting():
    time = datetime.datetime.now().time().hour
    if time <= 6 or time >= 21:
        talk('Hello sir')
    elif time <= 12:
        print('Good morning sir')
    elif time <= 16:
        print('Good day sir')
    elif time <= 21:
        print('Good evening sir')


def run_command():
    try:
        is_off = False
        with sr.Microphone() as source:
            while not is_off:
                command = take_command(source)

                if 'alexa' in command:
                    greeting()
                    command = command.replace('alexa', '')

                    if 'play' in command:
                        song = command.replace('play', '')
                        talk(f'playing {song}')
                        pywhatkit.playonyt(song)

                    elif 'time' in command:
                        time = datetime.datetime.now().strftime('%I:%M %p')
                        talk('Current time is ' + time)

                    elif 'joke' in command:
                        talk(pyjokes.get_joke())

                    elif 'turn off' in command:
                        talk('Goodbye')
                        is_off = True

                    elif 'message' or 'whatsapp' in command:
                        talk('Who do you want to send it to?')
                        name = take_command(source)
                        talk('What is your message?')
                        msg = take_command(source)
                        talk('When do you want me to send the message?')
                        time = take_command(source)

                        for key in CONTACTS:
                            if key == name:
                                if 'now' in time:
                                    talk('sending message' + msg + ' to ' + name + 'now')
                                    pywhatkit.sendwhatmsg(CONTACTS[key], msg,
                                                          int(datetime.datetime.now().strftime('%H')),
                                                          int(datetime.datetime.now().strftime('%M')) + 1)
                                else:
                                    time_list = list(time)

                    else:
                        talk('I did not understand what you said')
    except:
        talk('There seemed to be a problem, try again')
        run_command()
        pass


run_command()
