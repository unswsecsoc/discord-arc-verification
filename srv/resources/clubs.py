from models.club import Club
import falcon
from falcon.media.validators import jsonschema
from views.club import club_schema
from . import Resource, require_private_auth
from lib.recaptcha import validate_recaptcha

@falcon.before(require_private_auth)
class ClubsListResource(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response):
        self.send_response(res, [i.toJSON() for i in Club.get_all()])
    
    @jsonschema.validate(club_schema)
    def on_post(self, req: falcon.Request, res: falcon.Response):
        obj = Club.create(req.media)
        self.send_response(res, obj.toJSON())

class ClubResource(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, club_id):
        if club_id.isnumeric():
            obj = Club.by_id(club_id)
        else:
            obj = Club.by_permalink(club_id)
        if obj and obj.is_enabled:
            return self.send_response(res, obj.toJSON(["_id", "description", "email", "name", "permalink", "website"]) )
        return self.send_404(res)

