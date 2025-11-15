# **AI Voice Assistant (Python + LangChain + Ollama)**

A simple locally-running **voice-controlled AI assistant** built using:

-   **SpeechRecognition** → to capture and transcribe voice\
-   **pyttsx3** → for offline text-to-speech\
-   **LangChain** → for prompt management & conversation memory\
-   **Ollama** → to run a local LLM (Llama 3.1:8B in this project)\
-   **Streamlit WebUI** → a simple optional web interface to interact
    with the assistant

This assistant listens to your voice, processes the query with a local
LLM, speaks the answer back, and also provides a lightweight **web
interface** for text-based interactions.

------------------------------------------------------------------------

## **🚀 Features**

-   🎤 **Voice input** using your microphone\
-   🧠 **Local LLM** processing (fully offline)\
-   💬 **Conversation memory** using LangChain's `ChatMessageHistory`\
-   🔊 **Natural voice responses** with pyttsx3\
-   🌐 **Simple Streamlit WebUI** for browser-based chat\
-   🛑 **Voice command exit** ("exit" or "stop")

------------------------------------------------------------------------

## **📦 Requirements**

### **Python Libraries**

``` bash
pip install speechrecognition pyttsx3 langchain langchain-community langchain-core langchain-ollama streamlit
pip install pyaudio
```

### **Ollama**

Download Ollama:\
https://ollama.com/download

Pull the model:

``` bash
ollama pull llama3.1:8b
```

------------------------------------------------------------------------

## **📁 Project Structure**

    ai_voice_assistant.py      # Main voice assistant script
    webui.py                   # Simple Streamlit Web UI (optional)
    README.md                  # Project documentation

------------------------------------------------------------------------

## **▶️ Run the Voice Assistant**

``` bash
python ai_voice_assistant.py
```

------------------------------------------------------------------------

## **🌐 Run the Web UI**

``` bash
streamlit run webui.py
```

Then open the link shown in your terminal.

------------------------------------------------------------------------

## **🧠 How It Works**

### 1. Voice Input

Captured with `speech_recognition` and converted to text.

### 2. LLM Processing

`OllamaLLM(model="llama3.1:8b")` processes the query using a custom
prompt template.

### 3. Memory

Conversation history stored with `ChatMessageHistory()`.

### 4. Voice Output

Responses spoken with `pyttsx3`.

### 5. Streamlit Web UI

A lightweight interface where you can type messages instead of speaking.

------------------------------------------------------------------------

## **📜 License**

Free to modify and use for learning or personal projects.
