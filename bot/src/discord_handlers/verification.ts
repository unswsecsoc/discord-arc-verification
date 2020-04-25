/**
 * Verification related handlers.
 */

import { Message, DiscordAPIError } from "discord.js";
import { createVerification, APIError, APIErrorMessage } from '../services/api';


/**
 * Starts the verification process for a user. Firstly, checks if they are not a bot,
 * and then sends a DM with a link to start the verification process.
 * @param arg empty
 * @param ctx message context
 */
export async function initFromGuild(arg: string, ctx: Message): Promise<void> {
    // Only respond to requests within guilds
    if (ctx.guild == null) return;
    
    try {
        const data = await createVerification(ctx.author.id, ctx.guild.id);

        // Thumbs up react
        ctx.react('\uD83D\uDC4D');
        ctx.author.send(`Hi, you have requested ARC verification for ${ctx.guild.name}. ` + 
            'The server owner has requested that you complete this form before ' +
            'a verified role will be granted.\n\n' + 
            `Expires on: ${new Date(Date.now() + data.expires * 1000)}\n` +  data.url);
        
        return;
    } catch(e) {
        if (e instanceof APIError) {
            if (e.code === APIErrorMessage.BannedVerification) {
                ctx.react('\uD83D\uDC4D');
                ctx.author.send('Hi, the server owner has banned you from ' + 
                    'participating on this server. Please contact them to resolve ' + 
                    'this issue.');
            } else if (e.code === APIErrorMessage.AlreadyVerified) {
                return;
            }
        } else if (e instanceof DiscordAPIError) {
            if ((e as DiscordAPIError).code == 50013) {
                ctx.reply('I can\'t send you a direct message. Could you go into User Settings > ' + 
                    'Privacy & Safety and check if "Allow direct messages from server owners" ' + 
                    'is enabled.');
            }
        }
        
        throw e;
    }

}
initFromGuild.help = {
    guild: 'initiates your verification process for this server'
}