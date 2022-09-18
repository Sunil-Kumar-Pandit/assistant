import speech_recognition as sr
import os
from selenium import webdriver
import playsound
import wolframalpha
from gtts import gTTS
import json
from urllib.request import Request, urlopen
import urllib.error
import xml.etree.ElementTree as xml
num = 1


def a_s(out):
    global num
    if num == 1:

        print("Welcome sir. Hello, I am sky.")
        sp = gTTS(text="Welcome sir. Hello, I am sky.", lang="en", slow=False)
        sp.save("sky.mp3")
        playsound.playsound("sky.mp3", True)
        os.remove("sky.mp3")

    num += 1
    print("SKY:", out)
    tospeak = gTTS(text=out, lang='en', slow=False)
    file = str(num)+".mp3"
    tospeak.save(file)
    playsound.playsound(file, True)
    os.remove(file)


def g_a():
    robj = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print('Speak')
        audio = robj.listen(source, phrase_time_limit=5)
    print('stop')
    try:
        text = robj.recognize_google(audio, language='en')
        print("you:", text)
        return text
    except:
        a_s("Could not understand your audio")
        g_a()


def work(t):
    if "news" in t:
        try:
            req = Request(
                url='https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms',
                headers={'User-Agent': 'Mozilla/5.0'}
             )
    # rep=req.urlopen("https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms")
            webpage = urlopen(req)
    # print(webpage)
            data = webpage.read().decode()
            root = xml.fromstring(data)

    # print(data)
        except urllib.error.HTTPError as err:
            print(err.code)
        if(data):
            channel=root[0]
            item=channel.findall("item")
            for i in item:
                a_s(i[0].text)

    elif "weather" in t:
        a_s("Which city weather you have to check")
        city = g_a()
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + \
            str(city)+"&appid=32d1506930537b89840d7ea88e95bcfb"
        rep = req.urlopen(url).read().decode()
        weat = json.loads(rep)
        temp = weat["main"]["temp"]-273.15
        temp = round(temp, 2)
        a_s("City "+weat["name"])
        a_s("main weather "+weat["weather"][0]["main"])
        a_s("Temprature "+str(temp))
        a_s("Humidity "+str(weat["main"]["humidity"]))
    elif "i love you" in t:
        a_s("I love you too sir")
    elif "file" in t:
        location = input(a_s("Enter the location of file:"))
        a_s("In which mode read, write,delete or remove")
        mode = str(g_a())
        if "read" in mode:

            file = open(location).read()
            a_s(file)
        elif "write" in mode:
            file = open(location, "w+")
            text = str(g_a())
            file.write(text)
            file.close()
        elif "delete" in mode or "remove" in mode:
            re = a_s("you have to delete this file say yes or no")
            if "yes" in re:
                os.remove(location)
                a_s("File is deleted")
            else:
                a_s("ok file is not deleted")
        else:
            a_s("File does not found error 404")


if __name__ == "__main__":
    a_s("What is your name ,sir")

    name = g_a()
    a_s("Hello,"+str(name)+".")
    while (1):
        a_s("What can i do for you")
        text = g_a().lower()
        if text == 0:
            continue
        elif "exit" in str(text) or "bye" in str(text) or 'sleep' in str(text):
            a_s("okay bye "+name+".")
            break
        elif text != '':
            work(str(text))
        else:
            a_s("Sorry,I am not able to underderstand what you said")
            break
