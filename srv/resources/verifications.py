import falcon
from config import api_url
from . import Resource
from falcon.media.validators import jsonschema
from store.verification import UserVerification
from views.verification import admin_verification_schema
from models.user import User as UserModel
from models.club import Club as ClubModel
import requests

class Admin(Resource):
    @jsonschema.validate(admin_verification_schema)
    def on_post(self, req: falcon.Request, res: falcon.Response):
        user_id = req.media['user_id']
        guild_id = req.media['guild_id']

        club = ClubModel.by_discord_id(guild_id)

        if not club or not club.is_enabled:
            return self.send_error(res, "ClubNotExists")

        # TODO: check if user is already verified with server

        token, expires = UserVerification.create(user_id, guild_id)
        self.send_response(res, {
            "url": f"{api_url}/verifications/{token}",
            "expires": expires.seconds
        })
        

class User(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, token):
        obj = UserVerification.by_token(token)

        if not obj:
            return self.send_error(res, 'InvalidToken')
        
        # check if club exists and is enabled
        club = ClubModel.by_discord_id(obj.guild_id)

        if not club or not club.is_enabled:
            return self.send_error('ClubNotExists')
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(obj.user_id)

        return self.send_response({
            "user_confirmed": user is not None,
            "guild_id": obj.guild_id
        })
        
    
    def on_post(self, req: falcon.Request, res: falcon.Response, token):
        obj = UserVerification.by_token(token)

        if not obj:
            return self.send_error(res, 'InvalidToken', falcon.HTTP_BAD_REQUEST)
        
        # check if club exists and is enabled
        club = ClubModel.by_discord_id(obj.guild_id)
        if not club or not club.is_enabled:
            return self.send_error(res, 'ClubNotExists', falcon.HTTP_BAD_REQUEST)
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(obj.user_id)

        if user == None and "user" not in req.media:
            return self.send_error('NoUserDetails', falcon.HTTP_BAD_REQUEST)

        if user == None:
            user = UserModel.create({"discord_id": obj.user_id, **req.media["user"]})
        # TODO
        # r = requests.post("http://localhost:3000/add-roles", json={
        #     'user_id': obj.user_id, 
        #     'guild_id': obj.guild_id, 
        #     'role_ids': [club.verified_role_id]
        # }, headers={
        #     'authorization': 'Bearer srv.xxx'
        # })
        
        UserVerification.destroy(token)

        return self.send_response(res, user.toJSON())
        