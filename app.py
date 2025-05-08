import qrcode
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Generate the QR code once and save to static folder
QR_DATA = "http://localhost:5000/checkin"
QR_PATH = "static/qr_code.png"
if not os.path.exists(QR_PATH):
    os.makedirs("static", exist_ok=True)
    img = qrcode.make(QR_DATA)
    img.save(QR_PATH)

# Token storage
tokens = {}
next_token = 1

@app.route("/")
def home():
    return render_template("index.html", qr_path=QR_PATH)

@app.route("/scan")
def scan():
    return redirect(url_for("checkin"))

@app.route("/checkin")
def checkin():
    global next_token
    user_id = request.remote_addr
    if user_id not in tokens:
        tokens[user_id] = next_token
        next_token += 1
        return render_template("token.html", token=tokens[user_id], status="Checked In ✅")
    else:
        token = tokens.pop(user_id)
        return render_template("released.html", token=token, status="Checked Out ✅")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
