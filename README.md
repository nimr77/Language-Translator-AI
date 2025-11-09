# 🌍 Language Translator AI

🇵🇸 **Built with solidarity with Palestine** 🇵🇸

> "Freedom is not given—it is the voice that breaks through silence, the light that persists in darkness, and the hope that transcends all boundaries."

A beautiful Python application that translates files using Google Gemini AI with an intuitive console interface.

## ✨ Features

- 🎨 Beautiful console UI with emojis and rich formatting
- 🌐 Support for 30+ languages
- 💾 Configuration persistence (.config file)
- 🔄 Smart file naming (e.g., `intl_en.arb` → `intl_es.arb`)
- 📋 Saves your preferences for quick reuse
- ⚡ Fast and efficient translation using Google Gemini AI

## 🚀 Quick Start

1. **Set up your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Gemini API key
   ```

2. **Run the application:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 app.py
   ```

## 📋 Usage

1. The app will prompt you to select a source file
2. Choose languages to translate to from the available list
3. Specify the output directory
4. The app will translate and save files with the pattern: `{base_name}_{language_code}.arb`

## 🌐 Supported Languages

The app supports 30+ languages including:
- Spanish (es)
- French (fr)
- Arabic (ar)
- Turkish (tr)
- Japanese (ja)
- Portuguese (pt)
- Italian (it)
- And many more!

## 📁 Configuration

The app saves your preferences in a `.config` file:
- Source file path
- Selected languages
- Output directory

## 📝 Example

If you have a file `lib/l10n/intl_en.arb` and select Spanish, French, and Arabic, the app will create:
- `lib/l10n/intl_es.arb`
- `lib/l10n/intl_fr.arb`
- `lib/l10n/intl_ar.arb`

## 🔑 API Key

Get your Google Gemini API key from: https://makersuite.google.com/app/apikey

## 📦 Requirements

- Python 3.7+
- Google Gemini API key
- Internet connection

## 🛠️ Dependencies

- `python-dotenv` - Environment variable management
- `google-generativeai` - Google Gemini AI SDK
- `rich` - Beautiful terminal UI

