from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import os
from google.oauth2 import service_account
import gspread
import pandas as pd

app = Flask(__name__)

# Path to your credential JSON file
credential_file = os.path.join(os.getcwd(), 'credentials/spartan-soccer-2db8e2aa941f.json')

# Load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    credential_file, scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
)
# Create a client to interact with Google Sheets API
client = gspread.authorize(credentials)

# Open the Google Spreadsheet
spreadsheet = client.open('Spartanstats')  

# Select the specific sheet within the spreadsheet
sheet = spreadsheet.sheet1  # Assuming the data is on the first sheet

# Fetch all the values from the sheet
data = sheet.get_all_values()

# Create a DataFrame using the fetched data
df = pd.DataFrame(data[1:], columns=data[0])

# Define a route to render the players page
@app.route("/players")
def players():
    # Convert DataFrame to list of dictionaries
    player_data = df.to_dict(orient='records')

    # Render the players.html template and pass the player data
    return render_template("players.html", players=player_data)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_contact_form():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Send email
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = email  # Set the sender's email address
    msg["To"] = "expertprep2015@gmail.com"  # Set your email address as the recipient

    # Set up SMTP server and send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("expertprep2015@gmail.com", "pbetzfynskbsncye")
        smtp.send_message(msg)

    return "Thank you for your message!"


if __name__ == "__main__":
    app.run(debug=True)
