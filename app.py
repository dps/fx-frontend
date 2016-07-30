from flask import Flask
import oer
import os
import redis

app = Flask(__name__)
app.debug = True

appredis = None
ratefetcher = None

@app.before_first_request
def init():
    global appredis, ratefetcher
    print '+init'
    appredis = redis.StrictRedis(
        host=os.environ['REDIS_HOST'], 
        port=int(os.environ['REDIS_PORT']),
        db=int(os.environ['REDIS_DB']),
        password=os.environ['REDIS_KEY'],
        decode_responses=True)
    ratefetcher = oer.RateFetcher(appredis)
    print '-init ', appredis, ratefetcher

@app.route('/<currency>')
def index(currency):
    return str(ratefetcher.get_rate(currency))

