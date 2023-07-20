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
spreadsheet = client.open('Your Spreadsheet Name')

# Select the specific sheet within the spreadsheet
sheet = spreadsheet.worksheet('Sheet1')  # Replace 'Sheet1' with your actual sheet name

# Read the data from the sheet into a pandas DataFrame
data = sheet.get_all_values()
headers = data[0]
rows = data[1:]
df = pd.DataFrame(rows, columns=headers)

# Process the DataFrame to generate player cards dynamically
for index, row in df.iterrows():
    player_name = row['Player Name']
    goals = row['Goals']
    shots = row['Shots']
    assists = row['Assists']
    matches_played = row['Matches Played']

    # Generate player card dynamically using the retrieved data
    # Your code here to generate and display player cards

# Rest of your Flask application code

@app.route("/players")
def players():
    # Read the CSV file using pandas
    df = pd.read_csv("data/players.csv")

    # Generate player cards
    player_cards = []
    for _, row in df.iterrows():
        name = row["Name"]
        goals = row["Goals"]
        # Extract other relevant columns

        # Generate player card HTML
        player_card_html = f"""
        <div class="card-container">
            <div class="player-card">
                <img src="player-image.jpg" alt="Player Image" class="player-image">
                <div class="player-info">
                    <h3 class="player-name">Player Name</h3>
                    <p class="player-stats">Goals:
                        <span class="goal-count">10</span>
                    </p>
                    <p class="player-stats">Shots:
                        <span class="shot-count">20</span>
                    </p>
                    <p class="player-stats">Assists:
                        <span class="assist-count">5</span>
                    </p>
                    <p class="player-stats">Matches Played:
                        <span class="matches-played">15</span>
                    </p>
                </div>
            </div>
        """
        player_cards.append(player_card_html)
    return render_template("players.html", player_cards=player_cards)


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
