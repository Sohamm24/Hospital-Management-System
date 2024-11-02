from flask import Flask, render_template, request, redirect, url_for,flash
import sqlite3
import secrets
import string

app = Flask(__name__)
app.secret_key = 'HMS'

users = {
    'doctor': {'username': 'doc1', 'password': 'pass123'},
    'patient': {'username': 'pat1', 'password': 'pass123'},
    'management': {'username': 'man1', 'password': 'pass123'}
}

def create_doctors_table():
    conn = sqlite3.connect('doctors.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            experience INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'doctor':
            return redirect(url_for('doctor_login'))
        elif role == 'patient':
            return redirect(url_for('patient_login'))
        elif role == 'management':
            return redirect(url_for('management_login'))
    return render_template('login.html')

@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users['doctor']['username'] and password == users['doctor']['password']:
            return redirect(url_for('doctor_dashboard'))
        else:
            return "Invalid credentials for Doctor"
    return render_template('login_form.html', role="Doctor")

@app.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users['patient']['username'] and password == users['patient']['password']:
            return redirect(url_for('patient_dashboard'))
        else:
            return "Invalid credentials for Patient"
    return render_template('login_form.html', role="Patient")

@app.route('/management_login', methods=['GET', 'POST'])
def management_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users['management']['username'] and password == users['management']['password']:
            return redirect(url_for('management_dashboard'))
        else:
            return "Invalid credentials for Management"
    return render_template('login_form.html', role="Management")


@app.route('/doctor_dashboard')
def doctor_dashboard():
    return "Welcome to Doctor's Dashboard"

@app.route('/patient_dashboard')
def patient_dashboard():
    return "Welcome to Patient's Dashboard"

@app.route('/management_dashboard')
def management_dashboard():
    return  render_template('management.html')

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['doctorName']
        specialization = request.form['specialization']
        email = request.form['email']
        phone = request.form['phone']
        experience = request.form['experience']

    
        username = name.lower().replace(" ", "") + secrets.token_hex(3)

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for i in range(8))

        try:
            conn = sqlite3.connect('doctors.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO doctors (name, specialization, email, phone, experience, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, specialization, email, phone, experience, username, password))
            conn.commit()
            flash(f"Doctor added successfully! Username: {username}, Password: {password}", "success")
        except Exception as e:
            flash(f"Error occurred: {str(e)}", "danger")
            print(f"Database Error: {str(e)}") 
        finally:
            conn.close()

        return redirect(url_for('add_doctor'))
    
    return render_template('addDoctor.html')


if __name__ == '__main__':
      create_doctors_table()
      app.run(debug=True)

