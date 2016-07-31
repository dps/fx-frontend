from flask import Flask
from flask import Response
from werkzeug.routing import BaseConverter

import oer
import os
import redis


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
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

@app.route('/metrics')
def metrics():
	response = ''
	for key in appredis.keys('fx:meta*'):
		response = response + key + ' ' + appredis.get(key) + '\n'
	return Response(response, mimetype='text/plain')

@app.route('/<regex("[A-Z]{3}"):currency>')
def index(currency):
    return str(ratefetcher.get_rate(currency))

