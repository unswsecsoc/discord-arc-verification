import falcon

import lib.errors

from resources.info import InfoResource
from resources.clubs import ClubsListResource, ClubResource

def handle_404(req: falcon.Request, res: falcon.Response):
    res.status = falcon.HTTP_NOT_FOUND
    res.media = {
        'status': False,
        'error': 'not found'
    }

def handle_errors(ex, req: falcon.Request, res: falcon.Response, params: any):
    res.status = ex.code
    res.media = {
        'status': False,
        'error': ex.message
    }
        

application = falcon.API()
application.add_route('/info', InfoResource())

application.add_route('/clubs', ClubsListResource())
application.add_route('/clubs/{club_id}', ClubResource())

application.add_sink(handle_404, '')
application.add_error_handler(lib.errors.BaseError, handle_errors)
