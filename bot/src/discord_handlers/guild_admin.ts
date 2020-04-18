/**
 * Guild settings handlers
 */

import { Message, TextChannel } from "discord.js";
import { getClub, updateClub, getClubMembers } from "../services/api";


export async function setAdminChannel(arg: string, ctx: Message): Promise<void> {
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
setAdminChannel.help = {
    guild: '[admin] set current channel as admin channel'
}

export async function setVerificationRole(arg: string, ctx: Message): Promise<void> {
    if (!ctx.guild) return;
    if (!ctx.member.hasPermission('ADMINISTRATOR')) return;
  
    // Grab club
    const club = await getClub(ctx.guild.id);
    if (!club) return;
    if (ctx.channel.id !== club.admin_channel_id) return;

    const match = /<@&(\d+)>/g.exec(arg);
    if (match.length != 2) {
        ctx.reply("syntax error.");
        return;
    }

    const role = ctx.guild.roles.resolve(match[1]);
    if (!role) {
        ctx.reply("role doesn't exist.");
        return;
    }
    await updateClub(ctx.guild.id, 'verified_role_id', role.id);
    ctx.reply(`verified role for new users set to <@&${role.id}>`);
}
setVerificationRole.help = {
    guild: '[admin] set specified role as the role for verified users'
}

export async function listMembers(arg: string, ctx: Message): Promise<void> {
    if (!ctx.guild) return;
    if (!ctx.member.hasPermission('ADMINISTRATOR')) return;
  
    // Grab club
    const club = await getClub(ctx.guild.id);
    if (!club) return;
    if (ctx.channel.id !== club.admin_channel_id) return;
    const members = await getClubMembers(ctx.guild.id);
    
    let message = "";
    for (const i of members) {
        message += `${i.zid || i.email + ' ' + i.phone}\t\t` + 
        `${i.given_name} ${i.family_name}\t\t` + 
        `<@${i.discord_id}>\n`;
    }
    ctx.channel.send(message);
}
setVerificationRole.help = {
    guild: '[admin] list verified members in server'
}
