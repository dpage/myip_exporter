import datetime
import logging
import os

import requests as requests
from flask import Flask
from prometheus_client import make_wsgi_app, Gauge, Info
from waitress import serve

app = Flask("MyIP-Exporter")

# Setup logging values
format_string = 'level=%(levelname)s datetime=%(asctime)s %(message)s'
logging.basicConfig(encoding='utf-8',
                    level=logging.DEBUG,
                    format=format_string)

# Disable Waitress Logs
log = logging.getLogger('waitress')
log.disabled = True

cache_seconds = int(os.environ.get('MYIP_CACHE_TIMEOUT', 5))
cache_until = datetime.datetime.fromtimestamp(0)

# Create Metric
status = Gauge('myip_status', 'MyIP status and info',
               ['country',
                'country_code',
                'region',
                'region_name',
                'city',
                'zip',
                'timezone',
                'isp',
                'org',
                'asn',
                'longitude',
                'latitude',
                'query'])


def get_myip():
    try:
        data = requests.get('http://ip-api.com/json/', timeout=10).json()
    except:
        pass

    return data


@app.route("/metrics")
def metrics():
    global cache_until

    if datetime.datetime.now() > cache_until:
        data = get_myip()

        status.labels(country=data['country'],
                      country_code=data['countryCode'],
                      region=data['region'],
                      region_name=data['regionName'],
                      city=data['city'],
                      zip=data['zip'],
                      timezone=data['timezone'],
                      isp=data['isp'],
                      org=data['org'],
                      asn=data['as'],
                      longitude=data['lon'],
                      latitude=data['lat'],
                      query=data['query']).set(1 if data['status'] == 'success' else 0)

        logging.info(data)

        cache_until = datetime.datetime.now() + datetime.timedelta(
            seconds=cache_seconds)

    return make_wsgi_app()


@app.route("/")
def index():
    return ("<h1>Welcome to MyIp-Exporter.</h1>" +
            "<p>Click <a href='/metrics'>here</a> to see metrics.</p>")


if __name__ == '__main__':
    PORT = os.getenv('MYIP_PORT', 9691)
    logging.info("Starting MyIP-Exporter on http://localhost:" +
                 str(PORT))
    serve(app, host='0.0.0.0', port=PORT)
