import os
import redis
import requests

KEY = os.environ['OER_KEY']
HOUR_IN_SECS = 60 * 60

class RateFetcher(object):

	def __init__(self, redis):
		self._redis = redis

	def get_rate(self, currency):
		self._redis.incr('fx:meta:requests')
		self._redis.incr('fx:meta:currency_requests:' + currency)
		result = ''
		result = self._redis.get('fx:USD:' + currency)
		if not result:
			self._update_rates()
			result = self._redis.get('fx:USD:' + currency)
		return result

	def _update_rates(self):
		print 'Updating Rates'
		self._redis.incr('fx:meta:network_requests')
		url = 'https://openexchangerates.org/api/latest.json?app_id=%s' % (KEY)
		try:
		  r = requests.get(url, timeout=1)
		except requests.exceptions.RequestException:
		  return result
		if r.status_code == 200:
			rates =  r.json()['rates']
			for symbol, value in rates.items():
				self._redis.set('fx:USD:' + symbol, value, ex=HOUR_IN_SECS)
		else:
			print r.status_code

if __name__ == '__main__':
	rf = RateFetcher(redis.StrictRedis(
        host=os.environ['REDIS_HOST'], 
        port=int(os.environ['REDIS_PORT']),
        db=int(os.environ['REDIS_DB']),
        password=os.environ['REDIS_KEY'],
        decode_responses=True))
	print rf.get_rate('GBP')