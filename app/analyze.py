# app/analyze.py
import os
from textwrap import dedent
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # lokal .env laden; im Deploy kommen Env Vars
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY fehlt. Setze ihn lokal in .env oder als Env Var im Hosting.")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = dedent("""
    Du erklärst Verträge in einfachem, verständlichem Deutsch.
    Du bist KEIN Rechtsanwalt; keine Rechtsberatung – nur sprachliche Erklärung.

    Antworte IMMER in dieser Struktur:
    1. Kurz zusammengefasst
    2. Deine Pflichten
    3. Pflichten der anderen Partei
    4. Geld / Haftung / Strafen
    5. Laufzeit & Kündigung
    6. ⚠ Risiken / Dinge, die du prüfen solltest

    Wenn etwas nicht geregelt ist, schreibe: "nicht klar geregelt".
""")

def analyze_contract_text(text: str) -> str:
    if not text or not text.strip():
        return "Kein Vertragstext erkannt."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Erkläre folgenden Vertragstext:\n\n{text}"}
        ],
    )
    return resp.choices[0].message.content
