import { Message } from "discord.js";
import handlers, { MAX_LENGTH } from './index';
import { DiscordObjectType } from "../types";
import { BOT_URL } from "../config";

export default function handler(arg: string, ctx: Message) {
    if (!ctx.guild) {
        return collateHelp(DiscordObjectType.USER, ctx);
    }
    return collateHelp(DiscordObjectType.GUILD, ctx);
}
handler.help = {
    user: 'shows this help message',
    guild: 'shows this help message'
};

function collateHelp(type: DiscordObjectType, ctx: Message) {
    let message = '```\nARC Verification Bot\n'
                     + '====================\n'
                     + `${BOT_URL}\n\n`;
    for (const i of Object.keys(handlers)) {
        if (handlers[i].help && handlers[i].help[type]) {
            message += `!${i.padEnd(MAX_LENGTH, ' ')}${handlers[i].help[type]}\n`;
        }
    }

    return ctx.reply(message + '```');
}