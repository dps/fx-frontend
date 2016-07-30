import os
import requests

KEY = os.environ['OER_KEY']

def get_rate(currency):
	result = ''
	url = 'https://openexchangerates.org/api/latest.json?app_id=%s' % (KEY)
	try:
	  r = requests.get(url, timeout=1)
	except requests.exceptions.RequestException:
	  return result
	if r.status_code == 200:
		return r.json()['rates'][currency]
	else:
		print r.status_code
	return result

if __name__ == '__main__':
	print get_rate('GBP')