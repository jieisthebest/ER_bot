from flask import Flask, render_template, request, flash, redirect
from datetime import datetime
from cs50 import SQL
import sqlite3

# Connect to the database
conn = sqlite3.connect('patient.db')
patient_db = conn.cursor()
#I am not sure about this


# app name
app = Flask(__name__)

#Datasets
GENDER = ["Male", "Female", "Other"]
AGE =["0-17","18-64","65+"]
SEVERITY=["1","2","3"]

# database configuration
triage_db = SQL("sqlite:///triage.db")
patient_db = SQL("sqlite:///patient.db")


@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime(format)

@app.route("/")
def index():
    """Default Web MD search page"""
    return render_template("index.html")


@app.route("/triage", methods=["GET", "POST"])
def triage():
    if request.method == "POST":
        triage_processor()
    else:
        return render_template("triage.html", GENDER=GENDER, SEVERITY=SEVERITY,AGE=AGE)

def triage_processor():
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    symptom = request.form.get("symptom")
    severity = request.form.get("severity")
    if not name or not age or not gender or not symptom or not severity:
        flash(f"Enter all details please!")

    patient_log = symptom
    # add user to database
    patient_db.execute("INSERT INTO patients (name, gender, age, date, patient_log) VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)", (name, gender, age, patient_log))
    conn.commit()
    #grabs ID from the recently created user for patient_id
    patient_id = patient_db.execute("SELECT last_insert_rowid()").fetchone()[0]
    # creates array of matched item to table
    results = []
    # break query of user symptom into words to iterrate and search
    symptoms = symptom.split()
    for s in symptoms:
        # get the symptom's id
        subquery = "SELECT id FROM triage WHERE symptom LIKE %s" % ("%" + s + "%")
        results.extend(triage_db.execute(subquery).fetchall())

        if len(results) <= 0:
            flash(f"Sorry did not find your symptom{symptom}! The system has logged this case!")
            # insert a unknown symptom or case at id=0
            patient_db.execute("INSERT INTO symptom_details (patient_id, symptom_id) VALUES (?,0)", patient_id)
            # redirect to other ressource to search
            return redirect("/index")
        else:
            for t in results:
                patient_db.execute("INSERT INTO symptom_details (patient_id, symptom_id) VALUES (?,?)" , patient_id, (t['id']))
            #now condition checks
            #location
            #severity




@app.route("/history", methods=["GET", "POST"])
def history():
    """Show history of transactions"""
    #not sure how to combine 2 tables of various data review SQL
    #history = patient_db.execute("SELECT  FROM patients WHERE patient_id = ? ORDER BY date DESC", patient_db.execute("SELECT last_insert_rowid()").fetchone()[0])
    #return render_template("history.html", history=history)
