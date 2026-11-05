# HealthDesk – Health Prediction Application

A Flask + SQLite patient-record management demo built for the Gokul Infocare Task 2 assessment.

## Features
- Create, read, update and delete patient records.
- Validates full name, email, date of birth and numeric blood-test values.
- Accepts DOB as `dd/mm/yyyy` and also `dd.mm.yyyy` to support the exact assessment test data.
- Rejects impossible dates and future dates.
- Stores records persistently in SQLite (`patients.db` is created automatically).
- Calls the Gemini Generative Language API for cautious, non-diagnostic remarks when an API key is configured.
- Uses a clearly labelled local fallback if no API key is configured or the API request fails.

## Technology
- Python 3.10+
- Flask
- SQLite
- Bootstrap 5, HTML and CSS
- Gemini API over HTTPS (`requests`)

## Setup (Windows PowerShell)

```powershell
# 1. Extract the ZIP and open this folder in VS Code
cd Health_Prediction_App

# 2. Create and activate a virtual environment
py -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your local environment file
Copy-Item .env.example .env
```

Open `.env` and add your Gemini API key to `GEMINI_API_KEY` if you have one. Keep `.env` private; it is excluded by `.gitignore`. The app still works without the key, using its labelled fallback.

```powershell
# 5. Run the application
python app.py
```

Open http://127.0.0.1:5000 in your browser. The SQLite database is created automatically on first run.

## Gemini API
The app sends only glucose, haemoglobin and cholesterol values to Gemini to produce a short educational summary. It does not send the patient's name, date of birth or email. The prompt explicitly asks the model not to diagnose and to mention missing units/clinical context.

To use Gemini:
1. Create an API key through Google AI Studio.
2. Put it in `.env` as `GEMINI_API_KEY=your_key`.
3. Restart the Flask application.
4. Create a new record to generate AI remarks.

If the API is unavailable, the app records a rule-based educational fallback and labels it accordingly. Do not describe fallback remarks as AI-generated.

## Assessment test-data handling

The supplied table contains intentionally invalid entries:
- Test 2: `hunter@gmail` is invalid because it has no complete domain suffix.
- Test 4: `31.11.2001` is not a real calendar date; November has 30 days.
- Test 8: `19.10.2030` is a future date and `Kris.wu.gmail.com` is not a valid email address.

The remaining entries are valid in basic format. Test 7's haemoglobin value is numerically accepted; an unusually low value should be flagged for clinician review, not rejected as a formatting error. Test 6 repeats Test 1. The app permits duplicates because the brief does not require unique patient names or emails.

The assessment asks you not to modify the supplied values. Enter each row exactly as provided. The three invalid rows should be rejected by validation and explained in your video. Do not silently correct them.

## Demonstration checklist
1. Add the valid test rows exactly as supplied.
2. Attempt Test 2 and show the email validation message.
3. Attempt Test 4 and show the invalid-calendar-date message.
4. Attempt Test 8 and show both future-DOB and invalid-email messages.
5. Show the list of successfully saved records.
6. Edit one saved record's email to `gokul@infocare.com`.
7. Delete one saved record.
8. Show the final list after deletion.
9. Walk through `validators.py`, `database.py`, `ai_service.py` and the routes in `app.py`.

## GitHub safety checklist
- Do not commit `.env`, `patients.db`, passwords or API keys.
- `.gitignore` already excludes `.env` and the SQLite database.
- Commit `.env.example` only; it contains blank configuration values.
- Use synthetic assessment data only. Do not upload real patient health information.

## Important limitations
This is an educational assessment prototype, not a clinical decision-support system. It does not establish diagnoses or replace a healthcare professional. The assessment data does not specify measurement units, fasting status, sex or laboratory reference ranges, so predictions must remain cautious and qualified.
