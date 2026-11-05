import re
from datetime import datetime, date

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")

def parse_date(value):
    """Accept the supplied assessment format dd.mm.yyyy and the requested dd/mm/yyyy."""
    value = (value or "").strip()
    for fmt in ("%d/%m/%Y", "%d.%m.%Y"):
        try:
            parsed = datetime.strptime(value, fmt).date()
            return parsed
        except ValueError:
            continue
    return None

def validate_patient(form):
    errors = []
    full_name = (form.get("full_name") or "").strip()
    dob_raw = (form.get("date_of_birth") or "").strip()
    email = (form.get("email") or "").strip()
    if not full_name or len(full_name) > 100:
        errors.append("Full name is required and must be 100 characters or fewer.")

    dob = parse_date(dob_raw)
    if not dob:
        errors.append("Date of birth must be a real date in dd/mm/yyyy format (the supplied dd.mm.yyyy format is also accepted).")
    elif dob > date.today():
        errors.append("Date of birth cannot be in the future.")

    if not EMAIL_PATTERN.fullmatch(email):
        errors.append("Enter a valid email address, for example name@example.com.")

    numbers = {}
    for field, label in (("glucose", "Glucose"), ("haemoglobin", "Haemoglobin"), ("cholesterol", "Cholesterol")):
        raw = (form.get(field) or "").strip()
        try:
            value = float(raw)
            if value < 0 or value > 10000:
                raise ValueError
            numbers[field] = value
        except (ValueError, TypeError):
            errors.append(f"{label} must be a valid non-negative numeric value.")

    data = {}
    if full_name:
        data["full_name"] = full_name
    if dob:
        data["date_of_birth"] = dob.strftime("%d/%m/%Y")
    if email:
        data["email"] = email
    data.update(numbers)
    return data, errors
