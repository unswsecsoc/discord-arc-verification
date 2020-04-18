import falcon
from . import Resource
from config import version

class InfoResource(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response):
        self.send_response(res, {'version': version})