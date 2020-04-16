import falcon

import lib.errors
import lib.db
import lib.redis

from resources.info import InfoResource
from resources.clubs import ClubsListResource, ClubResource
import resources.validations
import resources.verifications

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

application.add_route('/priv/clubs', ClubsListResource())
application.add_route('/clubs/{club_id}', ClubResource())

application.add_route('/priv/verifications', resources.verifications.Private())
application.add_route('/verifications/{token}', resources.verifications.User())
application.add_route('/validations/{token}', resources.validations.User())

application.add_sink(handle_404, '')
application.add_error_handler(lib.errors.BaseError, handle_errors)
