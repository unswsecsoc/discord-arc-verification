import falcon
from config import api_url
from . import Resource
from falcon.media.validators import jsonschema
from store.verification import UserVerification, EmailVerification
from views.verification import admin_verification_schema
from models.user import User as UserModel
from models.club import Club as ClubModel
from models.member import Member as MemberModel
import lib.rpc
import requests

class Admin(Resource):
    @jsonschema.validate(admin_verification_schema)
    def on_post(self, req: falcon.Request, res: falcon.Response):
        user_id = req.media['user_id']
        guild_id = req.media['guild_id']

        club = ClubModel.by_discord_id(guild_id)

        if not club or not club.is_enabled:
            return self.send_error(res, "ClubNotExists", falcon.HTTP_BAD_REQUEST)

        if not club.verified_role_id:
            return self.send_error(res, "ClubNotConfigured", falcon.HTTP_BAD_REQUEST)

        # check if user is already verified with server
        user = UserModel.by_discord_id(user_id)
        if user and MemberModel.check_existence(user._id, club._id):
            return self.send_error(res, "AlreadyVerified", falcon.HTTP_BAD_REQUEST)

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
            return self.send_error("ClubNotExists")
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(obj.user_id)

        return self.send_response(res, {
            "user_validated": user is not None,
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

        if not club.verified_role_id:
            return self.send_error(res, "ClubNotConfigured", falcon.HTTP_BAD_REQUEST)
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(obj.user_id)

        if user == None and "user" not in req.media:
            return self.send_error('NoUserDetails', falcon.HTTP_BAD_REQUEST)

        if user == None:
            user = UserModel.create({"discord_id": obj.user_id, **req.media["user"]})
        
        MemberModel.create({
            "user_id": user._id,
            "club_id": club._id
        })
        
        UserVerification.destroy(token)

        if user.is_verified:
            lib.rpc.bot_add_roles(obj.user_id, obj.guild_id, [club.verified_role_id])
            return self.send_response(res, {
                "user_verified": True
            })
        else:
            [token, expires] = EmailVerification.create(user._id)
            print(token)
            return self.send_response(res, {
                "user_verified": False
            })