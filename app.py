from flask import Flask, redirect, render_template, session, request, send_file
from datetime import datetime
import tools, os

app = Flask(__name__)
app.secret_key = "zawefkuzwvefkuwefgwef"

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def start():
    if "weather" in session and "last_weather_update" in session:
        last_update = datetime.fromisoformat(session["last_weather_update"])

        # If more than 1 hour has passed, fetch new weather data
        if (datetime.now() - last_update).total_seconds() / 3600 < 1:
            return render_template("index.html", weather=session["weather"])

    session["weather"] = tools.weather()
    session["last_weather_update"] = datetime.now().isoformat()
    return render_template("index.html", weather=session["weather"])

@app.route("/wetter")
def wetter():
    if "weather" in session and "last_weather_update" in session:
        last_update = datetime.fromisoformat(session["last_weather_update"])

        # If more than 1 hour has passed, fetch new weather data
        if (datetime.now() - last_update).total_seconds() / 3600 < 1:
            return render_template("wetter.html", weather=session["weather"])

    session["weather"] = tools.weather()
    session["last_weather_update"] = datetime.now().isoformat()
    return render_template("wetter.html", weather=session["weather"])

@app.route("/pv")
def pv():
    return render_template("pv.html")

@app.route("/slow-share")
def slow_share():
    files = list_files_in_folder(app.config['UPLOAD_FOLDER'])
    return render_template("slow_share.html", files=files)

@app.route("/slow-share/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return redirect("/message/file_not_uploaded")
    
    file = request.files['file']
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect("/slow-share")
    
    return "error"

@app.route("/slow-share/delete/<file>")
def delete(file):
    os.remove(f"files/{file}")
    return redirect("/slow-share")

@app.route("/slow-share/download/<file>")
def download(file):
    return send_file(f"files/{file}", as_attachment=True)

@app.route("/pop")
def pop():
    session.clear()
    return redirect("/")

def list_files_in_folder(folder):
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files
    except FileNotFoundError:
        return redirect("/message/dir_not_found")

if __name__ == "__main__":
    app.run(debug=True, port=5300)
