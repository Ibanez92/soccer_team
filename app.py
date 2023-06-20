from flask import Flask
from flask import render_template

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

if __name__ == '__main__':
    app.run(debug=True)