import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from database import init_db, get_all_patients, get_patient, create_patient, update_patient, delete_patient
from validators import validate_patient
from ai_service import generate_health_remarks

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-secret")
init_db()

@app.route("/")
def index():
    patients = get_all_patients()
    return render_template("index.html", patients=patients)

@app.route("/patients/new", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        data, errors = validate_patient(request.form)
        if errors:
            return render_template("patient_form.html", page_title="Add patient", patient=request.form,
                                   errors=errors, today=date.today().isoformat()), 400
        remarks = generate_health_remarks(data)
        create_patient(data, remarks)
        flash("Patient record created successfully.", "success")
        return redirect(url_for("index"))
    return render_template("patient_form.html", page_title="Add patient", patient={},
                           errors=[], today=date.today().isoformat())

@app.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id):
    patient = get_patient(patient_id)
    if not patient:
        flash("Patient record not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        data, errors = validate_patient(request.form)
        if errors:
            return render_template("patient_form.html", page_title="Edit patient", patient=request.form,
                                   errors=errors, today=date.today().isoformat()), 400
        # Regenerate remarks because the entered health values may have changed.
        remarks = generate_health_remarks(data)
        update_patient(patient_id, data, remarks)
        flash("Patient record updated successfully.", "success")
        return redirect(url_for("index"))
    return render_template("patient_form.html", page_title="Edit patient", patient=patient,
                           errors=[], today=date.today().isoformat())

@app.post("/patients/<int:patient_id>/delete")
def remove_patient(patient_id):
    if delete_patient(patient_id):
        flash("Patient record deleted.", "success")
    else:
        flash("Patient record not found.", "error")
    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
            host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
