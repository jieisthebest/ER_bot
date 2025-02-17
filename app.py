from flask import Flask, render_template, request, flash, redirect
from datetime import datetime
import sqlite3
from flask import Flask, url_for, render_template, request, redirect, g
from datetime import datetime



# app name
app = Flask(__name__)

# Datasets
GENDER = ["Male", "Female", "Other"]
SEVERITY=["1","2","3"]

# database configuration
triage_db = sqlite3.connect('triage.db')
patient_db = sqlite3.connect('patient.db')


@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime(format)

def error(message, code=400):
    """Render message as an apology to user."""

    def escape(s):

        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", top=code, bottom=escape(message)), code





@app.route("/")
def index():
    """Default Web MD search page"""
    return render_template("index.html")


@app.route("/triage", methods=["GET", "POST"])
def triage():
    if request.method == "POST":
        return triage_processor()
    else:
        return render_template("triage.html", GENDER=GENDER, SEVERITY=SEVERITY)
<<<<<<< HEAD
=======

>>>>>>> 6195e77 (finished polishing UI and SQL flow is working now)

def triage_processor():
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    symptom = request.form.get("symptom")
    severity = request.form.get("severity")
    # Checks for input
    if not name or not age or not gender or not symptom or not severity:
        return redirect("/triage")
    #check age
    try:
        age=int(age)

    except ValueError:
        return redirect("/triage")

    patient_log = symptom
    print(type(name), type(gender), type(age), type(patient_log))
    
    #TODO CS50 sql review error placeholder mismatch 
    try:
        patient_db.execute("INSERT INTO patients (name, gender, age, date, patient_log) VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)", (name, gender, age, patient_log))
        # grabs ID from the recently created user for patient_id
        patient_id = patient_db.execute("SELECT last_insert_rowid()").fetchone()[0]
        patient_db.commmit()
    except Exception as e:

        return redirect("/triage")


    # creates array of matched item to table
    results = []
    # break query of user symptom into words to iterate and search
    symptoms = symptom.split()
    for s in symptoms:
        # get the symptom's id
        subquery = "SELECT id FROM triage WHERE symptom LIKE ?"
        results.extend(triage_db.execute(subquery, ('%' + s + '%',)).fetchall())


    if len(results) <= 0:
        flash(f"Sorry did not find your symptom {symptom}! The system has logged this case!")
        # insert an unknown symptom case at id=0
        patient_db.execute("INSERT INTO symptom_details (patient_id, symptom_id) VALUES (?, 0)", patient_id)
        # redirect to other resource to search
        return redirect("/index")
    else:
        for t in results:
            patient_db.execute("INSERT INTO symptom_details (patient_id, symptom_id) VALUES (?, ?)", (patient_id, t['id']))
            #now condition checks
            #location
            #severityfrom flask import Flask, render_template, request, flash, redirect
