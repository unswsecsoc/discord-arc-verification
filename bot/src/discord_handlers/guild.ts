/**
 * Guild settings handlers
 */

import { Message, Role } from "discord.js";


export async function setAdminChannel(arg: string, ctx: Message) {
  if (!ctx.guild) return;
  if (!ctx.member.hasPermission('ADMINISTRATOR')) return;
}

export async function setVerificationRole(arg: string, ctx: Message) {
  if (!ctx.guild) return;
  if (!ctx.member.hasPermission('ADMINISTRATOR')) return;
  let role: Role;

  role = ctx.guild.roles.resolve(arg);
  if (!role) return ctx.reply("Role doesn't exist.");
  ctx.reply(role.name);
}