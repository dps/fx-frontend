from flask import Flask
import oer

app = Flask(__name__)
app.debug = True

@app.route('/<currency>')
def index(currency):
    return str(oer.get_rate(currency))

