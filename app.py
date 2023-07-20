from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


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
