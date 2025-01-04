from flask import Flask, render_template, request
from datetime import datetime

#app name
app = Flask(__name__)

#database configuration
triage_db = SQL("sqlite:///triage.db")
patient_db = SQL("sqlite:///patient.db")



@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime(format)

@app.route("/", methods=["GET", "POST"])
def index():
pass


@app.route("/triage", methods=["GET", "POST"])
def triage():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        symptom = request.form.get("symptom")
        severity = request.form.get("severity")
        patient_log = symptom
        #add user to database
        patient_db.execute("INSERT INTO patients (name, gender, patient_log, date, age) VALUES (?, ?, ?, CURRENT_TIMESTAMP,?)", name, gender,patient_log,age)
        #creates array of matched item to table
        results=[]
        #break query of user symptom into words to iterrate and search
        symptoms = symptom.split()
        for s in symptoms:
            subquery = "SELECT id FROM triage WHERE symptom LIKE %s" % ("%" + s + "%")
            results.extend(triage_db.execute(subquery).fetchall())

        if len(results)<=0:
            flash(f"Sorry did not find your symptom{symptom}!")
            # insert a unknown symptom or case at id=0
            return redirect("/index")
        else:
            for t in results:
                patient_db.execute("INSERT INTO symptom_details VALUES (?,?)", (t['id']))

    else:
        return render_template("triage.html")
