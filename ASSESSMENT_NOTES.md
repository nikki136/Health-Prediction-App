# Task 2 – Video explanation notes

## Architecture
Browser form -> Flask route (`app.py`) -> validation (`validators.py`) -> Gemini API service (`ai_service.py`) -> SQLite database (`database.py`) -> records table.

## Explain the main files
- `app.py`: Defines page routes and connects the form, validation, AI service and database.
- `validators.py`: Checks required name, email format, real DOB, future DOB and numeric non-negative test values.
- `database.py`: Uses SQLite and parameterized SQL statements for CRUD operations.
- `ai_service.py`: Sends a limited prompt to Gemini using an environment variable API key. If the API is unavailable, a labelled fallback is used.
- `templates/`: HTML pages rendered by Flask.
- `static/css/style.css`: Application styling.

## Why the supplied rows fail
- Test 2: `hunter@gmail` does not match the email pattern because a domain suffix is missing.
- Test 4: November has 30 days, so 31 November is not a valid date.
- Test 8: The date 19 October 2030 is after today's date at the time of the assessment, and `Kris.wu.gmail.com` has no `@` symbol.

## Important demonstration detail
The brief says not to modify the test data. Keep the original values when showing failed submissions. A failed form is not inserted into the database. For the duplicate row (Test 6), this prototype permits a duplicate because the brief does not define a duplicate-rejection rule.

## AI API explanation
`generate_health_remarks()` reads `GEMINI_API_KEY` from the environment. It posts a JSON prompt to the Gemini `generateContent` endpoint. The key is not hard-coded. The prompt excludes direct identifiers and asks for cautious educational remarks, not diagnosis. HTTP, response-shape and empty-response errors trigger the labelled fallback.
