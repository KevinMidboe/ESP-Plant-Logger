import json
import urequests

headers = { 'Content-Type': 'application/json' }
url = 'http://localhost.com:9200'
index = 'botany'

def logger(msg, data=None):
  uri = '/'.join([url, index, '_doc'])
  r = urequests.post(uri, data=json.dumps(data), headers=headers)

  print(r.status_code)
  text = r.text
  r.close()

  return text
