import falcon
import waitress
from timestamp import Timestamp
from snake import Snake

api = falcon.App()
timestamp = Timestamp()
snake = Snake()
api.add_route('/time', timestamp)
api.add_route('/snake', snake)

waitress.serve(api, listen='0.0.0.0:5003')
