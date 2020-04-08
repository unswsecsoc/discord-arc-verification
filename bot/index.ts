import * as config from './config';
import { Client, Message } from 'discord.js';
import handlers from './handlers';

const client = new Client();



client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
  client.user.setPresence({
    activity: {
      name: 'type !avhelp',
      type: 'PLAYING',
      url: config.BOT_URL
    }
  });
});

client.on('message', (ctx: Message) => {
  // Don't respond to bots
  if (ctx.author.bot) return;

  // for speed, don't need to split the whole string
  const idxSpace = ctx.content.indexOf(' ');
  const cmd = ctx.content.substr(0, idxSpace == -1 ? ctx.content.length : idxSpace);
  const arg = ctx.content.substr(idxSpace == -1 ? ctx.content.length : idxSpace + 1);
  if (cmd[0] == '!' && handlers[cmd.substr(1)]) {
    return handlers[cmd.substr(1)](arg, ctx);
  }
});

client.login(config.DISCORD_TOKEN)
  .catch((e) => {
    console.error("A fatal error occurred: ", e)
    process.exit(1);
  });
