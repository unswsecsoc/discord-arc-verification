import * as config from '../config';
import { Client } from 'discord.js';
import handlers from '../discord_handlers';
import { getClub } from './api';

const client = new Client();

/*
 * Set up Discord
 */
client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    // client.user.setPresence({
    //     activity: {
    //         name: 'type !avhelp',
    //         type: 'PLAYING',
    //         url: config.BOT_URL
    //     }
    // });
});

client.on('guildCreate', async (guild) => {
    try {
        const club = await getClub(guild.id);
        if (!club) guild.leave();
        console.log(`guild ${guild.name}, id: ${guild.id} not in database, leaving...`);
    } catch (e) {
        guild.leave();
        console.error(`Something went wrong when joining guild ${guild.name} id:${guild.id}`, e);
    }
});

client.on('message', async (ctx) => {
    // Don't respond to bots
    if (ctx.author.bot) return;

    // for speed, don't need to split the whole string
    const idxSpace = ctx.content.indexOf(' ');
    const cmd = ctx.content.substr(0, idxSpace == -1 ? ctx.content.length : idxSpace);
    const arg = ctx.content.substr(idxSpace == -1 ? ctx.content.length : idxSpace + 1);
    if (cmd[0] == '!' && handlers[cmd.substr(1)]) {
        try {
            return await handlers[cmd.substr(1)](arg, ctx);
        } catch (e) {
            ctx.reply('An unknown error occurred and our devs have been notified');
            console.error('Discord handler error:', e.stack);
        }
    }
});

client.login(config.DISCORD_TOKEN)
    .catch((e) => {
        console.error("A fatal error occurred: ", e)
        process.exit(1);
    });

export default client;