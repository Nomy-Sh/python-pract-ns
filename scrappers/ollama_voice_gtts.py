#!/usr/bin/env python3
"""
Voice wrapper for Ollama CLI with Google Text-to-Speech (better quality)
Requires: pip install gtts pygame
"""
import subprocess
import sys
import argparse
import tempfile
import os
from typing import Optional

try:
    import speech_recognition as sr
except ImportError:
    print("❌ speech_recognition not installed. Run: pip install SpeechRecognition")
    sys.exit(1)

try:
    from gtts import gTTS
except ImportError:
    print("❌ gtts not installed. Run: pip install gtts")
    sys.exit(1)

try:
    import pygame
except ImportError:
    print("❌ pygame not installed. Run: pip install pygame")
    sys.exit(1)

from rich.console import Console
from rich.panel import Panel

console = Console()


class OllamaVoiceGTTS:
    """Voice interface for Ollama CLI with Google TTS (better quality)."""

    def __init__(
        self,
        model: str = "llama3.1:8b",
        language: str = "en-US",
        tts_lang: str = "en",
        slow: bool = False,
    ):
        """
        Initialize voice interface with Google TTS.

        Args:
            model: Ollama model name
            language: Speech recognition language (en-US, es-ES, etc.)
            tts_lang: TTS language code (en, es, fr, etc.)
            slow: Slower TTS speech
        """
        self.model = model
        self.language = language
        self.tts_lang = tts_lang
        self.slow = slow

        # Check Ollama
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                console.print("❌ Ollama not running", style="red")
                sys.exit(1)
        except FileNotFoundError:
            console.print("❌ Ollama not installed", style="red")
            sys.exit(1)

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        console.print("✅ Google Text-to-Speech ready (high quality)", style="green")

    def listen(self, timeout: int = 5, phrase_limit: int = 15) -> Optional[str]:
        """Listen to microphone and return text."""
        with sr.Microphone() as source:
            console.print("🎤 Listening...", style="cyan")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
                console.print("🔄 Transcribing...", style="yellow")
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
        """Convert text to speech using Google TTS (high quality)."""
        try:
            console.print("🔊 Speaking...", style="cyan")

            # Create TTS
            tts = gTTS(text=text, lang=self.tts_lang, slow=self.slow)

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)

            # Play audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Clean up
            pygame.mixer.music.unload()
            os.remove(temp_file)

        except Exception as e:
            console.print(f"⚠️  TTS error: {e}", style="yellow")

    def ask_ollama(self, prompt: str) -> Optional[str]:
        """Send prompt to Ollama."""
        try:
            console.print(f"\n🤖 Asking {self.model}...", style="yellow")

            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                console.print(f"❌ Error: {result.stderr.strip()}", style="red")
                return None

        except subprocess.TimeoutExpired:
            console.print("⏱️  Timeout", style="red")
            return None
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            return None

    def chat_loop(self):
        """Run voice chat loop."""
        console.print(Panel.fit(
            f"[bold cyan]🎤 Voice Chat with Ollama ({self.model})[/bold cyan]\n\n"
            "[green]Using Google Text-to-Speech (High Quality)[/green]\n\n"
            "Commands:\n"
            "- Speak your questions naturally\n"
            "- Say 'exit', 'quit', or 'goodbye' to end\n",
            border_style="cyan"
        ))

        welcome = f"Hello! I'm {self.model}. I'm using high-quality voice. Ask me anything!"
        console.print(f"\n🤖 {self.model}: {welcome}\n", style="green")
        self.speak(welcome)

        while True:
            try:
                user_text = self.listen()

                if not user_text:
                    continue

                console.print(f"\n👤 You: {user_text}", style="cyan bold")

                if any(word in user_text.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                    farewell = "Goodbye! Have a great day!"
                    console.print(f"\n🤖 {self.model}: {farewell}\n", style="green")
                    self.speak(farewell)
                    break

                response = self.ask_ollama(user_text)

                if response:
                    console.print(f"\n🤖 {self.model}: {response}\n", style="green")
                    self.speak(response)

            except KeyboardInterrupt:
                console.print("\n\n👋 Interrupted", style="yellow")
                break
            except Exception as e:
                console.print(f"\n❌ Error: {e}", style="red")
                continue


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Voice chat with Ollama using Google TTS (high quality)"
    )
    parser.add_argument(
        "model",
        nargs="?",
        default="llama3.1:8b",
        help="Ollama model (default: llama3.1:8b)"
    )
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Slower speech"
    )
    parser.add_argument(
        "--language",
        default="en-US",
        help="Speech recognition language (default: en-US)"
    )
    parser.add_argument(
        "--tts-lang",
        default="en",
        help="TTS language: en, es, fr, de, etc. (default: en)"
    )

    args = parser.parse_args()

    console.print("\n🚀 Initializing high-quality voice chat...\n", style="bold cyan")

    voice = OllamaVoiceGTTS(
        model=args.model,
        language=args.language,
        tts_lang=args.tts_lang,
        slow=args.slow,
    )

    voice.chat_loop()

    console.print("\n✨ Voice chat ended!\n", style="bold green")


if __name__ == "__main__":
    main()
