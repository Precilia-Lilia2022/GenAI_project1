# GenAI Project 1

A Streamlit app for generating LinkedIn posts using Groq + Llama and LangChain.

## Features
- Generate LinkedIn post text with AI
- Select topic, language, and length
- Generate multiple variants
- Save generated post history

## Setup
1. Create a `.env` file in the project root.
2. Add your Groq API key:
   ```env
   GROQ_API_KEY="your_groq_api_key_here"
   ```
3. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Run the app:
   ```powershell
   streamlit run main.py
   ```

## Notes
- Do not commit `.env` to GitHub.
- Use Streamlit Cloud or another deployment service and store `GROQ_API_KEY` as a secret.
