#!/usr/bin/env python3
"""
Voice wrapper for Ollama CLI
Speak to Ollama models directly with voice input/output
"""
import subprocess
import sys
import argparse
from typing import Optional

try:
    import speech_recognition as sr
except ImportError:
    print("❌ speech_recognition not installed. Run: pip install SpeechRecognition")
    sys.exit(1)

try:
    import pyttsx3
except ImportError:
    print("❌ pyttsx3 not installed. Run: pip install pyttsx3")
    sys.exit(1)

from rich.console import Console
from rich.panel import Panel

console = Console()


class OllamaVoice:
    """Voice interface for Ollama CLI."""

    def __init__(
        self,
        model: str = "llama3.1:8b",
        voice_name: Optional[str] = None,
        voice_rate: int = 175,
        voice_volume: float = 0.9,
        language: str = "en-US",
    ):
        """
        Initialize voice interface for Ollama.

        Args:
            model: Ollama model name
            voice_name: Voice name (e.g., "Samantha", "Daniel", "Fred")
            voice_rate: Speech rate in words per minute
            voice_volume: Volume 0.0 to 1.0
            language: Speech recognition language
        """
        self.model = model
        self.language = language
        self.voice_name = voice_name

        # Check if Ollama is available
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                console.print("❌ Ollama not running. Start it with: ollama serve", style="red")
                sys.exit(1)
        except FileNotFoundError:
            console.print("❌ Ollama not installed. Visit: https://ollama.ai", style="red")
            sys.exit(1)
        except subprocess.TimeoutExpired:
            console.print("❌ Ollama not responding", style="red")
            sys.exit(1)

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', voice_rate)
            self.tts_engine.setProperty('volume', voice_volume)

            # Get available voices
            voices = self.tts_engine.getProperty('voices')

            # Select voice
            if voices:
                if voice_name:
                    # Try to find voice by name
                    voice_found = False
                    for voice in voices:
                        # Match by name (case-insensitive)
                        if voice_name.lower() in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            console.print(f"✅ Using voice: {voice.name}", style="green")
                            voice_found = True
                            break

                    if not voice_found:
                        console.print(f"⚠️  Voice '{voice_name}' not found, using default", style="yellow")
                else:
                    # Default: try to use Samantha or Alex on Mac
                    for voice in voices:
                        if 'samantha' in voice.name.lower() or 'alex' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            console.print(f"✅ Using voice: {voice.name}", style="green")
                            break

            if not voice_name:
                console.print("✅ Text-to-speech ready", style="green")
        except Exception as e:
            console.print(f"⚠️  TTS warning: {e}", style="yellow")
            self.tts_engine = None

    def listen(self, timeout: int = 5, phrase_limit: int = 15) -> Optional[str]:
        """
        Listen to microphone and return transcribed text.

        Args:
            timeout: Seconds to wait for speech
            phrase_limit: Max seconds for a phrase

        Returns:
            Transcribed text or None
        """
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
        """Convert text to speech."""
        if not self.tts_engine:
            return

        try:
            console.print("🔊 Speaking...", style="cyan")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            console.print(f"⚠️  TTS error: {e}", style="yellow")

    def ask_ollama(self, prompt: str) -> Optional[str]:
        """
        Send prompt to Ollama and get response.

        Args:
            prompt: User's question

        Returns:
            Ollama's response or None
        """
        try:
            console.print(f"\n🤖 Asking {self.model}...", style="yellow")

            # Run ollama command
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                response = result.stdout.strip()
                return response
            else:
                error = result.stderr.strip()
                console.print(f"❌ Ollama error: {error}", style="red")
                return None

        except subprocess.TimeoutExpired:
            console.print("⏱️  Ollama timeout", style="red")
            return None
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            return None

    @staticmethod
    def list_voices():
        """List all available TTS voices."""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')

            console.print("\n" + "="*70, style="cyan")
            console.print("🎙️  Available Text-to-Speech Voices", style="cyan bold")
            console.print("="*70 + "\n", style="cyan")

            for i, voice in enumerate(voices, 1):
                console.print(f"{i}. [bold]{voice.name}[/bold]")
                console.print(f"   ID: [dim]{voice.id}[/dim]")
                if hasattr(voice, 'languages') and voice.languages:
                    console.print(f"   Languages: {voice.languages}")
                console.print()

            console.print("="*70, style="cyan")
            console.print(f"Total: {len(voices)} voices\n", style="cyan")

        except Exception as e:
            console.print(f"❌ Error listing voices: {e}", style="red")

    def chat_loop(self):
        """Run the voice chat loop."""
        console.print(Panel.fit(
            f"[bold cyan]🎤 Voice Chat with Ollama ({self.model})[/bold cyan]\n\n"
            "Commands:\n"
            "- Speak your questions naturally\n"
            "- Say 'exit', 'quit', or 'goodbye' to end\n"
            "- Say 'stop' to interrupt\n",
            border_style="cyan"
        ))

        # Welcome
        welcome = f"Hello! I'm {self.model}. Ask me anything!"
        console.print(f"\n🤖 {self.model}: {welcome}\n", style="green")
        self.speak(welcome)

        while True:
            try:
                # Listen for input
                user_text = self.listen()

                if not user_text:
                    continue

                # Display what was heard
                console.print(f"\n👤 You: {user_text}", style="cyan bold")

                # Check for exit
                if any(word in user_text.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                    farewell = "Goodbye! Have a great day!"
                    console.print(f"\n🤖 {self.model}: {farewell}\n", style="green")
                    self.speak(farewell)
                    break

                # Check for stop
                if 'stop' in user_text.lower():
                    console.print("\n⏹️  Stopped", style="yellow")
                    continue

                # Ask Ollama
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
        description="Voice chat with Ollama models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ollama-voice                          # Use default model (llama3.1:8b)
  ollama-voice llama3.1:8b              # Specify model
  ollama-voice phi3:mini                # Use faster model
  ollama-voice --rate 150               # Slower speech
  ollama-voice --language es-ES         # Spanish
        """
    )
    parser.add_argument(
        "model",
        nargs="?",
        default="llama3.1:8b",
        help="Ollama model name (default: llama3.1:8b)"
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
    parser.add_argument(
        "--language",
        default="en-US",
        help="Speech recognition language (default: en-US)"
    )
    parser.add_argument(
        "--voice",
        help="Voice name (e.g., Samantha, Daniel, Fred). Use --list-voices to see all."
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List all available voices and exit"
    )

    args = parser.parse_args()

    # List voices and exit if requested
    if args.list_voices:
        OllamaVoice.list_voices()
        return

    # Start voice chat
    console.print("\n🚀 Initializing voice chat with Ollama...\n", style="bold cyan")

    voice = OllamaVoice(
        model=args.model,
        voice_name=args.voice,
        voice_rate=args.rate,
        voice_volume=args.volume,
        language=args.language,
    )

    voice.chat_loop()

    console.print("\n✨ Voice chat ended. Thank you!\n", style="bold green")


if __name__ == "__main__":
    main()
