from flask import Flask, render_template, request

#app name
app = Flask(__name__)

#database configuration
triage_db = SQL("sqlite:///triage.db")
patient_db = SQL("sqlite:///patient.db")

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

        #add user to database
        patient_db.execute("INSERT INTO patients (name, gender) VALUES (?, ?)", name, gender)


        # search in database for symptoms
        search = triage_db.execute("SELECT * FROM triage WHERE symptom LIKE ?","%" + symptom +"%")
        if len(search)<=0:
            flash(f"Sorry did not find your symptom{symptom}!")
            return redirect("/index")
        else:
            for row in search:
                patient_db.execute("INSERT INTO symptom_details("SELECT id FROM triage WHERE symptom LIKE ?","%" + symptom +"%")

        # add symptoms

    else:
        return render_template("triage.html")
