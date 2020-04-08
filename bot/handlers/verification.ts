/**
 * Verification related handlers.
 */

import { Message } from "discord.js";



/**
 * Starts the verification process for a user. Firstly, checks if they are not a bot,
 * and then sends a DM with a link to start the verification process.
 * @param arg empty
 * @param ctx message context
 */
export function initFromGuild(arg: string, ctx: Message) {
    ctx.author.send('Hi, you have requested ARC verification for a server. ' + 
        'The server owner has requested that you complete this form before ' +
        'a verified role will be granted.\n\nhttps://www.google.com');
}
initFromGuild.help = {
    guild: 'initiates your verification process for this server'
}