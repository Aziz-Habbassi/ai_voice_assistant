import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from playsound import playsound
import tempfile
import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm=OllamaLLM(model="llama3.1:8b")
if "chat_history" not in st.session_state:
    st.session_state.chat_history=ChatMessageHistory()


recognizer=sr.Recognizer()
#You can chose eather pyttsx3 or gtts for speaking
# def speak(text):
#     engine=pyttsx3.init()
#     engine.setProperty("rate",170)
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)
#     engine.say(text)
#     engine.runAndWait()
def speak(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name
    # Generate speech
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    # Play automatically
    playsound(filename)

def listen(listen_placeholder):
    
    with sr.Microphone() as source:
        listen_placeholder.write("\nListening...")
        recognizer.adjust_for_ambient_noise(source=source)
        audio=recognizer.listen(source=source)
    listen_placeholder.empty()
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
listen_placeholder = st.empty()
st.title("🤖Hi! I am your Ai assistant. How can I help you today ?")
if st.button("Start Listening..."):
    query=listen(listen_placeholder=listen_placeholder)
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