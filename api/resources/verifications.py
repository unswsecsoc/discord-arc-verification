import falcon
from config import api_url, web_url
from . import Resource, require_private_auth
from falcon.media.validators import jsonschema
from store.verification import UserVerification, EmailVerification
from views.verification import admin_verification_schema, user_verification_schema
from models.user import User as UserModel
from models.club import Club as ClubModel
from models.member import Member as MemberModel
from lib.mail import send_validation
from logging import getLogger
import lib.rpc
import requests

logger = getLogger(__name__)

@falcon.before(require_private_auth)
class Private(Resource):
    @jsonschema.validate(admin_verification_schema)
    def on_post(self, req: falcon.Request, res: falcon.Response):
        user_id = req.media['user_id']
        guild_id = req.media['guild_id']

        club = ClubModel.by_discord_id(guild_id)

        if not club or not club.is_enabled:
            raise falcon.HTTPBadRequest("ClubNotExists")

        if not club.verified_role_id:
            raise falcon.HTTPBadRequest("ClubNotConfigured")

        # check if user is already verified with server
        user = UserModel.by_discord_id(user_id)
        if user and user.is_verified and MemberModel.check_existence(user._id, club._id):
            lib.rpc.bot_add_roles(user_id, guild_id, [club.verified_role_id])
            raise falcon.HTTPBadRequest("AlreadyVerified")

        token, expires = UserVerification.create(user_id, guild_id)
        self.send_response(res, {
            "url": f"{web_url}/verifications/{token}",
            "expires": expires.seconds
        })
        

class User(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, token):
        obj = UserVerification.by_token(token)

        if not obj:
            raise falcon.HTTPBadRequest("InvalidToken")
        
        # check if club exists and is enabled
        club = ClubModel.by_discord_id(obj.guild_id)

        if not club or not club.is_enabled:
            raise falcon.HTTPBadRequest("ClubNotExists")
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(obj.user_id)

        return self.send_response(res, {
            "user_verified": user is not None,
            "club": club.toJSON(["_id", "description", "email", "name", "permalink", "website"]) 
        })
        
    @jsonschema.validate(user_verification_schema)
    def on_post(self, req: falcon.Request, res: falcon.Response, token):
        obj = UserVerification.by_token(token)

        if not obj:
            raise falcon.HTTPBadRequest("InvalidToken")
        
        # check if club exists and is enabled
        club = ClubModel.by_discord_id(obj.guild_id)
        if not club or not club.is_enabled:
            raise falcon.HTTPBadRequest("ClubNotExists")

        if not club.verified_role_id:
            raise falcon.HTTPBadRequest("ClubNotConfigured")
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(obj.user_id)

        if user == None and "user" not in req.media:
            raise falcon.HTTPBadRequest("NoUserDetails")

        if user == None:
            user = UserModel.create({"discord_id": obj.user_id, **req.media["user"]})
        
        try:
            MemberModel.create({
                "user_id": user._id,
                "club_id": club._id
            })
        except Exception as e:
            logger.warn("Error creating member: ", e)

        UserVerification.destroy(token)

        if user.is_verified:
            lib.rpc.bot_add_roles(obj.user_id, obj.guild_id, [club.verified_role_id])
            return self.send_response(res, {
                "user_verified": True
            })
        else:
            [token, expires] = EmailVerification.create(user._id)

            send_validation(
                to=f"{user.zid}@unsw.edu.au" if user.zid else user.email,
                name=user.given_name,
                link=f"{api_url}/validations/{token}",
                expires=expires
            )

            return self.send_response(res, {
                "user_verified": False
            })