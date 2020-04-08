import { Message } from "discord.js";
import handlers, { MAX_LENGTH } from './index';
import { BOT_URL } from "../config";
import { DiscordObjectType } from "../types";

// Only generate the help message once
let helpMessage = '';
function generateHelpMessage() {
    helpMessage = '```\nARC Verification Bot\n'
                     + '====================\n'
                     + `Source: ${BOT_URL}\n\n`;
    let guildCommands = '';
    let userCommands = '';
    for (const i of Object.keys(handlers)) {
        if (!handlers[i].help) continue;
        if (handlers[i].help[DiscordObjectType.GUILD])
            guildCommands += `!${i.padEnd(MAX_LENGTH, ' ')}` + 
                `${handlers[i].help[DiscordObjectType.GUILD]}\n`;
        if (handlers[i].help[DiscordObjectType.USER])
            userCommands += `!${i.padEnd(MAX_LENGTH, ' ')}` + 
            `${handlers[i].help[DiscordObjectType.USER]}\n`;
    }
    helpMessage += 'Server Commands\n' +
                   '---------------\n' + guildCommands + '\n' + 
                   'User Commands\n' +
                   '-------------\n' + userCommands + '```';
}

export default function handler(arg: string, ctx: Message) {
    if (!helpMessage) generateHelpMessage();

    return ctx.author.send(helpMessage);
}
handler.help = {
    user: 'shows this help message',
    guild: 'shows this help message'
};

