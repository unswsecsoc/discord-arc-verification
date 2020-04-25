import { Handler } from '../lib/types';
import * as VerificationHandler from './verification';
import HelpHandler from './help';
import * as GuildAdminHandler from './guild_admin';

const handlers: {[key: string]: Handler} = {
    'verify': VerificationHandler.initFromGuild,
    'avhelp': HelpHandler,
    'avsetverified': GuildAdminHandler.setVerificationRole,
    'avsetadmin': GuildAdminHandler.setAdminChannel,
    'avlistmembers': GuildAdminHandler.listMembers,
    'avwhois': GuildAdminHandler.getMember,
}

export default handlers;
export const MAX_LENGTH = Math.max(...Object.keys(handlers).map((i => i.length))) + 2;