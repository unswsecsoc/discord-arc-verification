import falcon
from config import api_url
from . import Resource
from falcon.media.validators import jsonschema
from store.verification import EmailVerification
from models.user import User as UserModel
from models.club import Club as ClubModel
from models.member import Member as MemberModel
import lib.rpc
import logging

logger = logging.getLogger(__name__)

class User(Resource):
    def on_get(self, req: falcon.Request, res: falcon.Response, token):
        obj = EmailVerification.by_token(token)

        if not obj:
            return self.send_error(res, "InvalidToken")
        
        # check if user is already active
        user = UserModel.by_id(obj.user_id)
        if user.is_verified:
            EmailVerification.destroy(token)
            return self.send_response(res, True)
        
        user.set_verified()
        for club in user.get_club_discord_ids():
            if not club[1] or not club[2]:
                logger.warn("club id=%s is improperly configured. Skipping for now.", club[0])
                continue
            lib.rpc.bot_add_roles(user.discord_id, club[1], [club[2]])

        EmailVerification.destroy(token)

        return self.send_response(res, True)