# 🎤 Voice Chat with Ollama Agent

Talk to your local AI agent using voice! This wrapper adds speech-to-text (STT) and text-to-speech (TTS) capabilities to your Ollama agent.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install voice libraries
pip install SpeechRecognition pyttsx3 pyaudio

# On Mac, if pyaudio fails, use homebrew:
brew install portaudio
pip install pyaudio

# On Linux:
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

# Reinstall the package to get the new entry point
cd /Users/nasheikh/Desktop/personal/python/scrappers
pip install -e .
```

### 2. Start Voice Chat

```bash
agent-voice
```

That's it! The agent will greet you and start listening.

---

## 🎙️ How to Use

### Basic Usage

1. **Start the app**: `agent-voice`
2. **Wait for "🎤 Listening..."**
3. **Speak your question** clearly
4. **Wait for the response** - it will be spoken back to you!

### Voice Commands

- **Normal questions**: "What is Python?", "Tell me about machine learning"
- **Search requests**: "Search for latest AI news"
- **Exit**: Say "exit", "quit", or "goodbye"
- **Clear conversation**: Say "clear" to reset the conversation history

### Example Conversation

```
🤖 Agent: Hello! I'm your voice assistant. How can I help you today?

You: "What is Python?"
🤖 Agent: Python is a high-level programming language known for its simplicity...

You: "Who created it?"
🤖 Agent: Python was created by Guido van Rossum and released in 1991...

You: "Goodbye"
🤖 Agent: Goodbye! Have a great day!
```

---

## ⚙️ Configuration Options

### Command Line Arguments

```bash
# Use a different model
agent-voice --model llama3.1:8b

# Disable tools for faster responses
agent-voice --no-tools

# Adjust speech rate (words per minute)
agent-voice --rate 150  # Slower
agent-voice --rate 200  # Faster

# Adjust volume (0.0 to 1.0)
agent-voice --volume 0.7  # Quieter
agent-voice --volume 1.0  # Max volume

# Use different language for speech recognition
agent-voice --language es-ES  # Spanish
agent-voice --language fr-FR  # French
```

### Full Options

```bash
agent-voice --help

Options:
  --model MODEL          Ollama model to use (default: llama3.1:8b)
  --no-tools             Disable all tools (faster responses)
  --language LANGUAGE    Speech recognition language (default: en-US)
  --rate RATE           Speech rate in words per minute (default: 175)
  --volume VOLUME       Speech volume 0.0-1.0 (default: 0.9)
```

---

## 🎛️ How It Works

### Architecture

```
┌─────────────┐
│ Microphone  │
└──────┬──────┘
       │ Audio
       ▼
┌─────────────────────────┐
│ SpeechRecognition       │  (Google Speech API)
│ Audio → Text            │
└──────┬──────────────────┘
       │ Text
       ▼
┌─────────────────────────┐
│ Ollama Agent            │  (Your local LLM)
│ Text → Response         │
└──────┬──────────────────┘
       │ Response Text
       ▼
┌─────────────────────────┐
│ pyttsx3 (TTS)           │  (Offline text-to-speech)
│ Text → Audio            │
└──────┬──────────────────┘
       │ Audio
       ▼
┌─────────────┐
│  Speaker    │
└─────────────┘
```

### Technologies Used

1. **SpeechRecognition** - Captures audio and converts to text
   - Uses Google Speech Recognition API (requires internet)
   - Automatically adjusts for ambient noise
   - Supports multiple languages

2. **pyttsx3** - Converts text to speech
   - Works offline (no API required)
   - Cross-platform (Mac, Linux, Windows)
   - Adjustable voice, rate, and volume

3. **Your Ollama Agent** - Processes the conversation
   - Uses your existing agent with tools
   - Optimized for voice (shorter, conversational responses)

---

## 🔧 Troubleshooting

### "No module named 'speech_recognition'"

```bash
pip install SpeechRecognition
```

### "No module named 'pyttsx3'"

```bash
pip install pyttsx3
```

### pyaudio Installation Fails

**On Mac**:
```bash
brew install portaudio
pip install pyaudio
```

**On Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**On Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

### "No speech detected"

- Check your microphone permissions
- Speak louder or closer to the mic
- Reduce background noise
- Check system audio settings

### "Could not understand audio"

- Speak more clearly
- Reduce background noise
- Check microphone quality
- Try adjusting `energy_threshold` in the code

### Speech Recognition Fails (No Internet)

The default speech recognition uses Google's API and requires internet. For offline recognition, you can modify the code to use:

```python
# In voice_chat.py, replace recognize_google with:
text = self.recognizer.recognize_sphinx(audio)  # Offline but less accurate
```

Install dependencies:
```bash
pip install pocketsphinx
```

### TTS Sounds Robotic

Try adjusting the voice:
```bash
agent-voice --rate 150  # Slower = more natural
```

Or modify the code to use a different voice engine (see "Advanced Customization" below).

---

## 🎨 Advanced Customization

### Change TTS Voice

Edit `voice_chat.py`:

```python
# List available voices
voices = self.tts_engine.getProperty('voices')
for voice in voices:
    print(f"Voice: {voice.name} (ID: {voice.id})")

# Set a specific voice
self.tts_engine.setProperty('voice', voices[0].id)  # Use first voice
```

### Use Google Text-to-Speech (gTTS)

For better quality (requires internet):

```bash
pip install gtts playsound
```

Modify `speak()` method:
```python
from gtts import gTTS
from playsound import playsound
import tempfile

def speak(self, text: str):
    tts = gTTS(text=text, lang='en', slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        playsound(fp.name)
```

### Adjust Microphone Sensitivity

In `voice_chat.py`:

```python
# Make more sensitive (picks up quieter sounds)
self.recognizer.energy_threshold = 2000

# Make less sensitive (ignores background noise)
self.recognizer.energy_threshold = 6000
```

### Support Multiple Languages

```bash
# Spanish
agent-voice --language es-ES

# French
agent-voice --language fr-FR

# German
agent-voice --language de-DE

# Japanese
agent-voice --language ja-JP
```

---

## 📊 Performance Tips

### Faster Responses

```bash
# Disable tools
agent-voice --no-tools

# Use faster model (if available)
agent-voice --model phi3:mini

# Reduce max iterations in code
agent = Agent(..., max_iterations=2)
```

### Better Quality

```bash
# Use better model
agent-voice --model llama3.1:70b

# Slower, more natural speech
agent-voice --rate 150
```

---

## 🔐 Privacy Notes

- **Speech Recognition**: Uses Google's API by default (audio sent to Google)
- **TTS**: Uses pyttsx3 which is completely offline
- **Ollama**: Runs locally, no data sent to external servers

For **completely offline** operation:
- Use `recognize_sphinx()` for speech recognition (less accurate)
- pyttsx3 is already offline
- Ollama is already local

---

## 🎯 Use Cases

### 1. Hands-Free Assistance
```bash
agent-voice
# While cooking, ask: "Convert 2 cups to milliliters"
```

### 2. Voice-Controlled Search
```bash
agent-voice
# Say: "Search for Python web scraping tutorials"
```

### 3. Learning / Practice
```bash
agent-voice
# Practice language or interview questions
```

### 4. Accessibility
```bash
agent-voice
# For users who prefer or require voice interaction
```

---

## 📝 Python API Usage

You can also use the VoiceChat class directly:

```python
from voice_chat import VoiceChat
from local_llm.agent import Agent
from tools import get_default_tools

# Create agent
agent = Agent(tools=get_default_tools())

# Create voice interface
voice = VoiceChat(agent=agent)

# Start listening
voice.chat_loop()

# Or use individual methods
text = voice.listen()  # Get speech input
if text:
    response = agent.chat(text)
    voice.speak(response)  # Speak the response
```

---

## 🚧 Known Limitations

1. **Internet Required**: Default speech recognition needs internet
2. **Voice Quality**: pyttsx3 voices can sound robotic (use gTTS for better quality)
3. **Latency**: ~2-5 seconds between speech and response (depends on model)
4. **Background Noise**: May affect recognition accuracy
5. **Continuous Speech**: Doesn't support interruption (must wait for response to finish)

---

## 🔄 Comparison: Text vs Voice Chat

| Feature | agent-chat | agent-voice |
|---------|-----------|-------------|
| Input | Keyboard | Microphone |
| Output | Text | Speech + Text |
| Speed | Fast | Slower (STT + TTS overhead) |
| Internet | Optional | Required (for STT) |
| Best For | Complex queries, coding | Hands-free, quick questions |
| Response Length | Detailed | Concise (optimized for voice) |

---

## 🎉 Next Steps

1. **Test basic voice interaction**:
   ```bash
   agent-voice
   # Say: "Hello, what can you do?"
   ```

2. **Try voice search**:
   ```bash
   agent-voice
   # Say: "Search for Python tutorials"
   ```

3. **Customize for your needs**:
   - Adjust speech rate
   - Change voice
   - Add custom tools

4. **Build voice-first applications**:
   - Voice-controlled home automation
   - Hands-free research assistant
   - Accessibility tools

---

## 📚 Additional Resources

- [SpeechRecognition Docs](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 Docs](https://pypi.org/project/pyttsx3/)
- [Ollama Models](https://ollama.ai/library)

---

**Happy voice chatting! 🎤🤖**
