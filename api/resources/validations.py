import falcon
import logging
from falcon.media.validators import jsonschema

import lib.mail
import lib.rpc
from config import web_url
import lib.const as const
from . import Resource
import store.token
from models.user import User as UserModel
from models.club import Club as ClubModel
from models.member import Member as MemberModel

logger = logging.getLogger(__name__)

def generate_token(user_id):
    return store.token.generate(TOKEN_AUD, const.VALIDATION_EXPIRES, {
        "uid": user_id
    })


class User(Resource):
    def on_post(self, req: falcon.Request, res: falcon.Response, token):
        # check if token is valid and consume
        data = store.token.validate_destroy(store.token.AUD_VALIDATION, token)

        if not data:
            raise falcon.HTTPBadRequest("InvalidToken")

        # check if user is already active
        user = UserModel.by_id(data["uid"])
        if user.is_verified:
            return self.send_response(res, {})
        
        user.set_verified()
        for club in user.get_club_discord_ids():
            if not club[1] or not club[2]:
                logger.warn("club id=%s is improperly configured. Skipping for now.", club[0])
                continue
            lib.rpc.bot_add_roles(user.discord_id, club[1], [club[2]])

        return self.send_response(res, {})