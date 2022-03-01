import json
import threading
import falcon

class Snake:
    def __init__(self):
        print("Starting snake")
        self.iteration_float = 0
        self.iteration_step = 0.00000005
        self.main_thread = threading.Thread(target = self.operate_snake, args=())
        self.main_thread.start()

    def operate_snake(self):
        while True:
            self.iteration_float += self.iteration_step

    def iteration(self):
        return int(self.iteration_float)
    
    def on_get(self, req, resp):
        payload = {}
        payload['iteration'] = self.iteration()
        resp.text = json.dumps(payload)
        resp.status = falcon.HTTP_200
