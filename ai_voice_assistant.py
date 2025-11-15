import speech_recognition as sr
import pyttsx3
import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm=OllamaLLM(model="llama3.1:8b")
if "chat_history" not in st.session_state:
    st.session_state.chat_history=ChatMessageHistory()


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
        st.write("\nListening...")
        recognizer.adjust_for_ambient_noise(source=source)
        audio=recognizer.listen(source=source)
    try:
        query=recognizer.recognize_google(audio_data=audio)
        st.write(f"\nYou said : {query}")
        return query.lower()
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't Understant. try again !")
        return ""
    except sr.RequestError:
        print("Speech Recognize Service Unavalible for now")
        return ""

prompt=PromptTemplate(input_variables=["chat_history","question"],template="Previous conversation: {chat_history}\nUser: {question}\nAI:")

def run_chain(question):
    chat_history_text="\n".join([f"{msg.type.capitalize()} : {msg.content}"for msg in st.session_state.chat_history.messages])
    response=llm.invoke(prompt.format(chat_history=chat_history_text,question=question))

    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

    return response

st.title("🤖Hi! I am your Ai assistant. How can I help you today ?")
if st.button("Start Listening..."):
    query=listen()
    if "exit" in query or "stop" in query:
        st.write("\nAi: Have a good Day, GoodBye !")
        st.write("Have a good Day, GoodBye !")   
    if query :
        response=run_chain(question=query)
        st.write(f"\nUser: {query}")
        st.write(f"\nAi: {response}")
        speak(response)

st.subheader("📜Chat History")
for msg in st.session_state.chat_history.messages:
    st.write(msg.type.capitalize()+" : "+msg.content)