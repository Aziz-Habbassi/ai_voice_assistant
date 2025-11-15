import speech_recognition as sr
import pyttsx3
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm=OllamaLLM(model="llama3.1:8b")
chat_history=ChatMessageHistory()


recognizer=sr.Recognizer()

def speak(text):
    engine=pyttsx3.init()
    engine.setProperty("rate",170)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source=source)
        audio=recognizer.listen(source=source)
    try:
        query=recognizer.recognize_google(audio_data=audio)
        print(f"\nYou said : {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't Understant. try again !")
        return ""
    except sr.RequestError:
        print("Speech Recognize Service Unavalible for now")
        return ""

prompt=PromptTemplate(input_variables=["chat_history","question"],template="Previous conversation: {chat_history}\nUser: {question}\nAI:")

def run_chain(question):
    chat_history_text="\n".join([f"{msg.type.capitalize()} : {msg.content}"for msg in chat_history.messages])
    response=llm.invoke(prompt.format(chat_history=chat_history_text,question=question))

    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)

    return response

speak("Hi! I am your Ai assistant. How can I help you today ?")
while True:
    query=listen()
    if "exit" in query or "stop" in query:
        print("\nAi: Have a good Day, GoodBye !")
        speak("Have a good Day, GoodBye !")
        break
    if query :
        response=run_chain(question=query)
        print(f"\n Ai: {response}")
        speak(response)
    if not query:
        continue