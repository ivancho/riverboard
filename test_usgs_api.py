import requests

URL_API = 'https://waterservices.usgs.gov/nwis/iv/'
DURANGO_SITE = '09361500'
VARS = '00060,00010'

def test_api():
    r = requests.get('{}/?site={}&format=json&indent=on&variables={}'.format(URL_API, DURANGO_SITE, VARS))
    j = r.json()
    for s in j['value']['timeSeries']:
        current = s['values'][0]['value'][0]
        print("{0}: {1} @ {2}".format(s['variable']['variableDescription'], current['value'], current['dateTime']))

if __name__ == '__main__':
    test_api()
