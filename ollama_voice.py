#!/usr/bin/env python3
"""
Voice wrapper for Ollama using macOS 'say' command (native TTS)
Simple, clean, no extra dependencies needed!
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

from rich.console import Console
from rich.panel import Panel

console = Console()


class OllamaVoiceSay:
    """Voice interface for Ollama using macOS say command."""

    def __init__(
        self,
        model: str = "llama3.1:8b",
        voice: str = "Samantha",
        rate: int = 175,
        language: str = "en-US",
    ):
        """
        Initialize voice interface.

        Args:
            model: Ollama model name
            voice: macOS voice name (Samantha, Daniel, Fred, etc.)
            rate: Speech rate in words per minute
            language: Speech recognition language
        """
        self.model = model
        self.voice = voice
        self.rate = rate
        self.language = language

        # Check if say command exists (macOS only)
        try:
            subprocess.run(['say', '-v', '?'], capture_output=True, check=True, timeout=2)
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            console.print("❌ 'say' command not found. This tool requires macOS.", style="red")
            sys.exit(1)

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

        console.print(f"✅ Using macOS voice: {self.voice} (rate: {self.rate} wpm)", style="green")

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
        """Convert text to speech using macOS say command."""
        try:
            console.print("🔊 Speaking...", style="cyan")
            subprocess.run(
                ['say', '-v', self.voice, '-r', str(self.rate), text],
                check=True
            )
        except subprocess.CalledProcessError as e:
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

    def list_voices(self):
        """List all available macOS voices."""
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        console.print("\n📋 Available Voices:\n", style="cyan bold")
        for line in result.stdout.strip().split('\n')[:20]:  # Show first 20
            console.print(f"  {line}")
        console.print("\n  ... (run 'say -v ?' to see all 177 voices)\n")

    def chat_loop(self):
        """Run voice chat loop."""
        console.print(Panel.fit(
            f"[bold cyan]🎤 Voice Chat with Ollama ({self.model})[/bold cyan]\n\n"
            f"[green]Voice: {self.voice} | Rate: {self.rate} wpm[/green]\n\n"
            "Commands:\n"
            "- Speak your questions naturally\n"
            "- Say 'exit', 'quit', or 'goodbye' to end\n"
            "- Say 'list voices' to see available voices\n",
            border_style="cyan"
        ))

        welcome = f"Hello! I'm {self.model} using the {self.voice} voice. Ask me anything!"
        console.print(f"\n🤖 {self.model}: {welcome}\n", style="green")
        self.speak(welcome)

        while True:
            try:
                user_text = self.listen()

                if not user_text:
                    continue

                console.print(f"\n👤 You: {user_text}", style="cyan bold")

                # Check for list voices
                if 'list voices' in user_text.lower():
                    self.list_voices()
                    continue

                # Check for exit
                if any(word in user_text.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                    farewell = "Goodbye! Have a great day!"
                    console.print(f"\n🤖 {self.model}: {farewell}\n", style="green")
                    self.speak(farewell)
                    break

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
        description="Voice chat with Ollama using macOS say command",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Voices (Popular):
  Samantha     - Female, US (natural, default)
  Daniel       - Male, UK (British accent)
  Fred         - Male, US (deep voice)
  Victoria     - Female, US (professional)
  Alex         - Male, US (classic Mac voice)

Run 'say -v ?' in terminal to see all 177 voices.

Examples:
  python ollama_voice_say.py                    # Default (Samantha)
  python ollama_voice_say.py --voice Daniel     # British male
  python ollama_voice_say.py --voice Fred       # Deep US male
  python ollama_voice_say.py --rate 150         # Slower speech
  python ollama_voice_say.py --rate 200         # Faster speech
        """
    )
    parser.add_argument(
        "model",
        nargs="?",
        default="llama3.1:8b",
        help="Ollama model (default: llama3.1:8b)"
    )
    parser.add_argument(
        "--voice",
        default="Samantha",
        help="macOS voice name (default: Samantha)"
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=175,
        help="Speech rate in words per minute (default: 175)"
    )
    parser.add_argument(
        "--language",
        default="en-US",
        help="Speech recognition language (default: en-US)"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List all available voices and exit"
    )

    args = parser.parse_args()

    # Just list voices and exit
    if args.list_voices:
        console.print("\n📋 All Available macOS Voices:\n", style="cyan bold")
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        console.print(result.stdout)
        return

    console.print("\n🚀 Initializing voice chat...\n", style="bold cyan")

    voice = OllamaVoiceSay(
        model=args.model,
        voice=args.voice,
        rate=args.rate,
        language=args.language,
    )

    voice.chat_loop()

    console.print("\n✨ Voice chat ended!\n", style="bold green")


if __name__ == "__main__":
    main()
