from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/players')
def players():
    return render_template('players.html')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET'])
def contact():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Send email
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = email  # Set the sender's email address
    msg['To'] = 'expertprep2015@gmail.com'  # Set your email address as the recipient

    # Set up SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('expertprep2015@gmail.com', 'pbetzfynskbsncye')
        smtp.send_message(msg)

    return "Thank you for your message!"


if __name__ == '__main__':
    app.run(debug=True)