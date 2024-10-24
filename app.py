from flask import Flask, redirect, render_template, session
from datetime import datetime
import tools

app = Flask(__name__)
app.secret_key = "zawefkuzwvefkuwefgwef"

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

@app.route("/pop")
def pop():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5300)
