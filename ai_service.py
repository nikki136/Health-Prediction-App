import os
import requests

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

def _safe_fallback(data):
    """A transparent educational fallback; this is not a medical diagnosis."""
    notes = []
    glucose = data["glucose"]
    haemoglobin = data["haemoglobin"]
    cholesterol = data["cholesterol"]

    if glucose >= 200:
        notes.append("Glucose is elevated and should be reviewed by a qualified healthcare professional.")
    elif glucose >= 126:
        notes.append("Glucose is above a commonly used fasting reference threshold; interpretation depends on fasting status.")
    else:
        notes.append("Glucose value alone does not establish a health condition.")

    if haemoglobin < 12:
        notes.append("Haemoglobin is below common adult reference ranges for many people; ranges vary by age and sex.")
    elif haemoglobin > 17.5:
        notes.append("Haemoglobin is above some adult reference ranges; clinical context is needed.")
    else:
        notes.append("Haemoglobin needs interpretation using the patient's age, sex and laboratory range.")

    if cholesterol >= 240:
        notes.append("Total cholesterol is in a commonly described high range.")
    elif cholesterol >= 200:
        notes.append("Total cholesterol is in a commonly described borderline-high range.")
    else:
        notes.append("Total cholesterol is below 200 mg/dL, if the supplied unit is mg/dL.")

    return " ".join(notes) + " This is an automated educational summary, not a diagnosis. Consult a clinician."

def generate_health_remarks(data):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "[Rule-based fallback; Gemini API key not configured] " + _safe_fallback(data)

    prompt = f"""
You are assisting with a health-record demonstration. Summarise these laboratory values cautiously:
Glucose: {data['glucose']}
Haemoglobin: {data['haemoglobin']}
Total cholesterol: {data['cholesterol']}
The units and fasting status were not provided. Do not diagnose or claim certainty. Mention that reference
ranges vary by age, sex, lab and clinical context. Give a short, plain-language note and advise clinician
review for abnormal values. Do not invent patient details. Keep it under 90 words.
"""
    try:
        response = requests.post(
            GEMINI_URL.format(model=GEMINI_MODEL),
            params={"key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not text:
            raise ValueError("Empty AI response")
        return "[Gemini AI] " + text
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        return "[AI API unavailable; rule-based fallback used] " + _safe_fallback(data)
