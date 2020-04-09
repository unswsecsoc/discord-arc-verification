/**
 * User related handlers.
 */

import { Message } from "discord.js";


/**
 * Revokes access for a server admin to the user's personal data. Immediately
 * remove verified role from the guild. Warn user that data will remain
 * accessible to guild admins for 1 week due to auditing.
 * @param arg server name
 * @param ctx message context
 */
export function revokeAccess(arg: string, ctx: Message): void {
    return;
}

/**
 * Warn users that they will potentially lose their verified role on all
 * guilds,and that their data will remain accessible to guild admins for
 * 1 week due to auditing.
 * @param arg 
 * @param ctx message context
 */
export function warnDeleteAllRecords(arg: string, ctx: Message): void {
    return;
}

/**
 * Mark account for deletion and immediately revokes the verified role from
 * all guilds.
 * @param arg 
 * @param ctx message context
 */
export function deleteAllRecords(arg: string, ctx: Message): void {
    return;
}