from . import Resource, require_private_auth
from models.user import User
import falcon

@falcon.before(require_private_auth)
class DiscordUser(Resource):
  def on_get(self, req: falcon.Request, res: falcon.Response, user_id: str):
    user = User.by_discord_id(user_id)
    return self.send_response(res, {**user.toJSON(), 
      "guilds": [i[1] for i in user.get_club_discord_ids()]
    })