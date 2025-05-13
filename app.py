import qrcode
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

tokens = {}
next_token = 1

@app.route("/")
def home():
    # Dynamically get full domain from request
    base_url = request.url_root.rstrip('/')
    qr_data = f"{base_url}/checkin"
    qr_path = "static/qr_code.png"

    # Generate QR code every time to ensure URL is correct
    os.makedirs("static", exist_ok=True)
    img = qrcode.make(qr_data)
    img.save(qr_path)

    return render_template("index.html", qr_path=qr_path)

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
