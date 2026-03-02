#!/usr/bin/env python3
"""
Voice Chat with Ollama Agent
Speech-to-text and text-to-speech interface for the AI agent
"""
import sys
import os
import logging
from typing import Optional

# Try to import speech libraries
try:
    import speech_recognition as sr
except ImportError:
    print("❌ speech_recognition not installed. Run: pip install SpeechRecognition pyaudio")
    sys.exit(1)

try:
    import pyttsx3
except ImportError:
    print("❌ pyttsx3 not installed. Run: pip install pyttsx3")
    sys.exit(1)

from local_llm.agent import Agent
from tools import get_default_tools
from rich.console import Console
from rich.panel import Panel

console = Console()
logging.basicConfig(level=logging.WARNING)


class VoiceChat:
    """Voice interface for Ollama agent using speech recognition and TTS."""

    def __init__(
        self,
        agent: Agent,
        language: str = "en-US",
        voice_rate: int = 175,
        voice_volume: float = 0.9,
    ):
        """
        Initialize voice chat interface.

        Args:
            agent: The Agent instance to use
            language: Speech recognition language (default: en-US)
            voice_rate: Speech rate in words per minute (default: 175)
            voice_volume: Volume level 0.0 to 1.0 (default: 0.9)
        """
        self.agent = agent
        self.language = language

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust based on environment
        self.recognizer.dynamic_energy_threshold = True

        # Initialize text-to-speech engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', voice_rate)
            self.tts_engine.setProperty('volume', voice_volume)

            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to use a more natural voice if available
                # On Mac, use 'Samantha' or 'Alex'
                for voice in voices:
                    if 'samantha' in voice.name.lower() or 'alex' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break

            console.print("✅ Text-to-speech engine initialized", style="green")
        except Exception as e:
            console.print(f"⚠️  TTS initialization warning: {e}", style="yellow")
            self.tts_engine = None

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen to microphone and convert speech to text.

        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for a phrase

        Returns:
            Transcribed text or None if failed
        """
        with sr.Microphone() as source:
            console.print("🎤 Listening...", style="cyan")

            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                console.print("🔄 Transcribing...", style="yellow")

                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text

            except sr.WaitTimeoutError:
                console.print("⏱️  No speech detected", style="yellow")
                return None
            except sr.UnknownValueError:
                console.print("❓ Could not understand audio", style="yellow")
                return None
            except sr.RequestError as e:
                console.print(f"❌ Speech recognition error: {e}", style="red")
                return None

    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.

        Args:
            text: Text to speak
        """
        if not self.tts_engine:
            console.print("⚠️  TTS not available, skipping speech", style="yellow")
            return

        try:
            console.print("🔊 Speaking...", style="cyan")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            console.print(f"⚠️  TTS error: {e}", style="yellow")

    def chat_loop(self):
        """Run the voice chat loop."""
        console.print(Panel.fit(
            "[bold cyan]🎤 Voice Chat with Ollama Agent[/bold cyan]\n\n"
            "Commands:\n"
            "- Speak naturally to ask questions\n"
            "- Say 'exit', 'quit', or 'goodbye' to end\n"
            "- Say 'clear' to reset conversation\n",
            border_style="cyan"
        ))

        # Welcome message
        welcome = "Hello! I'm your voice assistant. How can I help you today?"
        console.print(f"\n🤖 Agent: {welcome}\n", style="green")
        self.speak(welcome)

        while True:
            try:
                # Listen for user input
                user_text = self.listen()

                if not user_text:
                    continue

                # Display what was heard
                console.print(f"\n👤 You said: {user_text}", style="cyan bold")

                # Check for exit commands
                if any(word in user_text.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                    farewell = "Goodbye! Have a great day!"
                    console.print(f"\n🤖 Agent: {farewell}\n", style="green")
                    self.speak(farewell)
                    break

                # Check for clear command
                if 'clear' in user_text.lower():
                    self.agent.reset()
                    response = "Conversation cleared. What would you like to talk about?"
                    console.print(f"\n🤖 Agent: {response}\n", style="green")
                    self.speak(response)
                    continue

                # Get agent response
                console.print("\n🤔 Thinking...", style="yellow")
                response = self.agent.chat(user_text)

                # Display and speak response
                console.print(f"\n🤖 Agent: {response}\n", style="green")
                self.speak(response)

            except KeyboardInterrupt:
                console.print("\n\n👋 Interrupted by user", style="yellow")
                break
            except Exception as e:
                console.print(f"\n❌ Error: {e}", style="red")
                continue


def main():
    """Main entry point for voice chat."""
    import argparse

    parser = argparse.ArgumentParser(description="Voice chat with Ollama agent")
    parser.add_argument(
        "--model",
        default="llama3.1:8b",
        help="Ollama model to use (default: llama3.1:8b)"
    )
    parser.add_argument(
        "--no-tools",
        action="store_true",
        help="Disable all tools (faster responses)"
    )
    parser.add_argument(
        "--language",
        default="en-US",
        help="Speech recognition language (default: en-US)"
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=175,
        help="Speech rate in words per minute (default: 175)"
    )
    parser.add_argument(
        "--volume",
        type=float,
        default=0.9,
        help="Speech volume 0.0-1.0 (default: 0.9)"
    )

    args = parser.parse_args()

    # Create agent
    console.print("\n🚀 Initializing voice chat...\n", style="bold cyan")

    tools = [] if args.no_tools else get_default_tools(
        include_browser_tools=False,
        include_copart=False
    )

    # Use a more conversational system prompt for voice
    system_prompt = """You are a helpful voice assistant. Keep your responses concise and conversational since they will be spoken aloud.

Important guidelines:
- Keep responses brief (2-3 sentences when possible)
- Avoid long lists or technical jargon unless asked
- Be friendly and natural in tone
- Only use tools when the user explicitly asks or when absolutely necessary
- For general questions, answer from your knowledge directly"""

    agent = Agent(
        tools=tools,
        model=args.model,
        system_prompt=system_prompt,
        max_iterations=3,  # Limit iterations for faster voice responses
    )

    if tools:
        console.print(f"✅ Loaded {len(tools)} tools", style="green")

    # Create voice chat interface
    voice_chat = VoiceChat(
        agent=agent,
        language=args.language,
        voice_rate=args.rate,
        voice_volume=args.volume,
    )

    # Start chat loop
    voice_chat.chat_loop()

    console.print("\n✨ Voice chat ended. Thank you!\n", style="bold green")


if __name__ == "__main__":
    main()
