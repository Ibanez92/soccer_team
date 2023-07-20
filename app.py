from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import os
from google.oauth2 import service_account
import gspread
import pandas as pd

app = Flask(__name__)

# Path to your credential JSON file
credential_file = os.path.join(os.getcwd(), 'credentials/credentials/spartan-soccer-0861efb1932a.json')

# Load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    credential_file, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

# Create a client to interact with Google Sheets API
client = gspread.authorize(credentials)

# Open the Google Spreadsheet
spreadsheet = client.open('Spartan stats')  # Replace with your actual spreadsheet name

# Select the specific sheet within the spreadsheet
sheet = spreadsheet.sheet1  # Assuming the data is on the first sheet

# Fetch all the values from the sheet
data = sheet.get_all_values()

# Create a DataFrame using the fetched data
df = pd.DataFrame(data[1:], columns=data[0])

# Process the DataFrame to generate player cards dynamically
for _, row in df.iterrows():
    player_name = row['Name']
    goals = row['Goals']
    shots = row['Shots']
    assists = row['Assists']
    matches_played = row['Matches Played']

    # Generate player card dynamically using the retrieved data
    # Your code here to generate and display player cards

# Rest of your Flask application code

@app.route("/players")
def players():
    # Convert DataFrame to list of dictionaries
    player_data = df.to_dict(orient='records')

    # Render the players.html template and pass the player data
    return render_template("players.html", players=player_data)

@app.route("/")
def home():
    return render_template("index.html")


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
