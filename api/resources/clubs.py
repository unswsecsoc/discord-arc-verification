from models.club import Club
import falcon
from falcon.media.validators import jsonschema
from views.club import club_schema, club_guild_update_schema
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

@falcon.before(require_private_auth)
class ClubMemberResource(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, guild_id: str):
        obj = Club.by_discord_id(guild_id)
        if not obj:
            raise falcon.HTTPNotFound()
        self.send_response(res, [i.toJSON() for i in obj.get_members()])

@falcon.before(require_private_auth)
class ClubByGuildResource(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, guild_id: str):
        obj = Club.by_discord_id(guild_id)
        if not obj:
            raise falcon.HTTPNotFound()
        self.send_response(res, obj.toJSON())
    
    """
    Updates a discord related property in guild
    """
    @jsonschema.validate(club_guild_update_schema)
    def on_put(self, req: falcon.Request, res: falcon.Response, guild_id: str):
        obj = Club.by_discord_id(guild_id)
        if not obj:
            raise falcon.HTTPNotFound()
        obj.update_value(req.media['key'], req.media['value'])
        return self.send_response(res, True)

class ClubResource(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, club_id: str):
        if club_id.isnumeric():
            obj = Club.by_id(club_id)
        else:
            obj = Club.by_permalink(club_id)
        if obj and obj.is_enabled:
            return self.send_response(res, obj.toJSON(["_id", "description", "email", "name", "permalink", "website"]))
        
        raise falcon.HTTPNotFound()

