import falcon
from config import web_url
from . import Resource, require_private_auth
from falcon.media.validators import jsonschema
from store.verification import EmailVerification
from views.verification import admin_verification_schema, user_verification_schema
from models.user import User as UserModel
from models.club import Club as ClubModel
from models.member import Member as MemberModel
from lib.mail import send_validation
import lib.const as const
import logging
import lib.rpc
import store.token
import time
import requests

logger = logging.getLogger(__name__)

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

        # create a signed token
        token = store.token.generate_verification(user_id, guild_id)

        self.send_response(res, {
            "url": f"{web_url}/verifications/{token}",
            "expires": store.token.EXPIRES_VERIFICATION
        })
        

class User(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, token):
        data = store.token.validate(store.token.AUD_VERIFICATION, token)

        if not data:
            raise falcon.HTTPBadRequest("InvalidToken")
        
        # check if club exists and is enabled
        club = ClubModel.by_discord_id(data["gid"])

        if not club or not club.is_enabled:
            raise falcon.HTTPBadRequest("ClubNotExists")
        
        # grab user once we verify existence of club
        user = UserModel.by_discord_id(data["uid"])

        return self.send_response(res, {
            "user_verified": user is not None,
            "club": club.toJSON(["_id", "description", "email", "name", "permalink", "website"]) 
        })
        
    @jsonschema.validate(user_verification_schema)
    def on_post(self, req: falcon.Request, res: falcon.Response, token):
        data = store.token.validate(store.token.AUD_VERIFICATION, token)

        if not data:
            raise falcon.HTTPBadRequest("InvalidToken")
        
        # check if club exists and is enabled
        club = ClubModel.by_discord_id(data["gid"])
        if not club or not club.is_enabled:
            raise falcon.HTTPBadRequest("ClubNotExists")

        if not club.verified_role_id:
            raise falcon.HTTPBadRequest("ClubNotConfigured")

        # grab user once we verify existence of club
        user = UserModel.by_discord_id(data["uid"])

        if user == None and "user" not in req.media:
            raise falcon.HTTPBadRequest("NoUserDetails")
        
        # destroy and lock token
        if not store.token.destroy(token):
            raise falcon.HTTPBadRequest("InvalidToken")

        if user == None:
            user = UserModel.create({"discord_id": data["uid"], **req.media["user"]})
        try:
            MemberModel.create({
                "user_id": user._id,
                "club_id": club._id
            })
        except Exception as e:
            logger.warn("Error creating member: ", e)

        if user.is_verified:
            lib.rpc.bot_add_roles(data["uid"], data["gid"], [club.verified_role_id])
            return self.send_response(res, {
                "user_verified": True
            })
        else:
            token = store.token.generate_validation(user._id, "zid" if user.zid else "email")
            send_validation(
                to=f"{user.zid}@unsw.edu.au" if user.zid else user.email,
                name=user.given_name,
                token=token
            )

            return self.send_response(res, {
                "user_verified": False
            })
