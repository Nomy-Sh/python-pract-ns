# 🎤 Voice Chat - Quick Setup

## What's Been Created

A complete **voice interface** for your Ollama agent with:
- 🎙️ **Speech-to-Text** (STT) - Talk to your agent
- 🔊 **Text-to-Speech** (TTS) - Agent talks back
- 🤖 **Full Agent Integration** - All your tools available via voice

---

## 📦 Installation Steps

### Step 1: Install System Dependencies (Mac)

```bash
# Install portaudio (required for microphone access)
brew install portaudio
```

**Don't have Homebrew?** Install it first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python Libraries

```bash
# Navigate to project
cd /Users/nasheikh/Desktop/personal/python/scrappers

# Install voice dependencies
pip install SpeechRecognition pyttsx3 pyaudio

# Reinstall package to register the voice command
pip install -e .
```

### Step 3: Test It!

```bash
agent-voice
```

You should see:
```
🚀 Initializing voice chat...
✅ Text-to-speech engine initialized
┌─────────────────────────────────────┐
│ 🎤 Voice Chat with Ollama Agent     │
│                                     │
│ Commands:                           │
│ - Speak naturally to ask questions  │
│ - Say 'exit', 'quit', or 'goodbye' │
│ - Say 'clear' to reset             │
└─────────────────────────────────────┘

🤖 Agent: Hello! I'm your voice assistant...
🎤 Listening...
```

---

## 🚀 Quick Test

1. Start voice chat:
   ```bash
   agent-voice
   ```

2. Wait for "🎤 Listening..."

3. Say: **"What is Python?"**

4. The agent will:
   - Transcribe your speech
   - Process the question
   - Speak the answer back to you!

---

## ⚙️ Common Usage

### Basic Commands

```bash
# Start with default settings
agent-voice

# Use without tools (faster)
agent-voice --no-tools

# Adjust speech speed
agent-voice --rate 150    # Slower
agent-voice --rate 200    # Faster

# Adjust volume
agent-voice --volume 0.5  # Quieter
agent-voice --volume 1.0  # Louder
```

### Voice Commands to Try

- "Hello" - Greet the assistant
- "What is Python?" - Ask general questions
- "Search for AI news" - Use web search tool
- "Clear" - Reset conversation
- "Goodbye" - Exit the chat

---

## 🔧 If Installation Fails

### PyAudio Won't Install

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Still fails?** You can try:
```bash
# Install from conda instead
conda install pyaudio
```

### No Microphone Detected

1. Check system preferences → Privacy → Microphone
2. Grant permission to Terminal/iTerm
3. Test with: `python -m speech_recognition`

### TTS Not Working

The TTS (pyttsx3) should work out of the box on Mac. If it fails:
```bash
# Try alternative TTS
pip install gtts playsound
```

Then modify the code to use Google TTS (see VOICE_CHAT_GUIDE.md).

---

## 📁 Files Created

1. **`voice_chat.py`** - Main voice chat implementation
   - VoiceChat class with listen() and speak() methods
   - Integration with your existing Agent
   - Full conversation loop

2. **`VOICE_CHAT_GUIDE.md`** - Complete documentation
   - How it works
   - Configuration options
   - Troubleshooting
   - Advanced customization

3. **`pyproject.toml`** - Updated with entry point
   - `agent-voice` command registered

---

## 🎯 Features

### Speech Recognition
- ✅ Real-time voice input
- ✅ Automatic noise adjustment
- ✅ Multi-language support (en-US, es-ES, fr-FR, etc.)
- ✅ Timeout handling
- ✅ Internet-based (Google Speech API)

### Text-to-Speech
- ✅ Offline TTS (pyttsx3)
- ✅ Adjustable voice, rate, volume
- ✅ Cross-platform (Mac, Linux, Windows)
- ✅ Natural voice selection (tries Samantha/Alex on Mac)

### Agent Integration
- ✅ Full tool support (web_search, fetch_page, etc.)
- ✅ Conversational system prompt (optimized for voice)
- ✅ Shorter responses (better for speaking)
- ✅ Clear and reset commands

---

## 📊 How It Works

```
You speak → Microphone → Google Speech API → Text
                                               ↓
                                         Ollama Agent
                                         (with tools)
                                               ↓
Agent Response ← pyttsx3 ← Text Response ← Agent
       ↓
   Speaker
```

**Latency**: ~3-5 seconds per interaction
- ~1s for speech recognition
- ~2-4s for agent processing (depends on model/tools)
- <1s for text-to-speech

---

## 💡 Tips

### For Best Results

1. **Speak clearly** - Short, clear sentences work best
2. **Reduce background noise** - Close windows, turn off fans
3. **Wait for the prompt** - Only speak when you see "🎤 Listening..."
4. **Be patient** - Voice adds 2-3 seconds latency vs text chat
5. **Use --no-tools** - For faster responses if you don't need web search

### When to Use Voice vs Text

**Use Voice (`agent-voice`):**
- ✅ Hands-free operation
- ✅ Quick questions
- ✅ While multitasking
- ✅ Accessibility needs

**Use Text (`agent-chat`):**
- ✅ Complex queries
- ✅ When silence is needed
- ✅ Faster responses
- ✅ Better for long outputs

---

## 🎨 Customization Examples

### Different Language

```bash
agent-voice --language es-ES  # Spanish
```

### Faster Voice

```bash
agent-voice --rate 200 --no-tools
```

### Different Model

```bash
agent-voice --model phi3:mini  # Faster responses
```

---

## ✅ Verification Checklist

Before using voice chat:
- [ ] Homebrew installed (`brew --version`)
- [ ] Portaudio installed (`brew list portaudio`)
- [ ] SpeechRecognition installed (`pip show SpeechRecognition`)
- [ ] pyttsx3 installed (`pip show pyttsx3`)
- [ ] pyaudio installed (`pip show pyaudio`)
- [ ] Microphone permissions granted (System Preferences)
- [ ] Internet connection (for speech recognition)
- [ ] Ollama running (`ollama list`)

---

## 🚦 Next Steps

### 1. Install Dependencies
```bash
brew install portaudio
pip install SpeechRecognition pyttsx3 pyaudio
pip install -e .
```

### 2. Test Voice Chat
```bash
agent-voice --no-tools
```

### 3. Try Full Features
```bash
agent-voice
# Say: "Search for Python tutorials"
```

### 4. Read Full Guide
```bash
cat VOICE_CHAT_GUIDE.md
```

---

## 🆘 Need Help?

1. **Can't install pyaudio?**
   - See "If Installation Fails" section above
   - Or check VOICE_CHAT_GUIDE.md troubleshooting

2. **Speech not recognized?**
   - Check microphone permissions
   - Speak louder/clearer
   - Try: `python -m speech_recognition` to test mic

3. **Agent not responding?**
   - Make sure Ollama is running: `ollama list`
   - Test text chat first: `agent-chat`

---

**Ready to talk to your AI! 🎤🤖**

Run: `agent-voice`
