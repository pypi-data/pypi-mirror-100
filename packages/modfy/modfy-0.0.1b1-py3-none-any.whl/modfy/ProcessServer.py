import json
import requests
from modfy.config import Config


class ProcessServer:

    def __init__(self, operation):
        self.operation = operation
        config = Config()
        self.API_URL = config.API_URL

    def process(self, token):
        try:
            jsonOp = json.dumps(self.operation.serverOperationJson)
            response = requests.post(self.API_URL + '/process', data=dict(
                operation=jsonOp, token=token, test=True), files=dict(video=self.operation.inputFiles[0]))
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print('Error making process request', e)
            raise SystemExit(e)
