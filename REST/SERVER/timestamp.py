import json
import arrow
import falcon

class Timestamp(object):
	def on_get(self, req, resp):
		payload = {}
		payload['utc'] = arrow.utcnow().format('YYYY-MM-DD HH:mm:SS')
		payload['field2'] = "This is a field #2"
		resp.text = json.dumps(payload)
		resp.status = falcon.HTTP_200
