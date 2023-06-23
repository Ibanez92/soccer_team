from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Welcome to the soccer team website!'

@app.route('/players')
def players():
    return 'List of players'

@app.route('/schedule')
def schedule():
    return 'Team schedule'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit_contact_form', methods=['GET'])
def contact():
    return render_template('home.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Send email
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = email  # Set the sender's email address
    msg['To'] = 'JavierIbanez92@outlook.com'  # Set your email address as the recipient

    # Set up SMTP server and send email
    with smtplib.SMTP('outlook.office365.com', 993) as smtp:
        smtp.login('JavierIbanez92@outlook.com', 'Oleo0507!')
        smtp.send_message(msg)

    return "Thank you for your message!"


if __name__ == '__main__':
    app.run(debug=True)