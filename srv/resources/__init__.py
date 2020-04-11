import falcon

class Resource(object):
    def send_response(self, res: falcon.Response, data: any = None, status: falcon.HTTPStatus = falcon.HTTP_OK) -> None:
        res.status = status
        res.media = {
            "data": data
        }

    def send_error(self, res: falcon.Response, error: str, status: falcon.HTTPStatus = falcon.HTTP_INTERNAL_SERVER_ERROR) -> None:
        res.status = status
        res.media = {
            'error': error
        }
        
    def send_404(req: falcon.Request, res: falcon.Response):
        res.status = falcon.HTTP_NOT_FOUND
        res.media = {
            'error': 'not found'
        }