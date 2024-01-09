from flask import Flask,jsonify,render_template_string, send_from_directory, request,Response,render_template
import subprocess
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
import sqlite3


app = Flask(__name__)
app.config['UPLOAD_FOLDER']="/home/kali/Desktop/upload"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/")     
def main_page():
    return render_template ("index.html")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html", error=None)
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #if not username or not passwd:                             
            #error = "Please fill out both username and password fields"    <-- keine abfrage
            #return render_template("index.html", error=error)

        # Verbindung zur Datenbank herstellen
        connection = sqlite3.connect("unsafe-test.db")
        cursor = connection.cursor()

        # SQL-Abfrage ausführen
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        user_data = cursor.fetchone()

        # Verbindung schließen
        connection.close()

        # Überprüfen, ob ein Benutzer gefunden wurde
        if user_data:
            return render_template("login.html") #news.html
        else:
            error = "Invalid username or password"
            return render_template("index.html", error=error)

@app.route("/user/<string:name>")
def search_user(name, username, passwd):
    try:
        # Verbindung zur Datenbank herstellen
        connection = sqlite3.connect("unsafe-test.db")
        cursor = connection.cursor()

        # SQL-Abfrage ausführen
        cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + passwd + "'")
        #cursor.execute("SELECT * FROM users WHERE username = ?", (name,)) <-- sicher
        user_data = cursor.fetchall()

        # Verbindung schließen
        connection.close()

        # Überprüfen, ob ein Benutzer gefunden wurde
        if user_data:
            # Hier kannst du die Benutzerdaten nach Bedarf verarbeiten
            return jsonify(data=user_data), 200
        else:
            return jsonify(data=f"Benutzer '{name}' nicht gefunden"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


        
@app.route("/user_pass_control")
def user_pass_control():
    import re
    username=request.form.get("username")
    password=request.form.get("password")
    if re.search(username,password):
        return jsonify(data="Password include username"), 200
    else:
        return jsonify(data="Password doesn't include username"), 200

@app.route('/route')
def route():
    content_type = request.args.get("Content-Type")
    response = Response()
    headers = Headers()
    headers.add("Content-Type", content_type)
    response.headers = headers
    return response

@app.route("/get_users")
def get_users():
    try:
        hostname = request.args.get('hostname')
        command = "dig " + hostname
        data = subprocess.check_output(command, shell=True)
        return data
    except:
        data = str(hostname) + " username didn't found"
        return data
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8084, debug= True)

connection = {}
max_con = 50

    
#für mich unwichtig

