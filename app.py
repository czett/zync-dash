from flask import Flask, redirect, render_template, session
import tools

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5300)