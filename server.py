from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # My personal email. (Change to business email once created.)
    to_email = "webdev.by.tom@gmail.com"
    from_email = "webdev.by.tom@gmail.com"
    subject = f"New message from {name}"

    msg = MIMEText(f"From: {name} <{email}>\n\n{message}")
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email


    # When business email is created ensure that you also change the APP password as well.
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, os.environ.get("EMAIL_PASS"))
            server.send_message(msg)
        print("Message sent successfully.")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error: Please contact IT.", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
