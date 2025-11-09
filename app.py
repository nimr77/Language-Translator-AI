#!/usr/bin/env python3
"""
Language Translator AI - Translate files using Google Gemini AI
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

# Load environment variables
load_dotenv()

console = Console()

# Language codes and names mapping
LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "ar": "Arabic",
    "tr": "Turkish",
    "ja": "Japanese",
    "pt": "Portuguese",
    "it": "Italian",
    "de": "German",
    "zh": "Chinese",
    "ru": "Russian",
    "ko": "Korean",
    "hi": "Hindi",
    "nl": "Dutch",
    "pl": "Polish",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
    "cs": "Czech",
    "ro": "Romanian",
    "hu": "Hungarian",
    "el": "Greek",
    "he": "Hebrew",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
    "uk": "Ukrainian",
    "bg": "Bulgarian",
    "hr": "Croatian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "et": "Estonian",
    "lv": "Latvian",
    "lt": "Lithuanian",
}

CONFIG_FILE = ".config"


class LanguageTranslator:
    def __init__(self):
        self.config = self.load_config()
        self.api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        
        if not self.api_key:
            console.print("❌ [bold red]Error:[/bold red] GOOGLE_GEMINI_API_KEY not found in .env file", style="bold red")
            sys.exit(1)
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def load_config(self) -> Dict:
        """Load configuration from .config file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"⚠️  [yellow]Warning:[/yellow] Could not load config: {e}")
        return {
            "source_file": "",
            "languages": [],
            "output_path": ""
        }
    
    def save_config(self):
        """Save configuration to .config file"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            console.print(f"✅ [green]Configuration saved to {CONFIG_FILE}[/green]")
        except Exception as e:
            console.print(f"❌ [bold red]Error saving config:[/bold red] {e}")
    
    def display_welcome(self):
        """Display welcome screen"""
        welcome_text = Text()
        welcome_text.append("🌍 ", style="bold cyan")
        welcome_text.append("Language Translator AI", style="bold cyan")
        welcome_text.append(" 🌍", style="bold cyan")
        
        console.print("\n")
        console.print(Panel(
            welcome_text,
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print("✨ Translate your files using Google Gemini AI ✨\n", style="cyan")
    
    def select_source_file(self) -> str:
        """Prompt user to select source file"""
        console.print("\n📄 [bold]Step 1: Select Source File[/bold]\n")
        
        if self.config.get("source_file") and os.path.exists(self.config["source_file"]):
            use_saved = Confirm.ask(
                f"📋 Use saved source file: [cyan]{self.config['source_file']}[/cyan]?",
                default=True
            )
            if use_saved:
                return self.config["source_file"]
        
        while True:
            source_file = Prompt.ask("📁 Enter the path to your source file")
            if os.path.exists(source_file):
                self.config["source_file"] = source_file
                return source_file
            else:
                console.print("❌ [red]File not found! Please try again.[/red]")
    
    def display_languages(self):
        """Display available languages in a table"""
        table = Table(title="🌐 Available Languages", show_header=True, header_style="bold magenta")
        table.add_column("Code", style="cyan", width=8)
        table.add_column("Language", style="green", width=20)
        
        for code, name in sorted(LANGUAGES.items(), key=lambda x: x[1]):
            table.add_row(code, name)
        
        console.print(table)
    
    def select_languages(self) -> List[str]:
        """Prompt user to select languages"""
        console.print("\n🌐 [bold]Step 2: Select Languages to Translate To[/bold]\n")
        
        self.display_languages()
        
        if self.config.get("languages"):
            use_saved = Confirm.ask(
                f"📋 Use saved languages: [cyan]{', '.join([LANGUAGES.get(l, l) for l in self.config['languages']])}[/cyan]?",
                default=True
            )
            if use_saved:
                return self.config["languages"]
        
        console.print("\n💡 [yellow]Tip:[/yellow] Enter language codes separated by commas (e.g., es,fr,ar,tr,ja,pt,it)\n")
        
        while True:
            selected = Prompt.ask("🎯 Enter language codes to translate to")
            codes = [code.strip().lower() for code in selected.split(",")]
            
            invalid_codes = [code for code in codes if code not in LANGUAGES]
            if invalid_codes:
                console.print(f"❌ [red]Invalid language codes: {', '.join(invalid_codes)}[/red]")
                continue
            
            if not codes:
                console.print("❌ [red]Please select at least one language[/red]")
                continue
            
            # Display selected languages
            selected_names = [f"{LANGUAGES[code]} ({code})" for code in codes]
            console.print(f"\n✅ Selected languages: [green]{', '.join(selected_names)}[/green]")
            
            self.config["languages"] = codes
            return codes
    
    def get_output_path(self) -> str:
        """Get or prompt for output path"""
        console.print("\n📂 [bold]Step 3: Output Path Configuration[/bold]\n")
        
        if self.config.get("output_path"):
            use_saved = Confirm.ask(
                f"📋 Use saved output path: [cyan]{self.config['output_path']}[/cyan]?",
                default=True
            )
            if use_saved:
                return self.config["output_path"]
        
        source_file = self.config["source_file"]
        source_path = Path(source_file)
        
        # Extract directory and filename pattern
        default_dir = source_path.parent
        default_pattern = source_path.stem
        
        console.print(f"💡 [yellow]Default pattern:[/yellow] {default_dir}/[cyan]{default_pattern}_[language_code].arb[/cyan]")
        
        output_path = Prompt.ask(
            "📁 Enter output directory path",
            default=str(default_dir)
        )
        
        self.config["output_path"] = output_path
        return output_path
    
    def read_source_file(self, file_path: str) -> str:
        """Read content from source file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            console.print(f"❌ [bold red]Error reading file:[/bold red] {e}")
            sys.exit(1)
    
    def translate_content(self, content: str, target_language: str, language_name: str) -> str:
        """Translate content using Gemini AI"""
        prompt = f"""You are a professional translator. Translate the following JSON/ARB file content to {language_name} ({target_language}).

IMPORTANT RULES:
1. Preserve the exact JSON/ARB structure and formatting
2. Only translate the string values, NOT the keys
3. Keep all special characters, placeholders (like {{variable}}), and formatting intact
4. Maintain the same indentation and structure
5. Do not translate technical terms, variable names, or code

Content to translate:
{content}

Return ONLY the translated content, maintaining the exact same structure."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            console.print(f"❌ [bold red]Translation error for {language_name}:[/bold red] {e}")
            return None
    
    def save_translated_file(self, content: str, file_path: str):
        """Save translated content to file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            console.print(f"❌ [bold red]Error saving file {file_path}:[/bold red] {e}")
    
    def generate_output_filename(self, source_file: str, language_code: str, output_dir: str) -> str:
        """Generate output filename based on pattern"""
        source_path = Path(source_file)
        source_name = source_path.stem
        
        # Extract language code from source if present (e.g., intl_en.arb -> intl)
        if '_' in source_name:
            parts = source_name.split('_')
            # Assume last part is language code, remove it
            base_name = '_'.join(parts[:-1])
        else:
            base_name = source_name
        
        output_filename = f"{base_name}_{language_code}{source_path.suffix}"
        return os.path.join(output_dir, output_filename)
    
    def run(self):
        """Main application flow"""
        self.display_welcome()
        
        # Step 1: Select source file
        source_file = self.select_source_file()
        
        # Step 2: Select languages
        languages = self.select_languages()
        
        # Step 3: Get output path
        output_dir = self.get_output_path()
        
        # Save configuration
        self.save_config()
        
        # Read source file
        console.print(f"\n📖 [bold]Reading source file:[/bold] [cyan]{source_file}[/cyan]")
        source_content = self.read_source_file(source_file)
        
        # Confirm before translating
        console.print(f"\n🚀 [bold]Ready to translate![/bold]")
        console.print(f"📄 Source: [cyan]{source_file}[/cyan]")
        console.print(f"🌐 Languages: [green]{', '.join([LANGUAGES.get(l, l) for l in languages])}[/green]")
        console.print(f"📂 Output: [cyan]{output_dir}[/cyan]\n")
        
        if not Confirm.ask("✨ Start translation?", default=True):
            console.print("👋 Translation cancelled. Goodbye!")
            return
        
        # Translate to each language
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            total = len(languages)
            
            for i, lang_code in enumerate(languages, 1):
                lang_name = LANGUAGES[lang_code]
                task = progress.add_task(f"🔄 Translating to {lang_name}...", total=1)
                
                # Translate
                translated_content = self.translate_content(source_content, lang_code, lang_name)
                
                if translated_content:
                    # Generate output filename
                    output_file = self.generate_output_filename(source_file, lang_code, output_dir)
                    
                    # Save file
                    self.save_translated_file(translated_content, output_file)
                    
                    progress.update(task, completed=1)
                    console.print(f"✅ [green]Saved:[/green] [cyan]{output_file}[/cyan]")
                else:
                    progress.update(task, completed=1)
                    console.print(f"❌ [red]Failed to translate to {lang_name}[/red]")
        
        console.print(f"\n🎉 [bold green]Translation complete![/bold green] 🎉")
        console.print(f"📊 Translated to [bold]{len(languages)}[/bold] language(s)\n")


def main():
    try:
        translator = LanguageTranslator()
        translator.run()
    except KeyboardInterrupt:
        console.print("\n\n👋 [yellow]Translation cancelled by user. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n❌ [bold red]Unexpected error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

