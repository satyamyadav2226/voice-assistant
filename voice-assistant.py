import speech_recognition as sr
import pyttsx3
import requests
import datetime

engine = pyttsx3.init()
engine.say("Hello! I'm your personal assistant. How can I help you today?")
engine.runAndWait()

def calculate(expression):
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}."
    except Exception as e:
        return "Sorry, I couldn't calculate that."
    
while True:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-US").lower()
            print("You:", text)
        except sr.UnknownValueError:
            print("Assistant: Sorry, I did not understand.")
            engine.say("Sorry, I did not understand.")
            engine.runAndWait()
            continue
        
        if "weather" in text:
            city = "mumbai"
            api_key = "e8db3855a317bb437b89b8a836e128a7"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                message = f"The weather in {city} is {weather} with a temperature of {temp}°C."
                print("Assistant:", message)
                engine.say(message)
            else:
                print("Assistant: Sorry, I could not fetch the weather.")
                engine.say("Sorry, I could not fetch the weather.")
            engine.runAndWait()

        elif "news" in text:
            api_key_news = "d12b75af8a8d4062b9d0a9434e454b57"
            url_news = f"https://newsapi.org/v2/top-headlines?country=us&apikey={api_key_news}"
            response = requests.get(url_news)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                headlines = [article['title'] for article in articles[:5]]
                print("Assistant: Here are the top 5 news headlines:")
                for i, headline in enumerate(headlines, 1):
                    print(f"{i}. {headline}")
                engine.say("Here are the top 5 news headlines: " + ", ".join(headlines))
            else:
                print("Assistant: Sorry, I could not fetch the news.")
                engine.say("Sorry, I could not fetch the news.")
            engine.runAndWait()

        elif "time" in text:
            time = datetime.datetime.now().strftime("%I:%M %p")
            message = f"The current time is {time}."
            print("Assistant:", message)
            engine.say(message)
            engine.runAndWait()

        elif "calculate" in text:
            engine.say("Please say the calculation.")
            engine.runAndWait()
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    calculation = recognizer.recognize_google(audio, language="en-US").lower()
                    print("You:", calculation)
                    result = calculate(calculation)
                    print("Assistant:", result)
                    engine.say(result)
                except sr.UnknownValueError:
                    print("Assistant: Sorry, I did not understand the calculation.")
                    engine.say("Sorry, I did not understand the calculation.")
                engine.runAndWait()    

        elif text in ["exit", "quit"]:
            print("Assistant: Goodbye!")
            engine.say("Goodbye!")
            engine.runAndWait()
            break

        else:
            print("Assistant: I'm sorry, I can't help with that.")
            engine.say("I'm sorry, I can't help with that.")
            engine.runAndWait()
