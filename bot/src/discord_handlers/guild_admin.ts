/**
 * Guild settings handlers
 */

import { Message, Role, TextChannel } from "discord.js";
import { getClub, updateClub } from "../services/api";


export async function setAdminChannel(arg: string, ctx: Message) {
  if (!ctx.guild) return;
  if (!ctx.member.hasPermission('ADMINISTRATOR')) return;

  // Grab club
  const club = await getClub(ctx.guild.id);
  const newChannel = new TextChannel(ctx.guild, {id: ctx.channel.id});
  const oldChannel = new TextChannel(ctx.guild, {id: club.admin_channel_id});
  if (!club || club.admin_channel_id === ctx.channel.id) return;
  await updateClub(ctx.guild.id, 'admin_channel_id', ctx.channel.id);
  ctx.reply('admin channel updated to the current channel');


  if (oldChannel) {
    oldChannel.send(`<@${ctx.author.id}> changed the admin channel to <#${newChannel.id}>`);
  }
}

export async function setVerificationRole(arg: string, ctx: Message) {
  if (!ctx.guild) return;
  if (!ctx.member.hasPermission('ADMINISTRATOR')) return;
  
  // Grab club
  const club = await getClub(ctx.guild.id);
  if (!club) return;
  if (ctx.channel.id !== club.admin_channel_id) return;

  const match = /<@&(\d+)>/g.exec(arg);
  if (match.length != 2) {
    return ctx.reply("syntax error.");
  }

  const role = ctx.guild.roles.resolve(match[1]);
  if (!role) return ctx.reply("role doesn't exist.");
  await updateClub(ctx.guild.id, 'verified_role_id', role.id);
  ctx.reply(`verified role for new users set to <@&${role.id}>`);
}